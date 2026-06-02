import asyncio

from logic import Logic
from bullmq import Worker, Queue

master = None
response_queue = None

async def processor(job, token):
    
    global response_queue, master

    print("JOB:", job.name)
    
    data = job.data

    results = []
    usages = []

    for item in data["items"]:
        
        print("Processing item:", item["url"])

        result, usage = master.work(item["url"])
        
        #
        
        result["mediaId"] = item["mediaId"]
        results.append(result)
        
        #
        
        #usages calculations
    #

    response = {
        "fbAdId": data["fbAdId"],
        "usage": {},
        "snapshotId": data["snapshotId"],
        "analisysVersion": "v0.1",
        "items": results
    }

    await response_queue.add(
        job.name,
        response
    )

    return {
        "status": "ok"
    }
#

async def main():
    
    global response_queue, master
    
    master = Logic()
    
    response_queue = Queue(
        "INFERENCE_RESULT_QUEUE",
        {
            "prefix": "development",
            "connection": {
                "host": "208.122.212.137",
                "port": 6379,
                "username": "default",
                "password": "spyka-redis"
            }
        }
    )
    
    worker = Worker(
        "INFERENCE_QUEUE",
        processor,
        {
            "prefix": "development",
            "connection": {
                "host": "208.122.212.137",
                "port": 6379,
                "username": "default",
                "password": "spyka-redis"
            }
        }
    )

    print("Worker started")

    await asyncio.Future()
#

if __name__ == "__main__":

    asyncio.run(main())