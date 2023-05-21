import asyncio
import aio_pika
import aio_pika.abc
import json

async def main(loop, exchange_name, message):
    # Explicit type annotation
    connection: aio_pika.RobustConnection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost:5672/", loop=loop
    )

    routing_key = exchange_name
    channel: aio_pika.abc.AbstractChannel = await connection.channel()    
    exchange = await channel.declare_exchange(exchange_name)
    
    ready_queue = await channel.declare_queue(
                routing_key, durable=True
            )
    await ready_queue.bind(exchange, routing_key)
    
    await exchange.publish(
        aio_pika.Message(
            body=json.dumps({'message': message}).encode()
        ),
        routing_key=routing_key
    )

    await connection.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    asyncio.gather(
        *[loop.run_until_complete(main(loop, 'TestExchange', 'Hello this is a new message')) for _ in range(10000)]
    )

    # loop = asyncio.get_event_loop()
    # for _ in range(10000): loop.run_until_complete(main(loop, 'TestExchange', 'Hello this is a new message'))
    # loop.close()