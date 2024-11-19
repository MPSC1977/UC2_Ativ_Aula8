import os

os.system('cls')

import pandas as pd
import numpy as np

try:
    print('Obtendo dados...')

    tb_vendas = pd.read_csv('tb_Vendas2017_Miranda.csv', sep=';', encoding='iso8859-1')
    tb_cadastro_produtos = pd.read_csv('tb_CadastroProdutos2017_Miranda.csv', sep=';', encoding='iso8859-1')

    df_vendas = tb_vendas[['ID Produto', 'Quantidade Vendida']]
    df_cadastro_produtos = tb_cadastro_produtos[['ID Produto', 'Preco Unitario', 'Categoria']]

    df_cadastro_produtos.loc[:, 'Preco Unitario'] = df_cadastro_produtos['Preco Unitario'].str.replace(',', '.').astype(float)

    print('\nDados obtidos com sucesso!')

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()

try:
    df_tabelas_concat = pd.merge(df_cadastro_produtos, df_vendas, on= 'ID Produto')

    df_tabelas_concat['Valor Total'] = df_tabelas_concat['Quantidade Vendida'] * df_tabelas_concat['Preco Unitario']

    df_tabelas_concat_agrup = df_tabelas_concat.groupby('ID Produto').agg({'Quantidade Vendida': 'sum', 'Valor Total': 'sum'}).reset_index()
    print()
    print(df_tabelas_concat_agrup.head(10))

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()

try:
   array_vendas = np.array(df_tabelas_concat_agrup['Valor Total'])

   media_qtde_vendida = np.mean(array_vendas)
   mediana_qtde_vendida = np.median(array_vendas)
   distancia = abs((media_qtde_vendida - mediana_qtde_vendida) / mediana_qtde_vendida) * 100

   maximo = np.max(array_vendas)
   minimo = np.min(array_vendas)
   amplitude = maximo - minimo

   q1 = np.quantile(array_vendas, 0.25, method='weibull')
   q2 = np.quantile(array_vendas, 0.50, method='weibull')
   q3 = np.quantile(array_vendas, 0.75, method='weibull')
   iqr = q3 - q1
   limite_superior = q3 + (1.5 * iqr)
   limite_inferior = q1 - (1.5 * iqr)

   df_vendas_outliers_inferiores = df_tabelas_concat_agrup[df_tabelas_concat_agrup['Valor Total'] < limite_inferior]
   df_vendas_outliers_superiores = df_tabelas_concat_agrup[df_tabelas_concat_agrup['Valor Total'] > limite_superior]

   print('\nMEDIDAS DE TENDÊNCIA CENTRAL')
   print(30*'=')
   print(f'A média de vendas registrada é de: {media_qtde_vendida:.2f}')
   print(f'A mediana de vendas regsitrada é de: {mediana_qtde_vendida:.2f}')
   print(f'A distância entre a média e a mediana de vendas é: {distancia:.2f}%')
    
   print('\nMEDIDAS DE DISPERSÃO')
   print(20*'=')
   print(f'Máximo: {maximo:.2f}')
   print(f'Mínimo: {minimo:.2f}')
   print(f'Amplitude total: {amplitude}')

   print('\nMEDIDAS DE POSIÇÃO')
   print(20*'=')
   print(f'Mínimo: {minimo:.2f}')
   print(f'Limite inferior: {limite_inferior:.2f}')
   print(f'Q1: {q1:.2f}')
   print(f'Q2: {q2:.2f}')
   print(f'Q3: {q3:.2f}')
   print(f'IQR: {iqr:.2f}')
   print(f'Limite superior: {limite_superior:.2f}')
   print(f'Máximo: {maximo:.2f}')

   print('\nOUTLIERS')
   print(25*'=')

   print('\nOutliers inferiores')
   print(20*'=')
   if len(df_vendas_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
   else:
        print(df_vendas_outliers_inferiores.sort_values(by='Valor Total', ascending=True))

   print('\nOutliers superiores: ')
   print(20*'=')
   if len(df_vendas_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
   else:
        print(df_vendas_outliers_superiores.sort_values(by='Valor Total', ascending=False))

   print('\nCONCLUSÃO DA ANÁLISE: ')
   print('\n ')


except ImportError as e:
   print(f'Erro ao obter dados: {e}')
   exit() 
