import os
from dotenv import load_dotenv

load_dotenv(override=True)
LOCAL_BASE_URL = os.getenv("LOCAL_BASE_URL")

OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

ZHIPU_API_KEY=os.getenv("ZHIPU_API_KEY")
ZHIPU_BASE_URL=os.getenv("ZHIPU_BASE_URL")
