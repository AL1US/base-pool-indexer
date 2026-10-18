from dotenv import load_dotenv
from web3 import AsyncWeb3, Web3
import asyncio
import os


load_dotenv()

WSS_URL = os.getenv("WSS_URL")

TOKEN = "0x83f3ACa29Bc79B048B99C56013475570acc97ccF"
TOPIC_TRANSFER = 0x19b47279256b2a23a1665c810c8d55a1758940ee09377d4f8d26497a3577dc83
# {
#         'subscription': '0x6b4ed6b8ad381cfe8b8517a97f62a908',
#         'result': AttributeDict({
#             'address': '0x29cC30f9D113B356Ce408667aa6433589CeCBDcA',
#             'topics': [HexBytes('0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'),
#                        HexBytes('0x00000000000000000000000083f3aca29bc79b048b99c56013475570acc97ccf'),
#                        HexBytes('0x0000000000000000000000005e4efb192dfd5a267e5bedac155fd9b79df82496')],
#             'data': HexBytes('0x000000000000000000000000000000000000000000000015601a7b4a6cffc40c'),
#             'blockHash': HexBytes('0xe460260c46c34d0f8bf0a1cb25fde8a125a231afae97521dd913804e866a198a'),
#             'blockNumber': 52782759,
#             'blockTimestamp': '0x6ad52a31',
#             'transactionHash': HexBytes('0xc033a79677a1914d0b16a62e26a08e9956f34f2ec22ca0cf1c188b05a
def decode_data(result: dict) -> dict:
    topics = result["topics"]
    data = result["data"]

    sender = Web3.to_checksum_address(topics[1][-20:].hex())
    recipient = Web3.to_checksum_address(topics[2][-20:].hex())
    
    token1 = 




# async def get_logs():
#     w3 = AsyncWeb3(AsyncWeb3.WebSocketProvider(f"wss://base-mainnet.g.alchemy.com/v2/{WSS_URL}"))
#
#     async with w3:
#         # subscibe on logs
#         sub_id = await w3.eth.subscribe(
#                 "logs",
#                 {
#                     "address": w3.to_checksum_address(TOKEN),
#                     "topics": [TOPIC_TRANSFER]
#                     }
#                 ) 
#         print(f"получен sub_id: {sub_id}")
#         print("Ожидание данных")
#         async for payload in w3.socket.process_subscriptions():
#             print(payload)
#             print("-" * 50)
#
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
