
import time
import logging
from tradingbot.exchange import Exchange

# Documentation:
# https://help.ftx.com/hc/en-us/articles/360031896592-Advanced-Order-Types

# A logger for this file
log = logging.getLogger(__name__)

class Order():
    def __init__(self,**kwargs) -> None:

        self.market     = kwargs.get('market')
        self.side       = kwargs.get('side') 
        self.size       = kwargs.get('size') 
        self.price      = kwargs.get('price') 
        self.order_id   = None 
        self.exchange   = kwargs.get('exchange') 
        
        client_id = int(time.time() * 1000) 
        self.client_id = client_id
        self.place_order()
        
        
    def place_order(self):
        self.order_info = self.exchange.make_order(self.market,self.side,self.price,self.size,self.client_id)
        self.order_id = self.order_info['id']
        self.dateCreationOrder = self.order_info['createdAt']
        log.info(f"Created order: {self.order_info}") 

    def modify_order(self,market=None,side=None,price=None,size=None,client_id=None):
        pass 

    def cancel_order(self):
        if not self.order_id is None:
            self.exchange.cancel_order(self.order_id)
            log.info(f"Cancelled order: {self.order_info}") 

    def help(self):
        return "This is a Limit Order"

    def send_notification(self):
        pass 

    def store_order(self):
        pass

class MarketOrder(Order):
    def __init__(self,**kwargs) -> None:
        super().__init__(**kwargs)

    def place_order(self):
        self.order_info = self.exchange.make_order(self.market,self.side,self.price,self.size,type="market")
        self.order_id = self.order_info['id']
        self.dateCreationOrder = self.order_info['createdAt']
        log.info(f"Created order: {self.order_info}") 


#Stop-loss buy orders are sent when the market price exceeds their trigger price. Stop-loss sell orders are sent when the market price drops below their trigger price."
class stopLossLimit(Order):
    #orderPrice:	optional; order type is limit if this is specified; otherwise market
    def __init__(self,**kwargs) -> None:
        self.orderPrice = kwargs.get('orderPrice')
        super().__init__(**kwargs)
        

    def help(self):
        return "Stop-loss buy orders are sent when the market price exceeds their trigger price. Stop-loss sell orders are sent when the market price drops below their trigger price."

    def place_order(self):
        self.order_info = self.exchange.place_conditional_order(self.market,self.side,self.price,self.size,type="stop",orderPrice=self.orderPrice)
        self.order_id = self.order_info['id']
        self.dateCreationOrder = self.order_info['createdAt']
        log.info(f"Created order: {self.order_info}") 

#Take-profit if you are buying, the order will get sent when the market price drops below your trigger price. If you are selling, the order will get sent when the market price exceeds above your trigger price.
class TakeProfitLimit(Order):
    def __init__(self,market,side,price,size,client_id=None) -> None:
        super().__init__()

    def help(self):
        return "Take-Profit buy orders are sent when the market price drop below your trigger price. Take-Profit sell orders are sent when the market price exceeds above your trigger price."

    def place_order(self):
        self.order_info = self.exchange.place_conditional_order(self.market,self.side,self.price,self.size,type="take_profit",orderPrice=self.orderPrice)
        self.order_id = self.order_info['id']
        self.dateCreationOrder = self.order_info['createdAt']
        log.info(f"Created order: {self.order_info}") 

    




