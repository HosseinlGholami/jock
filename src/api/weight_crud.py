from src.db import scales_weight, database
from datetime import datetime
from src.api.brokerConnection import BlockingRpcClient


async def getWeight(id: int):
    query = scales_weight.select().where(id == scales_weight.c.id)
    return await database.fetch_one(query=query)


async def postWeight(user_id: int, scale_id: int, scale_name: str):
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M")
    # Create an instance of the BlockingRpcClient
    rpc_client = BlockingRpcClient(
        queue_name=scale_name, recieved_topic=f".server.scale.{scale_name}", send_topic=f".scale.{scale_name}")
    try:
        # Send a request asynchronously and wait for response, with a timeout of 1 seconds
        weight = await rpc_client.get_weight("Request message", timeout=100)
    except (RuntimeError, TimeoutError) as e:
        weight = -1
        print("Error:", str(e))
    finally:
        # Close the connection
        rpc_client.close()

    query = scales_weight.insert().values(scale_id=scale_id,
                                          user_id=user_id,
                                          weight=weight,
                                          timestamp=created_date
                                          )
    return await database.execute(query=query)
