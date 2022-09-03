import os
import time
from fastapi import APIRouter
import json
from web3 import Web3
from dotenv import load_dotenv
import threading

load_dotenv()


class setInterval:
    def __init__(self, interval, action):
        self.interval = interval
        self.action = action
        self.stopEvent = threading.Event()
        thread = threading.Thread(target=self.__setInterval)
        thread.start()

    def __setInterval(self):
        nextTime = time.time() + self.interval
        while not self.stopEvent.wait(nextTime - time.time()):
            nextTime += self.interval
            self.action()

    def cancel(self):
        self.stopEvent.set()


router = APIRouter(prefix="/blockchain", tags=["blockchain"])

@router.on_event("startup")
async def startup_event():
    web3 = Web3(Web3.HTTPProvider(os.getenv("MAINNET_RPC")))
    contract_address = os.getenv("CONTRACT_ADDRESS")
    with open("./abi.json") as abi_file:
        abi = json.load(abi_file)

    contract = web3.eth.contract(address=contract_address, abi=abi)

    def update_number_minted():
        global number_minted
        number_minted = contract.functions.totalSupply().call()

    setInterval(os.getenv("NUMBER_MINTED_UPDATE_INTERVAL"), update_number_minted)


@router.get("/number_minted")
def get_number_minted():
    try:
        resp = {"value_name": "number_minted", "value": number_minted}
    except BaseException:
        pass
        
    return resp
