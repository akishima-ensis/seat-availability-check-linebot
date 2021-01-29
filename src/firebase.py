from typing import Dict, Union
from datetime import datetime, timedelta, timezone

from src import db


def get_time() -> datetime:
    """
    現在時刻の取得（JST）
    Returns:
        datetime
    """
    jst = timezone(timedelta(hours=+9), 'JST')
    return datetime.now(jst)


def get_rooms_data() -> Dict:
    """
    最新の空席情報の取得

    Returns:
        dict: 空席情報
    """
    now = get_time()
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H%M')
    rooms_ref = db.collection('rooms').document(date).get()
    rooms_data = None
    if rooms_ref.exists:
        rooms_data = rooms_ref.to_dict().get(time)
        if not rooms_data:
            before = (now - timedelta(minutes=1)).strftime('%H%M')
            rooms_data = rooms_ref.to_dict().get(before)
    return rooms_data


def get_reserved_room(user_id: str) -> Union[str, None]:
    """
    予約が存在するかの確認

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        dict:
    """
    user_ref = db.collection('users').document(user_id).get()
    if user_ref.exists:
        data = user_ref.to_dict()
        if data['reserved']:
            return data['room_name']


def reserve_notice(user_id: str, room_name: str) -> datetime:
    """
    空席通知予約

    Args:
        user_id(str): LINEのユーザーID
        room_name(str): 学習室名

    Returns:
        datetime: 予約時間
    """
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
