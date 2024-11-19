import os

os.system('cls')

import pandas as pd
import numpy as np

try:
    print('Obtendo dados...')

    tb_vendas = pd.read_csv('tb_Vendas2017_Miranda.csv', sep=';', encoding='iso8859-1')
    tb_cadastro_produtos = pd.read_csv('tb_CadastroProdutos2017_Miranda.csv', sep=';', encoding='iso8859-1')

    # print(tb_vendas.columns)
    # print(tb_cadastro_produtos.columns)

    df_vendas = tb_vendas[['ID Produto', 'Quantidade Vendida']]
    df_cadastro_produtos = tb_cadastro_produtos[['ID Produto', 'Preco Unitario', 'Categoria']]
    print(df_vendas.columns)

    df_cadastro_produtos.loc[:, 'Preco Unitario'] = df_cadastro_produtos['Preco Unitario'].str.replace(',', '.').astype(float)

    df_tabelas_concat = pd.merge(df_cadastro_produtos, df_vendas, on= 'ID Produto')
    print(df_tabelas_concat)

    df_tabelas_concat_agrup = df_tabelas_concat.groupby(['Categoria']).sum(['Quantidade Vendida']).reset_index()
    print(df_tabelas_concat_agrup)

except ImportError as e:
    print(f'Erro ao obter dados: {e}')
    exit()


try:
   array_vendas = np.array(df_tabelas_concat_agrup['Quantidade Vendida'])
   print(array_vendas)

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

   df_vendas_outliers_inferiores = df_vendas[df_vendas['Quantidade Vendida'] < limite_inferior]
   df_vendas_outliers_superiores = df_vendas[df_vendas['Quantidade Vendida'] > limite_superior]

   print('\nMEDIDAS DE TENDÊNCIA CENTRAL')
   print(30*'=')
   print(f'A média de vendas registrada é de: {media_qtde_vendida:.2f}')
   print(f'A mediana de vendas regsitrada é de: {mediana_qtde_vendida:.2f}')
   print(f'A distância entre a média e a mediana de vendas é: {distancia:.2f}%')
    
   print('\nMEDIDAS DE DISPERSÃO')
   print(20*'=')
   print(f'Máximo: {maximo}')
   print(f'Mínimo: {minimo}')
   print(f'Amplitude total: {amplitude}')

   print('\nMEDIDAS DE POSIÇÃO')
   print(20*'=')
   print(f'Mínimo: {minimo}')
   print(f'Limite inferior: {limite_inferior}')
   print(f'Q1: {q1}')
   print(f'Q2: {q2}')
   print(f'Q3: {q3}')
   print(f'IQR: {iqr}')
   print(f'Limite superior: {limite_superior}')
   print(f'Máximo: {maximo}')

   print('\nOUTLIERS')
   print(25*'=')

   print('\nOutliers inferiores')
   print(20*'=')
   if len(df_vendas_outliers_inferiores) == 0:
        print('Não existem outliers inferiores!')
   else:
        print(df_vendas_outliers_inferiores.sort_values(by='Quantidade Vendida', ascending=True))

   print('\nOutliers superiores: ')
   print(20*'=')
   if len(df_vendas_outliers_superiores) == 0:
        print('Não existe outliers superiores!')
   else:
        print(df_vendas_outliers_superiores.sort_values(by='Quantidade Vendida', ascending=False))

   print('\nCONCLUSÃO DA ANÁLISE: ')
   print('\n ')


except ImportError as e:
   print(f'Erro ao obter dados: {e}')
   exit() 