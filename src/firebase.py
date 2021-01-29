from typing import Dict, Optional
from datetime import datetime, timedelta

from src import db, jst


def get_rooms_data() -> Optional[Dict]:
    """
    最新の空席情報の取得

    Returns:
        dict or None: 空席情報が存在した場合はdictを返す
    """
    now = datetime.now(jst)
    date = now.strftime('%Y%m%d')
    time = now.strftime('%H%M')
    rooms_ref = db.collection('rooms').document(date).get()
    if rooms_ref.exists:
        rooms_data = rooms_ref.to_dict().get(time)
        if not rooms_data:
            before = (now - timedelta(minutes=1)).strftime('%H%M')
            rooms_data = rooms_ref.to_dict().get(before)
        return rooms_data


def get_reserved_room(user_id: str) -> Optional[str]:
    """
    予約が存在するかの確認

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        dict or None: 予約が行われていた場合は学習室名を返す
    """
    users_ref = db.collection('users').document(user_id).get()
    if users_ref.exists:
        data = users_ref.to_dict()
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
    now = datetime.now(jst)
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
