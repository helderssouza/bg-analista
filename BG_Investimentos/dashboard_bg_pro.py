import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================
# 🔒 SISTEMA DE LOGIN + LOGOUT
# ==============================================

# 🔐 Usuários e Senhas
USER_CREDENTIALS = {
    "admin": "1234",
    "helder": "abcd"
}

# Inicializar o estado de sessão
if 'logado' not in st.session_state:
    st.session_state['logado'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = ""

# 🔒 Função de autenticação
def autenticar_usuario():
    with st.sidebar:
        st.subheader("🔑 Login")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        if st.button("Entrar"):
            if usuario in USER_CREDENTIALS and senha == USER_CREDENTIALS[usuario]:
                st.session_state['logado'] = True
                st.session_state['usuario'] = usuario
                st.success(f"✅ Bem-vindo, {usuario}!")
            else:
                st.error("❌ Usuário ou senha incorretos.")

# 🔒 Função de logout
def logout():
    st.session_state['logado'] = False
    st.session_state['usuario'] = ""
    st.experimental_rerun()

# 🔐 Controle de login
if not st.session_state['logado']:
    autenticar_usuario()
    st.stop()

# ==============================================
# 🎯 CONFIGURAÇÃO DO DASHBOARD
# ==============================================

st.set_page_config(page_title="BG PRO — Ações e FIIs", layout="wide")

st.title("💼 BG PRO — Dashboard de Ações e FIIs")
st.markdown("---")

# 🎯 Menu Lateral + Logout
st.sidebar.success(f"👋 Usuário: {st.session_state['usuario']}")
if st.sidebar.button("🚪 Logout"):
    logout()

menu = st.sidebar.selectbox(
    "Selecione a Análise:",
    ("🏠 Dashboard Geral", "📈 Ações", "🏢 FIIs")
)

st.sidebar.subheader("📥 Upload dos Dados")

# 🔥 Função para carregar dados com fallback
def carregar_dados(caminho, texto_upload):
    if os.path.exists(caminho):
        return pd.read_csv(caminho)
    else:
        arquivo = st.sidebar.file_uploader(texto_upload, type=["csv"])
        if arquivo is not None:
            return pd.read_csv(arquivo)
        else:
            st.warning(f"⚠️ Envie o arquivo {texto_upload} na barra lateral.")
            st.stop()

# 📄 Carregar Ações
df_acoes = carregar_dados('BG_Investimentos/dados/acoes.csv', "Upload CSV de Ações")

# 📄 Carregar FIIs
df_fiis = carregar_dados('BG_Investimentos/dados/fiis.csv', "Upload CSV de FIIs")

# 🔥 Função de recomendação para Ações
def gerar_recomendacao_acao(row):
    if row['Upside (%)'] > 10 and row['Dividend Yield (%)'] >= 6 and row['ROE (%)'] >= 15:
        return 'Comprar'
    elif row['Upside (%)'] < -5:
        return 'Vender'
    else:
        return 'Manter'

if 'Recomendação' not in df_acoes.columns:
    df_acoes['Recomendação'] = df_acoes.apply(gerar_recomendacao_acao, axis=1)

# 🔥 Função de recomendação para FIIs
def gerar_recomendacao_fii(row):
    if row['P/VP'] < 0.95 and row['Dividend Yield (%)'] > 9 and row['Vacância (%)'] < 5:
        return 'Comprar'
    elif row['P/VP'] > 1.10 or row['Vacância (%)'] > 10:
        return 'Vender'
    else:
        return 'Manter'

if 'Recomendação' not in df_fiis.columns:
    df_fiis['Recomendação'] = df_fiis.apply(gerar_recomendacao_fii, axis=1)

# =====================
# 🏠 DASHBOARD GERAL
# =====================
if menu == "🏠 Dashboard Geral":
    st.subheader("📊 Visão Geral dos Ativos")

    total_acoes = df_acoes.shape[0]
    total_fiis = df_fiis.shape[0]

    col1, col2 = st.columns(2)
    col1.metric("💼 Total de Ações", total_acoes)
    col2.metric("🏢 Total de FIIs", total_fiis)

    col3, col4 = st.columns(2)
    col3.metric("📈 DY Médio Ações", f"{round(df_acoes['Dividend Yield (%)'].mean(), 2)}%")
    col4.metric("🏢 DY Médio FIIs", f"{round(df_fiis['Dividend Yield (%)'].mean(), 2)}%")

    col5, col6 = st.columns(2)
    col5.metric("🚀 Upside Médio Ações", f"{round(df_acoes['Upside (%)'].mean(), 2)}%")
    col6.metric("📏 P/VP Médio FIIs", round(df_fiis['P/VP'].mean(), 2))

    st.markdown("---")

    st.subheader("🟢🟡🔴 Distribuição das Recomendações")

    col7, col8 = st.columns(2)

    recomendacoes_acoes = df_acoes['Recomendação'].value_counts().reset_index()
    recomendacoes_acoes.columns = ['Recomendacao', 'Count']

    fig_acoes = px.pie(
        recomendacoes_acoes,
        names='Recomendacao',
        values='Count',
        title='Distribuição das Recomendações - Ações',
        color_discrete_map={'Comprar': 'green', 'Manter': 'gold', 'Vender': 'red'}
    )
    col7.plotly_chart(fig_acoes, use_container_width=True)

    recomendacoes_fiis = df_fiis['Recomendação'].value_counts().reset_index()
    recomendacoes_fiis.columns = ['Recomendacao', 'Count']

    fig_fiis = px.pie(
        recomendacoes_fiis,
        names='Recomendacao',
        values='Count',
        title='Distribuição das Recomendações - FIIs',
        color_discrete_map={'Comprar': 'green', 'Manter': 'gold', 'Vender': 'red'}
    )
    col8.plotly_chart(fig_fiis, use_container_width=True)

# =====================
# 📈 DASHBOARD AÇÕES
# =====================
elif menu == "📈 Ações":
    st.subheader("📈 Análise de Ações")

    st.dataframe(df_acoes, use_container_width=True)

    fig_dy = px.bar(
        df_acoes,
        x='Ticker',
        y='Dividend Yield (%)',
        title='Dividend Yield (%) por Ação',
        color='Recomendação'
    )
    st.plotly_chart(fig_dy, use_container_width=True)

    fig_upside = px.bar(
        df_acoes,
        x='Ticker',
        y='Upside (%)',
        title='Upside (%) por Ação',
        color='Recomendação'
    )
    st.plotly_chart(fig_upside, use_container_width=True)

    csv = df_acoes.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados das Ações CSV",
        data=csv,
        file_name='relatorio_bg_acoes.csv',
        mime='text/csv',
    )

# =====================
# 🏢 DASHBOARD FIIs
# =====================
elif menu == "🏢 FIIs":
    st.subheader("🏢 Análise de FIIs")

    st.dataframe(df_fiis, use_container_width=True)

    fig_dy = px.bar(
        df_fiis,
        x='Ticker',
        y='Dividend Yield (%)',
        title='Dividend Yield (%) por FII',
        color='Recomendação'
    )
    st.plotly_chart(fig_dy, use_container_width=True)

    fig_pvp = px.bar(
        df_fiis,
        x='Ticker',
        y='P/VP',
        title='P/VP por FII',
        color='Recomendação'
    )
    st.plotly_chart(fig_pvp, use_container_width=True)

    fig_vacancia = px.bar(
        df_fiis,
        x='Ticker',
        y='Vacância (%)',
        title='Vacância (%) por FII',
        color='Recomendação'
    )
    st.plotly_chart(fig_vacancia, use_container_width=True)

    csv = df_fiis.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados dos FIIs CSV",
        data=csv,
        file_name='relatorio_bg_fiis.csv',
        mime='text/csv',
    )
