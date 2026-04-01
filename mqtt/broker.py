import asyncio
from hbmqtt.broker import Broker

broker_config = {
    "listeners": {
        "default": {
            "type": "tcp",
            "bind": "0.0.0.0:1883"
        }
    },
    "sys_interval": 10,
    "topic-check": {
        "enabled": False
    }
}


async def start_broker():
    broker = Broker(broker_config)
    await broker.start()


if __name__ == "__main__":
    asyncio.run(start_broker())
