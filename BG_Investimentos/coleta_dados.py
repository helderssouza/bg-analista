import yfinance as yf

def obter_dados(ticker):
    acao = yf.Ticker(ticker)
    info = acao.info

    preco = info.get('currentPrice', 0)
    pl = info.get('trailingPE', 0)
    dy = info.get('dividendYield', 0) or 0
    dy = dy * 100 if dy else 0
    roe = info.get('returnOnEquity', 0) or 0
    roe = roe * 100 if roe else 0
    roic = roe * 0.7
    margem = info.get('profitMargins', 0) or 0
    margem = margem * 100 if margem else 0

    preco_justo = preco * 1.2
    upside = ((preco_justo - preco) / preco) * 100 if preco else 0

    return {
        'Ticker': ticker,
        'Preço Atual': round(preco, 2),
        'Preço Justo': round(preco_justo, 2),
        'Upside (%)': round(upside, 2),
        'P/L': round(pl, 2),
        'DY (%)': round(dy, 2),
        'ROE (%)': round(roe, 2),
        'ROIC (%)': round(roic, 2),
        'Margem Líquida (%)': round(margem, 2),
    }
