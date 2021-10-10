from typing import Union
from linebot.models import TextSendMessage, FlexSendMessage

from src.firebase import (get_rooms_data, get_reserved_room_num, reserve_notice)
from src.flex_message_template import (
    seats_info_message,  done_reservation_message, confirm_new_reservation_message,
    closing_day_message, failed_to_get_data_message, usage_message
)
from src.const import (
    ROOM_NAME_MESSAGES,
    ROOM_NAME_MESSAGES_LIST,
    ROOM_RESERVATION_MESSAGES,
    ROOM_RESERVATION_MESSAGES_LIST,
    ROOM_NEW_RESERVATION_MESSAGES,
    ROOM_NEW_RESERVATION_MESSAGES_LIST,
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
    elif message in ROOM_RESERVATION_MESSAGES_LIST:
        room_num = ROOM_RESERVATION_MESSAGES[message]
        reply_content = create_reserve_notice_message(user_id, room_num)

    # 空席通知新規予約（既に予約済みだった場合新規の予約で上書きする）
    elif message in ROOM_NEW_RESERVATION_MESSAGES_LIST:
        room_num = ROOM_NEW_RESERVATION_MESSAGES[message]
        reply_content = create_reserve_notice_message(user_id, room_num, new=True)

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


def create_reserve_notice_message(user_id: str, room_num: int, new: bool = False) -> Union[FlexSendMessage, TextSendMessage]:
    """
    空席通知予約に関するメッセージの生成

    Args:
        user_id: LINEのユーザーID
        room_num: 学習室番号（const.pyを参照）
        new(bool): 新規通知予約かどうか

    Returns:
        FlexSendMessage or TextSendMessage
    """
    rooms_data = get_rooms_data()
    if rooms_data:
        if rooms_data['status']:
            room_data = rooms_data['data'][room_num]
            room_name = room_data['name']
            if room_data['seats_num'] == 0:
                if new:
                    reserved_time = reserve_notice(user_id, room_num)
                    notice_time = f'{str(reserved_time.hour).zfill(2)}:{str(reserved_time.minute).zfill(2)}'
                    return done_reservation_message(room_name, notice_time)
                else:
                    reserved_room_num = get_reserved_room_num(user_id)
                    if not reserved_room_num:
                        reserved_time = reserve_notice(user_id, room_num)
                        notice_time = f'{str(reserved_time.hour).zfill(2)}:{str(reserved_time.minute).zfill(2)}'
                        return done_reservation_message(room_name, notice_time)
                    else:
                        reserved_room_name = [k for k, v in ROOM_NAME_MESSAGES.items() if v == reserved_room_num][0]
                        return confirm_new_reservation_message(reserved_room_name, room_data['name'])
            else:
                return TextSendMessage(text=f'{room_name}は空席があります。')
        else:
            return failed_to_get_data_message()
    else:
        return closing_day_message()
