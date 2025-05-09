
# CARREGAMENTO DAS BIBLIOTECAS
import streamlit as st
import pandas as pd
import sqlite3

# CONECTANDO AO BANCO DE DADOS SQLITE3
conn = sqlite3.connect('data/notebooks.db')

# CARREGAR OS DADOS DA TABELA EM UM DATAFRAME PANDAS
df = pd.read_sql_query("SELECT * FROM notebook", conn)

# FECHANDO A CONEXÃO
conn.close()

# TITULO 
st.title('📊 Pesquisa de Mercado - Notebooks no Site do Fornecedor')


# LAYOUT COM COLUNAS PARA OS INDICADORES
st.subheader('💡 Principais índicadores')
col1, col2, col3 = st.columns(3)

# INDICADOR 1: NÚMERO TOTAL DE ITENS
total_itens = df.shape[0]
col1.metric(label="🖥️ Total de Notebooks",value=total_itens)


# INDICADOR 2: NÚMERO DE MARCAS ÚNICAS
marcas_unicas = df['brand'].nunique()
col2.metric(label="🏷️ Marcas Únicas", value=marcas_unicas)


# INDICADOR 3: PREÇO MÉDIO
preco_medio_final = df['preco_final'].mean()
preco_medio_formatado = f"{preco_medio_final:,.2f}"
col3.metric(label="💰 Preço Médio (R$)", value=preco_medio_formatado)


# MARCAS MAIS FREQUENTES
st.subheader('🏆 Marcas mais encontradas até a 10ª página')
col1, col2 = st.columns([4, 2])
top_marcas = df['brand'].value_counts().sort_values(ascending=False)
col1.bar_chart(top_marcas)


# VALOR MÉDIO POR MARCA
st.subheader('💵 Preço médio por marca')
col1, col2 = st.columns([4, 2])
precos_diferentes_de_zero = df[df['preco_final'] > 0]
preco_medio_por_marca = precos_diferentes_de_zero.groupby('brand')['preco_final'].mean().sort_values(ascending=False)
col1.bar_chart(preco_medio_por_marca)


# TITULO DA ANÁLISE DE DESCONTOS
st.subheader('📉 Análise de Descontos')
col1_desc, col2_desc = st.columns(2)

# INDICADOR 4: MÉDIA DE DESCONTO
desconto_medio = ((df['preco_antigo'] - df['preco_final']) / df['preco_antigo']).mean() * 100
col1_desc.metric(label="📉 Desconto Médio", value=f"{desconto_medio:.1f}%")


# INDICADOR 5: ECONOMIA MÉDIA POR PRODUTO
economia_media = (df['preco_antigo'] - df['preco_final']).mean()
col2_desc.metric(label="💰 Economia Média (R$)", value=f"{economia_media:,.2f}")

# GRÁFICO DA DISTRIBUIÇÃO DE DESCONTOS
st.subheader('📊 Distribuição de Descontos')
faixas_desconto = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0] # Faixas de 0-10%, 10-20%, ...
labels_desconto = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '>50%']
df['desconto_percentual'] = (df['preco_antigo'] - df['preco_final']) / df['preco_antigo']
df['faixa_desconto'] = pd.cut(df['desconto_percentual'], bins=faixas_desconto, labels=labels_desconto, right=False)
distribuicao_descontos = df['faixa_desconto'].value_counts().sort_index()
st.bar_chart(distribuicao_descontos)

# TITULO 
st.subheader('🏷️ Marcas e Preços')
col1_marca_preco, col2_marca_preco = st.columns(2)


# INDICADOR 6: MARCA COM O MAIOR DESCONTO MÉDIO
desconto_medio_por_marca = df.groupby('brand').apply(lambda x: ((x['preco_antigo'] - x['preco_final']) / x['preco_antigo']).mean() * 100).sort_values(ascending=False)
marca_maior_desconto = desconto_medio_por_marca.index[0]
maior_desconto = desconto_medio_por_marca.iloc[0]
col1_marca_preco.metric(label="🏆 Marca com Maior Desconto Médio", value=f"{marca_maior_desconto} ({maior_desconto:.1f}%)")


# GRÁFICO DE AMPLITUDE DE VALOR POR MARCA
amplitude_preco_por_marca = df.groupby('brand')['preco_final'].max() - df.groupby('brand')['preco_final'].min()
col2_marca_preco.subheader('↔️ Amplitude de Preço por Marca')
st.bar_chart(amplitude_preco_por_marca.sort_values(ascending=False))

