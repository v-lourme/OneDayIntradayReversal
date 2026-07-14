import yfinance as yf
import pandas as pd

class YahooFinanceSource:

    """ Download and normalize daily OHLCV data from yfinance. """

    def _download(self, tickers: list[str], start: str, end: str) -> pd.DataFrame:
        prices = yf.download(tickers, start=start, end=end, auto_adjust=True)
        return prices
    
    def _validate_structure(self, prices: pd.DataFrame) -> None:
        if not isinstance(prices, pd.DataFrame):
            raise TypeError("Data structure is no longer a dataframe")
        
        if not isinstance(prices.columns, pd.MultiIndex):
            raise TypeError("DataFrame has no multi-index")
        
        if not "Ticker" in prices.columns.names:
            raise ValueError("Ticker is no longer present as a column")
    
    def _normalize(self, prices: pd.DataFrame) -> pd.DataFrame:
        return prices.stack(level="Ticker").reset_index()
    
    def _validate_request(self, tickers: list[str], prices: pd.DataFrame) -> None:

        if prices.empty:
            raise ValueError("Empty DataFrame")
        
        if not all([ticker in prices["Ticker"].unique() for ticker in tickers]):
            raise ValueError("one or more ticker cannot be retreived")
        

    
    def get_price(self, tickers: list[str], start: str, end: str) -> pd.DataFrame:
        raw_price = self._download(tickers, start, end)
        self._validate_structure(raw_price)
        standard_price = self._normalize(raw_price)
        self._validate_request(tickers, standard_price)
        return standard_price
    

