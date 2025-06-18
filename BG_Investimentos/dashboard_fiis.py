import streamlit as st
import pandas as pd
import plotly.express as px

# 🎯 Configuração da página
st.set_page_config(page_title="BG Analista de FIIs", layout="wide")

st.title("🏢 BG Analista — Dashboard de FIIs")
st.subheader("Análise de Fundos Imobiliários — Com Recomendação Inteligente")

st.markdown("---")

# 📥 Upload do CSV
uploaded_file = st.sidebar.file_uploader(
    "📥 Faça upload do arquivo CSV dos FIIs (ou use o arquivo padrão)",
    type=["csv"]
)

# 🗂️ Fallback: Se não fizer upload, carrega o CSV da pasta ./dados/
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Arquivo carregado com sucesso via upload!")
else:
    try:
        df = pd.read_csv('./dados/fiis.csv')
        st.info("ℹ️ Nenhum arquivo foi enviado. Usando o arquivo padrão da pasta './dados/fiis.csv'.")
    except Exception as e:
        st.error(f"❌ Nenhum arquivo foi enviado e não encontramos o arquivo padrão. Erro: {e}")
        st.stop()

# 🎯 Função de Recomendação
def gerar_recomendacao_fii(row):
    if row['P/VP'] < 0.95 and row['Dividend Yield (%)'] > 9 and row['Vacância (%)'] < 5:
        return 'Comprar'
    elif row['P/VP'] > 1.10 or row['Vacância (%)'] > 10:
        return 'Vender'
    else:
        return 'Manter'

# ✔️ Aplicar recomendação se não existir
if 'Recomendação' not in df.columns:
    df['Recomendação'] = df.apply(gerar_recomendacao_fii, axis=1)

# 🎯 Cards de Resumo Gerais
st.subheader("📊 Resumo Geral dos FIIs")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total de FIIs", df.shape[0])
col2.metric("DY Médio (%)", f"{round(df['Dividend Yield (%)'].mean(), 2)}%")
col3.metric("Vacância Média (%)", f"{round(df['Vacância (%)'].mean(), 2)}%")
col4.metric("P/VP Médio", round(df['P/VP'].mean(), 2))

st.markdown("---")

# 🎯 Cards de Recomendação
st.subheader("🎯 Distribuição das Recomendações")

col5, col6, col7 = st.columns(3)

total_comprar = df[df['Recomendação'] == 'Comprar'].shape[0]
total_manter = df[df['Recomendação'] == 'Manter'].shape[0]
total_vender = df[df['Recomendação'] == 'Vender'].shape[0]

col5.metric("🟢 Comprar", total_comprar)
col6.metric("🟡 Manter", total_manter)
col7.metric("🔴 Vender", total_vender)

st.markdown("---")

# 📊 Gráfico de Pizza — Distribuição das Recomendações
recomendacoes = df['Recomendação'].value_counts().reset_index()
recomendacoes.columns = ['Recomendacao', 'Count']

fig_pizza = px.pie(
    recomendacoes,
    names='Recomendacao',
    values='Count',
    title='Distribuição das Recomendações',
    color_discrete_map={
        'Comprar': 'green',
        'Manter': 'gold',
        'Vender': 'red'
    }
)
st.plotly_chart(fig_pizza, use_container_width=True)

st.markdown("---")

# 🎯 Gráficos padrão
st.subheader("📊 Análise dos Indicadores")

# 📈 DY
fig_dy = px.bar(
    df,
    x='Ticker',
    y='Dividend Yield (%)',
    title='Dividend Yield (%) por FII',
    text_auto=True,
    color='Recomendação'
)
st.plotly_chart(fig_dy, use_container_width=True)

# 📈 P/VP
fig_pvp = px.bar(
    df,
    x='Ticker',
    y='P/VP',
    title='P/VP por FII',
    text_auto=True,
    color='Recomendação'
)
st.plotly_chart(fig_pvp, use_container_width=True)

# 📈 Vacância
fig_vacancia = px.bar(
    df,
    x='Ticker',
    y='Vacância (%)',
    title='Vacância (%) por FII',
    text_auto=True,
    color='Recomendação'
)
st.plotly_chart(fig_vacancia, use_container_width=True)

st.markdown("---")

# 🎯 Filtros na Tabela
st.subheader("🔎 Filtro e Dados Detalhados")

filtro_recomendacao = st.multiselect(
    "Filtrar por Recomendação:",
    options=df['Recomendação'].unique(),
    default=df['Recomendação'].unique()
)

df_filtrado = df[df['Recomendação'].isin(filtro_recomendacao)]

st.dataframe(df_filtrado, use_container_width=True)

# 📥 Download do relatório filtrado
csv = df_filtrado.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Relatório CSV Filtrado",
    data=csv,
    file_name='relatorio_bg_fiis.csv',
    mime='text/csv',
)

st.markdown("---")
st.caption("BG Analista — Dashboard exclusivo de FIIs • Desenvolvido por Helder")
