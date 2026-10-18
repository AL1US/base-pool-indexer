- Для начала нам нужно найти RPC api для подключения к блокчейну. Для этого воспользуемся такими сайтами как:
    - https://www.alchemy.com/
- во вкладке endpoints выбираем сеть, главное не светите своим api ключем
- теперь, если у вас сеть eth, или l2 сеть от эфира, то вы можете воспользоваться web3
- Можем воспользоваться любой платформой для анализа блкочейна, я буду использовать https://dexscreener.com
- Выбираем любую торговую пару или токен, который будем отслеживать, зайти на него справа вы увидете меню с данными, от туда нужно скопировать адрес контракта
- после того как мы получили адрес контракта нам необходимо узнать что именно мы будем отслеживать, например все переводы
- После этого нужно получить сигнатуру события, а чтобы её получить нужно сначала найти функцию (или вспомнить из чего она состоит)
- заходим на https://basescan.org и вбиваем туда адрес токена, после чего переходим во вкладку contract и ищем нашу функцию, нам потребуются только название и параметры
оно будет выглядеть примерно таким образом
```solidity
PoolCreated(address,address,uint24,int24,address)
Transfer(address,address,uint256)
```
Далее необходимо сделать хэширование сигнатуры события, для того чтобы по этому хэшу в дальнейшем искать наши события
```python
python -c 'from web3 import Web3; print(Web3.keccak(text="PoolCreated(address,address,uint24,int24,address)").hex())'
```

Далее оформляем подписку на логи, сначала более простой пример, затем более сложной
```python

async with w3: sub_id = await w3.eth.subscribe(
            "logs",
            {
            "address": w3.to_checksum_address(WETH_ADDRESS), # сюда указываем контракт который мы слушаем
            "topics": [TOPIC_TRANSFER] # сюда сигнатуру
            },
        )

await w3.subscription_manager.subscribe(
    [
        NewHeadsSubscription(
            label="new-heads-mainnet",
            handler=new_heads_handler
        ),
        LogsSubscription(
            label="WETH transfers",
            address=w3.to_checksum_address(
                "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
            ),
            topics=["0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"],
            handler=log_handler,
        ),
    ]

```
Когда мы вызвали эту строчку, Python отправил в открытый сокет JSON-RPC сообщение, нода прочитала это и повесила у себя в памяти тригер на этот фильтр и ответила обратно в сокет

Далее получаем данные
```python
async for payload in w3.socket.process_subscriptions():
    result = payload.get("result")
    if not result or len(result.get("topics", [])) < 3:
        continue
    
    print(payload)
```
Эти данные сырые и поэтому нам нужно написать декодер
```python
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

```


