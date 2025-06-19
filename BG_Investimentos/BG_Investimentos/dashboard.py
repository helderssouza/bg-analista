import streamlit as st
import pandas as pd
import plotly.express as px
from coleta_dados import obter_dados
from analise import gerar_recomendacao

# 🎯 Configuração da página
st.set_page_config(page_title="BG Analista de Ações e FIIs", layout="wide")

# 🎯 Cabeçalho
st.title("📈 BG Analista de Ações e FIIs")
st.subheader("Análise baseada nos métodos de Buffett e Graham")

st.markdown("---")

# 🎯 Sidebar — Configuração dos ativos
st.sidebar.header("Configuração dos Ativos")

ativos = st.sidebar.text_input(
    "Digite os tickers separados por vírgula (Ex.: ITSA4.SA, WEGE3.SA, TAEE11.SA)",
    value="ITSA4.SA, WEGE3.SA, TAEE11.SA, HGLG11.SA, MXRF11.SA"
).split(",")

ativos = [a.strip().upper() for a in ativos]

st.sidebar.markdown("---")
rodar = st.sidebar.button("🔍 Rodar Análise")

if rodar:
    st.subheader("🔍 Resultado da Análise")

    dados = []
    for ticker in ativos:
        try:
            dados.append(obter_dados(ticker))
        except Exception as e:
            st.error(f"Erro ao obter dados de {ticker}: {e}")

    if dados:
        df = pd.DataFrame(dados)
        df['Recomendação'] = df.apply(gerar_recomendacao, axis=1)

        # 🎯 Cards de resumo
        col1, col2, col3, col4 = st.columns(4)

        total_ativos = df.shape[0]
        total_comprar = df[df['Recomendação'] == 'Comprar'].shape[0]
        total_manter = df[df['Recomendação'] == 'Manter'].shape[0]
        total_vender = df[df['Recomendação'] == 'Vender'].shape[0]
        media_dy = round(df['DY (%)'].mean(), 2)
        media_upside = round(df['Upside (%)'].mean(), 2)

        col1.metric("🔢 Total de Ativos", total_ativos)
        col2.metric("🟢 Comprar", total_comprar)
        col3.metric("🟡 Manter", total_manter)
        col4.metric("🔴 Vender", total_vender)

        st.markdown("---")

        col5, col6 = st.columns(2)
        col5.metric("💰 DY Médio (%)", f"{media_dy}%")
        col6.metric("🚀 Upside Médio (%)", f"{media_upside}%")

        st.markdown("---")

        # 📊 Gráfico de Pizza — Recomendações
        recomendacoes = df['Recomendação'].value_counts().reset_index()
        recomendacoes.columns = ['Recomendacao', 'Count']

        fig_pizza = px.pie(
            recomendacoes,
            names='Recomendacao',
            values='Count',
            title='Distribuição das Recomendações',
            color_discrete_sequence=px.colors.qualitative.Set3
        )

        st.plotly_chart(fig_pizza, use_container_width=True)

        # 📈 Gráfico de Barras — Dividend Yield por Ativo
        fig_bar = px.bar(
            df,
            x='Ticker',
            y='DY (%)',
            title='Dividend Yield (%) por Ativo',
            text_auto=True,
            color='Recomendação'
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # 📈 Gráfico de Barras — Upside por Ativo
        fig_upside = px.bar(
            df,
            x='Ticker',
            y='Upside (%)',
            title='Upside (%) por Ativo',
            text_auto=True,
            color='Recomendação'
        )
        st.plotly_chart(fig_upside, use_container_width=True)

        st.markdown("---")

        # 📄 Tabela
        st.subheader("📄 Dados Detalhados")
        st.dataframe(df, use_container_width=True)

        # 📥 Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Baixar Relatório CSV",
            data=csv,
            file_name='relatorio_bg_analista.csv',
            mime='text/csv',
        )
    else:
        st.warning("Nenhum dado coletado. Verifique os tickers e tente novamente.")

else:
    st.info("Configure os ativos na barra lateral e clique em 'Rodar Análise'.")

st.markdown("---")
st.caption("BG Analista — Desenvolvido por Helder • Baseado nos métodos de Buffett e Graham")
