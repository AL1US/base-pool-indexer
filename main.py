import asyncio
import os
from web3 import AsyncWeb3

WSS_URL = os.getenv("WSS_URL")

BASE_FACTORY_V3 = "0x33128a8fc17869897dce68ed026d694621f6fdfd"
wss_url_base = f"wss://base-mainnet.g.alchemy.com/v2/{WSS_URL}"
RPC_URL = "https://mainnet.base.org"
POOL_ADDR = "0x83f3aca29bc79b048b99c56013475570acc97ccf"

# Минимальный ABI для чтения переменных token0 и token1
MINIMAL_POOL_ABI = [
    {"inputs": [], "name": "token0", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "token1", "outputs": [{"type": "address"}], "stateMutability": "view", "type": "function"},
]

async def get_tokens():
    w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(RPC_URL))
    pool = w3.eth.contract(address=w3.to_checksum_address(POOL_ADDR), abi=MINIMAL_POOL_ABI)
    
    t0 = await pool.functions.token0().call()
    t1 = await pool.functions.token1().call()
    print(f"Token0: {t0}")
    print(f"Token1: {t1}")

asyncio.run(get_tokens())

