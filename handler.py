import asyncio

from logic import Logic
from bullmq import Worker, Queue

from config import QUEUE_JOB, QUEUE_RESULT, REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD, REDIS_PREFIX

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
        
        #
        
        _usage = {}
        
        for u in usage:
            
            if u[0] not in _usage.keys(): _usage[u[0]] = {"input": 0, "output": 0}
            
            _usage[u[0]]["input"] += int(u[1])
            _usage[u[0]]["output"] += int(u[2])
        #
        
        result["usage"] = _usage
        
        #
        
        results.append(result)
    #

    response = {
        "fbAdId": data["fbAdId"],
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
        QUEUE_RESULT,
        {
            "prefix": REDIS_PREFIX,
            "connection": {
                "host": REDIS_HOST,
                "port": REDIS_PORT,
                "username": REDIS_USERNAME,
                "password": REDIS_PASSWORD
            }
        }
    )
    
    worker = Worker(
        QUEUE_JOB,
        processor,
        {
            "prefix": REDIS_PREFIX,
            "connection": {
                "host": REDIS_HOST,
                "port": REDIS_PORT,
                "username": REDIS_USERNAME,
                "password": REDIS_PASSWORD
            }
        }
    )

    print("Worker started")

    await asyncio.Future()
#

if __name__ == "__main__":

    asyncio.run(main())