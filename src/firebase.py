from src import db
from datetime import datetime, timedelta, timezone


def get_time():
    jst = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(jst)


def get_rooms_data():
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


def check_reserve_notice(user_id):
    user_ref = db.collection('users').document(user_id).get()
    if user_ref.exists:
        data = user_ref.to_dict()
        if data['reserved']:
            return {'reserved': True, 'name': data['room_name']}
        else:
            return {'reserved': False}
    else:
        return {'reserved': False}


def reserve_notice(user_id, room_name):
    now = get_time()
    users_ref = db.collection('users').document(user_id)
    data = {
        'reserve_time': now,
        'reserved': True,
        'room_name': room_name
    }
    if users_ref.get().exists:
        users_ref.update(data)
    else:
        users_ref.set(data)
    return now