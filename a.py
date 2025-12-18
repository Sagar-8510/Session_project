l1 = [1, 2]

k, _ = l1
print(k)


import redis

r = redis.Redis(host="127.0.0.1", port=6379, decode_responses=True)

# ===========String===============
r.setex("session:abc", 300, "afjsdf")
print(r.get("session:abc"))


# ==========Set=============
s = r.sadd("car", "abc", "av")
s = r.srem("car", "av")

# 1 if the value is a member of the set.
# 0 if the value is not a member of the set or if key does not exist.
print(f"Set size-->{r.scard("car")}")
print(f"Member of set-->{r.sismember("car","adg")}")
print()


# ==========List==============
# r.lpush("car:repaire","pqr")
l = r.rpush("car:repaire", "ab")
l=r.lpop("car:repaire")
print(f"{r.lrange("car:repaire",0,-1)}")
print(f"Lenght of list--->>{r.llen("car:repaire")}")
print(f"{r.ltrim("car:repaire",0,9)}")
# r.blpop("car:repaire")


# ==========Hash===========
r.hset("student", mapping={"name": "sagar", "mobile": 123})
print(r.hget("student", "name"))
print(r.hmget("student", "name","mobile"))
