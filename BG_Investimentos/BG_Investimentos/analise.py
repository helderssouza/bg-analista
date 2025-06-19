def gerar_recomendacao(row):
    if row['Upside (%)'] > 10 and row['DY (%)'] >= 6 and row['ROE (%)'] >= 15:
        return 'Comprar'
    elif row['Upside (%)'] < -5:
        return 'Vender'
    else:
        return 'Manter'
