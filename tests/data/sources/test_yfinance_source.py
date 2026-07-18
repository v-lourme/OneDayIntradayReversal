from src.data.sources.yfinance_source import YahooFinanceSource

source = YahooFinanceSource()

price = source.get_price(["NVDA"], "2016-01-01", "2026-06-30")

print(price.head())
