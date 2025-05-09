
# IMPORTANDO AS BIBLITOECAS
import pandas as pd
import sqlite3 
from datetime import datetime

# LENDO OS DADOS DO ARQUIVO DATA.JSON
df = pd.read_json('data/data.json')

# CONFIGURANDO PARA EXIBIR TODAS AS COLUNAS DO DF
pd.options.display.max_columns = None

# CRIANDO A COLUNA SOURCE COM A URL DA ORIGEM DOS DADOS
df['_source'] = "https://www.saldaodainformatica.com.br/notebook"

# CRIANDO COLUNA COM A DATA E HORA DA COLETA
df['_datetime'] = datetime.now()

# CONVERTENDO AS COLUNAS DE PREÇO PARA STRING 
df['preco_antigo'] = df['preco_antigo'].astype(str)
df['preco_final'] = df['preco_final'].astype(str)

# REALIZANDO A LIMPEZA DAS COLUNAS DE PREÇO
df['preco_antigo'] = df['preco_antigo'].str.replace('de: R$', '', regex=False).str.strip()
df['preco_antigo'] = df['preco_antigo'].str.replace(',', '.', regex=False)
df['preco_antigo'] = df['preco_antigo'].str.replace('.', '', regex=False)
df['preco_final'] = df['preco_final'].str.replace('R$', '', regex=False).str.strip()
df['preco_final'] = df['preco_final'].str.replace(',','.', regex=False)
df['preco_final'] = df['preco_final'].str.replace('.', '', regex=False)

# CONVERTENDO AS COLUNSA PARA FLOAT
df['preco_antigo'] = df['preco_antigo'].astype(float)
df['preco_final'] = df['preco_final'].astype(float)

# FUNÇÃO PARA EXTRAIR A MARCA DOS PRODUTOS
def extrair_marca(produto):
    if "Acer" in produto:
        return "Acer"
    elif "HP" in produto:
        return "HP"
    elif "Lenovo" in produto:
        return "Lenovo"
    elif "Positivo" in produto:
        return "Positivo"
    elif "Apple" in produto:
        return "Apple"
    elif "Vaio" in produto:
        return "Vaio"
    elif "Thinkpad" in produto:
        return "Thinkpad"
    elif "Asus" in produto:
        return "Asus"
    elif "Dell" in produto:
        return "Dell"
    elif "Samsung" in produto:
        return "Samsung"
    else:
        return None

# APLICANDO A FUNÇÃO E ATUALIZANDO O DF CRIANDO A COLUNA 'BRAND'
df['brand'] = df['produto'].apply(extrair_marca)
print(df.head())

cols = df.columns.tolist() # OBTÉM A LISTA DE COLUNAS
cols.insert(1, cols.pop(cols.index('brand'))) # MOVE BRAND PARA A SEGUNDA POSIÇÃO
df = df[cols] # REORDENA AS COLUNAS

# CONECTANDO AO BANCO DE DADOS SQLITE
conn = sqlite3.connect('data/notebooks.db')

# SALVANDO O DATAFRAME NO DB SQLITE
df.to_sql('notebook', conn, if_exists='replace', index=False)

# FECHANDO A CONEXÃO COM O DB
conn.close()

