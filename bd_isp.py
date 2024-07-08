import sqlite3

import pandas as pd

# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('bd_isp.db')
cursor = conn.cursor()

# Lista de arquivos CSV e nomes de tabelas correspondentes
arquivos_csv = ['bp_cv.csv', 'bp_pa.csv', 'arm.csv']
nomes_tabelas = ['casos_vitimas', 'prisoes_apreesoes', 'armas']

for arquivo_csv, nome_tabela in zip(arquivos_csv, nomes_tabelas):
    # Ler o arquivo CSV em um DataFrame do pandas
    df = pd.read_csv(arquivo_csv, sep=',')

    # Converter o DataFrame em uma tabela no SQLite
    df.to_sql(nome_tabela, conn, if_exists='replace', index=False)

# Fechar a conexão com o banco de dados
conn.close()

print('Arquivos CSV convertidos em tabelas SQLite com sucesso.')
