from dotenv import load_dotenv
import os

load_dotenv()

QUEUE_JOB = os.getenv("QUEUE_JOB")
QUEUE_RESULT = os.getenv("QUEUE_RESULT")

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_USERNAME = os.getenv("REDIS_USERNAME")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

REDIS_PREDIX = os.getenv("REDIS_PREDIX")

DASHSCOPE_URL = os.getenv("DASHSCOPE_URL")
DASHSCOPE_API = os.getenv("DASHSCOPE_API")

BASE_URL = os.getenv("BASE_URL")
BASE_API = os.getenv("BASE_API")