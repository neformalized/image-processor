import asyncio, multiprocessing, signal, argparse

from logic import Logic
from bullmq import Worker, Queue

from config import QUEUE_JOB, QUEUE_RESULT, REDIS_HOST, REDIS_PORT, REDIS_USERNAME, REDIS_PASSWORD, REDIS_PREFIX

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
        "fbAdId": data["fbAdId"],
        "snapshotId": data["snapshotId"],
        "analisysVersion": "v0.1",
        "items": results
    }
    
    await response_queue.add(
        job.name,
        response
    )
    
    print(f"{multiprocessing.current_process().name} finish job:{job.name}")
    
    return {
        "status": "ok"
    }
#

async def main():
    
    global response_queue, master
    
    shutdown_event = asyncio.Event()
    
    def signal_handler(signum, frame):
        
        print(f"{multiprocessing.current_process().name} received signal {signum}")
        shutdown_event.set()
    #
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    #
    
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
    
    #
    
    try:

        await shutdown_event.wait()

        print(f"{multiprocessing.current_process().name} stopping gracefully...")
    #
    finally:

        try:
            
            await worker.close()
            
            print(f"{multiprocessing.current_process().name} worker closed")
        #
        except Exception as e:
            print(f"worker close error: {e}")
        #
        
        try:
            
            await response_queue.close()
            
            print(f"{multiprocessing.current_process().name} queue closed")
        #
        except Exception as e:
            print(f"queue close error: {e}")
        #
        
        print(f"{multiprocessing.current_process().name} stopped")
    #
#

def run_worker():

    try:
        asyncio.run(main())
    #
    except KeyboardInterrupt:
        pass
    #
#

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--workers", type=int, default=100)
    args = parser.parse_args()
    
    multiprocessing.set_start_method("spawn", force=True)
    
    processes = []

    try:

        for i in range(args.workers):

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
    #
    except KeyboardInterrupt:

        print("Main process received Ctrl+C")

        for p in processes:
            p.join()
        #
    #
#