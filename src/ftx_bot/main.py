import hydra
from omegaconf import DictConfig,OmegaConf
from hydra.utils import get_original_cwd
from clients.ftx_client import FtxClient
from exchange import Exchange


@hydra.main(version_base=None, config_path='../../parameters', config_name='my_conf.yaml')
def metodo(cfg: DictConfig):
    client = FtxClient(cfg.ftx_client['key'],cfg.ftx_client['secret'],cfg.ftx_client['subaccount_name'])
    exchange = Exchange(client)
    

    import time
    ts = int(time.time() * 1000) 
    #r = exchange.make_order(market="USDT/USD",side="buy",price=0.90,size=1,client_id=str(ts))
    #print(r)
    #print("stampa prima: ", exchange.get_all_open_orders())
    #print(r)
    exchange.cancel_order(148396000502)
    print("stampa dopo: ", exchange.get_all_open_orders())
    #print(exchange.get_open_order("139563598672"))
    
    #wallet = exchange.get_sub_wallet('gold')
    #print("solo gold: \n", wallet)

    

if __name__ == "__main__":
    metodo()