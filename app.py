from ibapi.wrapper import EWrapper
from ibapi.client import EClient

from ibapi.contract import Contract
from ibapi.ticktype import TickTypeEnum
from ibapi.order import *
import threading
import time

class IBapi(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)

    def error(self, reqId, errorCode, errorString):
    	print("Error: ", reqId, " ", errorCode, " ", errorString)

    def tickPrice(self, reqId, tickType, price, attrib):
    	print("Tick Price. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Price:", price, end=' ')

    def tickSize(self, reqId, tickType, size):
    	print("Tick Size. Ticker Id:", reqId, "tickType:", TickTypeEnum.to_str(tickType), "Size:", size)

    def realTimeBar(self, reqId, time, open_, high, low, close, volume, wap, count):
        bot.on_bar_update(reqId, time, open_, high, low, close, volume, wap, count)

class Bot():
	ib = None
	contract = None
	symbol = ""

	def __init__(self):
		self.ib = IBapi()
		self.ib.connect("127.0.0.1", 4001, 0)

		ib_thread = threading.Thread(target=self.run_loop, daemon=True)
		ib_thread.start()
		time.sleep(1)

		self.symbol = input("Enter symbol to observe:")

		self.contract = Contract()
		self.contract.secType = "STK"
		self.contract.exchange = "SMART"
		self.contract.currency = "USD"
		self.contract.primaryExchange = "NASDAQ"
		self.contract.symbol = self.symbol.upper()

		self.ib.reqMarketDataType(4) #delayed frozen data
		self.ib.reqMktData(1, self.contract, "", False, False, [])
		#self.ib.reqRealTimeBars(0, self.contract, 5, "TRADES", 1, [])

		time.sleep(5)
		self.ib.disconnect()

	def run_loop(self):
		self.ib.run()

	def on_bar_update(self, reqId, time, open_, high, low, close, volume, wap, count):
		print(close)

def main():

	bot = Bot()

	"""
	app = IBapi()
	app.connect("127.0.0.1", 4001, 0)

	contract = Contract()
	contract.symbol = "AAPL"
	contract.secType = "STK"
	contract.exchange = "SMART"
	contract.currency = "USD"
	contract.primaryExchange = "NASDAQ"

	app.reqMarketDataType(4) #delayed frozen data
	app.reqMktData(1, contract, "", False, False, [])

	app.run()
	app.close()
	"""

if __name__ == "__main__":
	main()
