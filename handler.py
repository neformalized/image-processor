import asyncio, multiprocessing

from logic import Logic
from bullmq import Worker, Queue

from config import QUEUE_JOB, QUEUE_RESULT, REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD, REDIS_PREFIX, WORKERS

master = None
response_queue = None

async def processor(job, token):
    
    global response_queue, master

    print(f"{multiprocessing.current_process().name} get job:{job.name}")
    
    data = job.data
    
    results = []
    usages = []

    for item in data["items"]:

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
        "fbAdId": "x",
        "snapshotId": data["snapshotId"],
        "analisysVersion": "v0.1",
        "items": results
    }
    
    print(f"{multiprocessing.current_process().name} finish job:{job.name}")

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

    print(f"{multiprocessing.current_process().name} started worker")

    await asyncio.Future()
#

def run_worker():
    
    asyncio.run(main())
#

if __name__ == "__main__":
    
    multiprocessing.set_start_method("spawn", force=True)
    
    processes = []

    for i in range(int(WORKERS)):
        
        p = multiprocessing.Process(
            name=f"core #{i}",
            target=run_worker
        )
        
        p.start()
        processes.append(p)
    #
    
    for p in processes:
        
        p.join()
    #