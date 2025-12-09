import os
from dotenv import load_dotenv

load_dotenv()

print("YOUTUBE:", os.getenv("YOUTUBE_API_KEY"))
print("TRENDS:", os.getenv("TRENDS_API_KEY"))
