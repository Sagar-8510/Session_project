import os
import redis

from dotenv import load_dotenv
from mongoengine import connect

load_dotenv()

# =======MongoDB==============
db_url = os.getenv("DATABASE_URL")

conn = connect(db="userdb",host=db_url)
# print(conn)

# ========Redis===============

r=redis.Redis(host="127.0.0.1",port=6379,decode_responses=True)
