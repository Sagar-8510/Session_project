from fastapi import HTTPException
from v1.models import User
from passlib.hash import bcrypt
from .sessions import create_session
from v1.config import r


def create_user(user):
    try:
        if User.objects(email=user.email).first():
            print(user.password)
            raise HTTPException(status_code=400,detail="User is already registered")

        hash_pass=bcrypt.hash(user.password)
        User(
            name=user.name,
            email=user.email,
            password=hash_pass,
            max_login=user.max_login,
        ).save()
        
        return {"Message":"User registred"}
    
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")


def login_user(email,password,response):
    try:
        user=User.objects(email=email).first()
        if not user:
            raise HTTPException(status_code=404,detail="User not found")

        if not bcrypt.verify(password,user.password):
            raise HTTPException(status_code=400,detail="Password is incorrect")

        session_id=create_session(user_id=str(user.id))

        count_key = f"user_sessions:{user.id}"

        sessions = r.incr(count_key)
        r.expire(count_key, 300)

        if sessions > user.max_login:
            r.decr(count_key)
            raise HTTPException(401, f"Login limit {user.max_login} reached")

        # Send session to frontend via cookie
        response.set_cookie(
            key="session_id",
            value=session_id, 
            httponly=True,
            samesite="lax",
            max_age=300
        )

        return {"Message":"Logged in"}

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")
