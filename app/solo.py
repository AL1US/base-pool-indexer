from dotenv import load_dotenv
from web3 import AsyncWeb3, Web3
import asyncio
import os


load_dotenv()

WSS_URL = os.getenv("WSS_URL")

TOKEN = "0x29cC30f9D113B356Ce408667aa6433589CeCBDcA"
TOPIC_TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"
def decode_data(data: dict) -> dict:
    pass

async def get_logs():
    w3 = AsyncWeb3(AsyncWeb3.WebSocketProvider(f"wss://base-mainnet.g.alchemy.com/v2/{WSS_URL}"))

    async with w3:
        # subscibe on logs
        sub_id = await w3.eth.subscribe(
                "logs",
                {
                    "address": w3.to_checksum_address(TOKEN),
                    "topics": [TOPIC_TRANSFER]
                    }
                ) 
        print(f"получен sub_id: {sub_id}")
        print("Ожидание данных")
        async for payload in w3.socket.process_subscriptions():
            print(payload)
            print("-" * 50)

asyncio.run(get_logs())
