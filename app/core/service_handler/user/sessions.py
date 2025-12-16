import uuid
import json

from datetime import datetime, timedelta
from v1.config import r
from fastapi import HTTPException


def create_session(user_id):
    try:
        session_id = str(uuid.uuid4())
        userID = user_id
        expire_at = datetime.utcnow() + timedelta(minutes=5)

        session_key = f"session:{session_id}"

        session = {
            "session_id": session_id,
            "userID": userID,
            "expire_at": expire_at.isoformat(),
        }
        r.set(session_key, json.dumps(session),ex=300)

        return session_id

    except Exception as e:
        raise HTTPException(status_code=500,detail=f"{e}")


def get_session(session_id):
    session_key=f"session:{session_id}"

    session=r.get(session_key)

    return session

   
