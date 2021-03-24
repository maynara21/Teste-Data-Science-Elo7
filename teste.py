import sys
import os
import re
import functions

# os valores de preco sao reconhecidos por valores cheios ou com duas casas decimais com '.'
# string da 'query' é alfanumérica
msg_err = '''\n\nArgumentos inválidos!! :(\n
        Opções:
        -> teste_ds.py --category "{'query':<input_da_feature_1>,'price':<input_da_feature_2>}"
        -> teste_ds.py --intent "<termo_de_busca_do_usuário>"
        -> teste_ds.py --recommendation "<termo_de_busca_do_usuário>" \n\n'''

assert len(sys.argv) == 3 and (sys.argv[1] == '--category' or sys.argv[1] == '--intent' or sys.argv[1] == '--recommendation') , msg_err

# Classificacao de produtos
if sys.argv[1] == '--category':
    
    # Exemplo de arg valido para a classificacao "{'query':bonecas,'price':35.45}"
    
    msg_err_cat = "\n\nArgumento " + sys.argv[2] + " inválido!! :(" + " \n\nEntre com o devido padrão: \n\n" + \
              '''"{'query':<input_da_feature_1>,'price':<input_da_feature_2>}"\n\n'''
    
    # expressao regular para validar o formato da string recebida no 2 arg para a classificacao
    features = re.findall("\{\'query\':[\s\w]*\,\'price\'\:[0-9]*\.?[0-9]{0,2}\}", sys.argv[2])
    
    assert len(features) == 1, msg_err_cat
    
    # estruturando o argumento para a funcao de classificacao
    arg = features[0].strip("{}")
    arg = re.split("[,:']+", arg)[1:]
    dic_arg = {arg[0]:arg[1],arg[2]:float(arg[3])}
    
    print(functions.category(dic_arg))

# Classificação de termos de busca
elif sys.argv[1] == '--intent':
    
    intent_class, intent_class_num, _ = functions.intent(sys.argv[2])
    print(intent_class)
    
# Sistema híbrido
else:

    intent, intent_num, price = functions.intent(sys.argv[2])
    dic_arg = {'query':sys.argv[2], 'price':price}
    category = functions.category(dic_arg)
    product_rec = functions.recommendation(sys.argv[2], intent_num)
    
    print(category)
    print(intent)
    for indx, value in product_rec.items():
        print(indx,',',value)
    
    
    