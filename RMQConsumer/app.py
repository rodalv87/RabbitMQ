import asyncio
import aio_pika

async def main(exchange_name) -> None:
    # Perform connection
    connection = await aio_pika.connect("amqp://guest:guest@localhost/")
    async with connection:
        # Creating a channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(exchange_name, durable=True)

        # Start listening the queue with name 'hello'
        await queue.consume(on_message, no_ack=False)

        print(" [*] Waiting for messages. To exit press CTRL+C")
        await asyncio.Future()

async def on_message():
    pass

if __name__ == "__main__":
    asyncio.run(main('TestExchange'))
