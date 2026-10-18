from dotenv import load_dotenv
from web3 import AsyncWeb3, Web3
import asyncio
import os


load_dotenv()

WSS_URL = os.getenv("WSS_URL")

TOKEN = "0x3E5C020B3Ed038309b5AB18499997fdE3b5130E5"
def decode_data(data: dict) -> dict:
    pass

async def get_logs():
    w3 = AsyncWeb3(AsyncWeb3.WebSocketProvider(f"https://base-mainnet.g.alchemy.com/v2/{WSS_URL}"))

    async with w3:
        # subscibe on logs
        w3.eth.subscribe(
                "logs",
                {
                    "address": w3.to_checksum_address(TOKEN),
                    "topics": []
                    }
                ) 
        
