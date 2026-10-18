from dotenv import load_dotenv
import os
from web3 import AsyncWeb3
import asyncio
load_dotenv()

WSS_URL = os.getenv("WSS_URL")

BASE_FACTORY_V3 = "0x33128a8fc17869897dce68ed026d694621f6fdfd"
wss_url_eth = f"wss://eth-mainnet.g.alchemy.com/v2/{WSS_URL}"
wss_url_base = f"wss://base-mainnet.g.alchemy.com/v2/{WSS_URL}"
WETH_ADDRESS = "0x4200000000000000000000000000000000000006"
async def get_logs():
    w3 = AsyncWeb3(AsyncWeb3.WebSocketProvider(wss_url_base))

    async with w3:
        sub_id = await w3.eth.subscribe(
            "logs",
            {"address": w3.to_checksum_address(WETH_ADDRESS)}
        )

        print(f"подписка оформлена: {sub_id}")
        print("Ожидаем логи блокчейна")
        
        async for payload in w3.socket.process_subscriptions():
            print("-----------------")
            print(payload)

def run():
    try:
        asyncio.run(get_logs())
    except KeyboardInterrupt:
        print("\nВыход")

run()
