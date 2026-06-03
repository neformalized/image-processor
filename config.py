from dotenv import load_dotenv
import os

load_dotenv()

WORKERS = os.getenv("WORKERS")

QUEUE_JOB = os.getenv("QUEUE_JOB")
QUEUE_RESULT = os.getenv("QUEUE_RESULT")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS_PREFIX = os.getenv("REDIS_PREFIX")

DASHSCOPE_API = os.getenv("DASHSCOPE_API")

DASHSCOPE_URL = os.getenv("DASHSCOPE_URL")
DASHSCOPE_BASE_URL = os.getenv("DASHSCOPE_BASE_URL")