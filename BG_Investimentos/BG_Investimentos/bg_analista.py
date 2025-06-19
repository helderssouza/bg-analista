import pandas as pd
from coleta_dados import obter_dados
from analise import gerar_recomendacao

# ✅ Lista de ativos
ativos = ['ITSA4.SA', 'WEGE3.SA', 'TAEE11.SA', 'HGLG11.SA', 'MXRF11.SA']

# ✅ Coletar dados
dados = []
for ticker in ativos:
    try:
        dados.append(obter_dados(ticker))
    except Exception as e:
        print(f"Erro ao obter dados de {ticker}: {e}")

# ✅ Criar DataFrame
df = pd.DataFrame(dados)

# ✅ Aplicar análise
df['Recomendação'] = df.apply(gerar_recomendacao, axis=1)

# ✅ Exibir no console
print("\n===== RELATÓRIO BG ANALISTA =====")
print(df)

# ✅ Salvar no Excel
df.to_excel('./relatorios/relatorio_bg_analista.xlsx', index=False)
print("\nRelatório salvo na pasta relatorios")
