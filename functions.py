import numpy as np
import pandas as pd
from joblib import dump, load
from sklearn.metrics.pairwise import cosine_similarity

def category(dict_features):
    ''' função recebe como parametro uma dicionario:
    {'query': <nome_da_entrada>, 'price': <valor>}
    '''
    
    # categorias de produto
    category_list = ['Lembrancinhas','Decoração','Bebê','Papel e Cia','Outros','Bijuterias e Jóias']
    
    # vetorizando com tfidf
    vect = load('models/TFIDF_elo7data.pkl')
    query_vect = vect.transform([dict_features['query']]).toarray()[0]
    price = np.log1p(dict_features['price'])
    query_vect = np.append(query_vect,[price],axis=0)
    
    # classficacao com svm
    clf = load('models/SVM_elo7data.pkl') 
    category = clf.predict([query_vect])[0]
    
    return category_list[category] # retorna a categoria do produto

def intent(query):
    ''' Funcao recebe como parametro a 
        query de entrada do usuario (string)
    '''
    # Classes de intencao do cliente
    intent_class_list = ['Clientes que procuram algo barato e popular',
    'Clientes que procuram artigos mais sofisticados (preços maiores)',
    'Clientes que procuram presentes ou artigos "fora da curva", baratos, porém pouco populares',
    'Clientes que procuram artigos mais caros e populares']
    
    # vetorizando com tfidf
    vect = load('models/TFIDF_elo7data2.pkl')
    query_vect = vect.transform([query]).toarray()[0]
    
    # classificando com svm
    clf = load('models/SVM_elo7data2.pkl') 
    intent_class = clf.predict([query_vect])[0]
    
    # abrindo arquivo com preco medio de cada categoria de intencao
    with open('docs/mean_price.txt', mode='r') as f:
        price = f.read()
    
    price = list(map(lambda x: float(x),price.split()))
    
    #retorna o nome da classe de intencao, o número e o preco medio da mesma
    return intent_class_list[intent_class], intent_class, price[intent_class]

def recommendation(query, intent_num):
    '''Funcao recebe como parametro a query (string)
       e o numero da classe de intencao do cliente
    '''
    
    # carregando produtos rotulados nas classes de intencao
    products_data = pd.read_csv('dataset/elo7data_intent_labels.csv')
    
    # vetorizando com tfidf
    vect = load('models/TFIDF_elo7data2.pkl')  
    query_vec = vect.transform([query])
    query_tags = vect.transform(products_data['query_tags'])
    
    # calculando a semelhanca de cosseno entre as query_tags dos produtos e a query de entrada
    cossim = [cosine_similarity([vec], query_vec) for vec in query_tags.toarray()]
    cossim = list(map(lambda x: x[0][0], cossim))
    products_data['cossim'] = cossim
    
    # filtrando os produtos da classe de intencao
    products_data = products_data[products_data['clusters']==intent_num] 
    
    # retornando os 10 produtos com maior similaridade
    products_rec = products_data.sort_values(by=['cossim'],ascending=False).head(10)
    dic_products = dict(products_rec[['product_id','title']].values)
    
    return dic_products
    