import re
from typing import Union
from linebot.models import TextSendMessage, FlexSendMessage

from src import room_names
from src.firebase import (get_rooms_data, get_reserved_room, reserve_notice)
from src.flex_message_template import (
    seats_info_message,  done_reservation_message, confirm_new_reservation_message,
    closing_day_message, failed_to_get_data_message, usage_message
)
from src.const import (
    ROOM_NAME_MESSAGES,
    ROOM_NAME_MESSAGES_LIST,
    ROOM_RESERVATION_MESSAGES,
    ROOM_RESERVATION_MESSAGES_LIST,
    ROOM_NEW_RESERVATION_MESSAGES_LIST,
    ROOM_NEW_RESERVATION_MESSAGES,
)


def create_message(user_id: str, message: str) -> Union[FlexSendMessage, TextSendMessage]:
    """
    メッセージの内容に基づきクライアントの送信するメッセージの生成
    Args:
        user_id: LINEのユーザーID
        message: クライアントが送信したメッセージ

    Returns:
        FlexSendMessage or TextSendMessage
    """

    # 空席情報
    if message in ROOM_NAME_MESSAGES_LIST:
        reply_content = create_seats_info(ROOM_NAME_MESSAGES[message])

    # 空席通知予約
    elif message in [room + ' 予約' for room in room_names]:
        target_room_name = re.findall('(.+) 予約', message)[0]
        reply_content = create_reserve_notice_message(user_id, target_room_name)

    # 空席通知新規予約（既に予約済みだった場合新規の予約で上書きする）
    elif message in [room + ' 新規予約' for room in room_names]:
        target_room_name = re.findall('(.+) 新規予約', message)[0]
        reply_content = create_reserve_notice_message(user_id, target_room_name, new_reservation=True)

    # 予期しないメッセージへの対応
    else:
        reply_content = usage_message()

    return reply_content


def create_seats_info(room_num: int) -> FlexSendMessage:
    """
    現在の学習室の空席情報メッセージの生成

    Args:
        room_num: 学習室番号（const.pyを参照）

    Returns:
        FlexSendMessage
    """
    rooms_data = get_rooms_data()
    if rooms_data:
        if rooms_data['status']:
            room_data = rooms_data['data'][room_num]
            return seats_info_message(room_data, rooms_data['update'])
        return failed_to_get_data_message()
    return closing_day_message()


def create_reserve_notice_message(user_id: str, target_room_name: str, new_reservation: bool = False) -> Union[FlexSendMessage, TextSendMessage]:
    """
    空席通知予約に関するメッセージの生成

    Args:
        user_id: LINEのユーザーID
        target_room_name: 学習室名
        new_reservation(bool): 新規通知予約かどうか

    Returns:
        FlexSendMessage or TextSendMessage
    """
    rooms_data = get_rooms_data()
    if rooms_data:
        if rooms_data['status']:
            for room_data in rooms_data['data']:
                if target_room_name == room_data['name']:
                    if room_data['seats_num'] == 0:
                        if new_reservation:
                            reserved_time = reserve_notice(user_id, target_room_name)
                            notice_time = f'{str(reserved_time.hour).zfill(2)}:{str(reserved_time.minute).zfill(2)}'
                            return done_reservation_message(target_room_name, notice_time)
                        else:
                            reserved_room = get_reserved_room(user_id)
                            if not reserved_room:
                                reserved_time = reserve_notice(user_id, target_room_name)
                                notice_time = f'{str(reserved_time.hour).zfill(2)}:{str(reserved_time.minute).zfill(2)}'
                                return done_reservation_message(target_room_name, notice_time)
                            else:
                                return confirm_new_reservation_message(reserved_room, target_room_name)
                    else:
                        return TextSendMessage(text=f'{target_room_name}は空席があります。')
        else:
            return failed_to_get_data_message()
    else:
        return closing_day_message()
