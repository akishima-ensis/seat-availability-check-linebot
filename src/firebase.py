from src import db
from datetime import datetime, timedelta, timezone


def get_time():
    jst = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(jst)


def get_room_data():
    now = get_time()
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H%M')
    rooms_ref = db.collection('rooms').document(date).get()
    rooms = []
    if rooms_ref.exists:
        rooms = rooms_ref.to_dict().get(time)
        if not rooms:
            before = (now - timedelta(minutes=1)).strftime('%H%M')
            rooms = rooms_ref.to_dict().get(before)
    return rooms