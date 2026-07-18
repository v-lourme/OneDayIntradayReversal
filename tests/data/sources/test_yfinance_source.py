from src.data.sources.yfinance_source import YahooFinanceSource

def test_YahooFinanceSource() -> None:

    source = YahooFinanceSource()
    price = source.get_price(["NVDA", "AMD"], "2016-01-01", "2026-06-30")

    assert not price.empty
    assert list(price.columns) == ["Date", "Ticker", "Close", "High", "Low", "Open", "Volume"]

