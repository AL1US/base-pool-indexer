from dotenv import load_dotenv
import os
from web3 import AsyncWeb3, Web3
import asyncio
load_dotenv()

WSS_URL = os.getenv("WSS_URL")

BASE_FACTORY_V3 = "0x33128a8fc17869897dce68ed026d694621f6fdfd"
wss_url_eth = f"wss://eth-mainnet.g.alchemy.com/v2/{WSS_URL}"
wss_url_base = f"wss://base-mainnet.g.alchemy.com/v2/{WSS_URL}"
WETH_ADDRESS = "0x4200000000000000000000000000000000000006"
TOPIC_TRANSFER = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

def decode_transfer_log(result: dict) -> dict:
    topics = result["topics"]
    data = result["data"]


    # topics[1] и topics[2] — объекты HexBytes, берем последние 20 байт
    sender = Web3.to_checksum_address(topics[1][-20:].hex())
    recipient = Web3.to_checksum_address(topics[2][-20:].hex())

    # raw_data — это HexBytes, переводим напрямую в int
    amount_wei = int.from_bytes(data, byteorder="big")
    amount_eth = amount_wei / 10**18

    return {
            "block": result.get("blockNumber"),
            "tx_hash": result.get("transactionHash").hex(),
            "from": sender,
            "to": recipient,
            "amount_wei": amount_wei,
            "amount_eth": amount_eth,
        }

async def get_logs():
    w3 = AsyncWeb3(AsyncWeb3.WebSocketProvider(wss_url_base))

    async with w3:
        sub_id = await w3.eth.subscribe(
            "logs",
            {
                "address": w3.to_checksum_address(WETH_ADDRESS), # сюда указываем контракт который мы слушаем
                "topics": [TOPIC_TRANSFER] # сюда сигнатуру
            },

        )

        print(f"подписка оформлена: {sub_id}")
        print("Ожидаем логи блокчейна")

        async for payload in w3.socket.process_subscriptions():
            result = payload.get("result")
            if not result or len(result.get("topics", [])) < 3:
                continue
            
            event = decode_transfer_log(result)

            print(f"[Блок {event['block']}] Tx: {event['tx_hash'][:10]}...")
            print(f"  От:    {event['from']}")
            print(f"  Кому:  {event['to']}")
            print(f"  Сумма: {event['amount_eth']:.5f} WETH ({event['amount_wei']} wei)")
            print("-" * 50)

if __name__ == "__main__":
    try:
        asyncio.run(get_logs())
    except KeyboardInterrupt:
        print("\nОстановлено пользователем.")
