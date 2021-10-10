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


def get_reserved_room_num(user_id: str) -> Optional[int]:
    """
    予約が存在するかの確認

    Args:
        user_id(str): LINEのユーザーID

    Returns:
        int or None: 予約が行われていた場合は学習室番号
    """
    reservations_ref = db.collection('reservations').document(user_id).get()
    if reservations_ref.exists:
        data = reservations_ref.to_dict()
        return data['room_num']


def reserve_notice(user_id: str, room_num: int) -> datetime:
    """
    空席通知予約

    Args:
        user_id(str): LINEのユーザーID
        room_num(int): room_num: 学習室番号（const.pyを参照）

    Returns:
        datetime: 予約時間
    """
    now = datetime.now(jst)
    reservations_ref = db.collection('reservations').document(user_id)
    data = {'reservation_time': now, 'room_num': room_num}
    reservations_ref.set(data)
    return now
