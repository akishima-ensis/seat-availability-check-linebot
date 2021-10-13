from typing import Union

from linebot.models import (
    TextSendMessage,
    FlexSendMessage
)

from src.firebase import (
    get_rooms_data,
    get_reserved_room_num,
    reserve_notice
)
from src.flex_message_template import (
    room_info_message,
    done_reservation_message,
    confirm_new_reservation_message,
    closing_day_message,
    failed_to_get_data_message,
    usage_message
)
from src.const import (
    ROOM_NAME_MESSAGES,
    ROOM_RESERVATION_MESSAGES,
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
    if message in ROOM_NAME_MESSAGES.keys():
        reply_content = create_room_info_message(ROOM_NAME_MESSAGES[message])

    # 空席通知予約
    elif message in ROOM_RESERVATION_MESSAGES.keys():
        room_num = ROOM_RESERVATION_MESSAGES[message]
        reply_content = create_reserve_notice_message(user_id, room_num)

    # 空席通知新規予約（既に予約済みだった場合新規の予約で上書きする）
    elif message in ROOM_NEW_RESERVATION_MESSAGES.keys():
        room_num = ROOM_NEW_RESERVATION_MESSAGES[message]
        reply_content = create_reserve_notice_message(user_id, room_num, new=True)

    # 予期しないメッセージへの対応
    else:
        reply_content = usage_message()

    return reply_content


def create_room_info_message(room_num: int) -> FlexSendMessage:
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
            return room_info_message(room_data, rooms_data['update'])
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
                # 新規予約（現在の予約を上書きして予約）
                if new:
                    reserved_time = reserve_notice(user_id, room_num)
                    return done_reservation_message(room_name, reserved_time)
                # 予約
                else:
                    reserved_room_num = get_reserved_room_num(user_id)
                    # 予約されていなかったら
                    if not reserved_room_num:
                        reserved_time = reserve_notice(user_id, room_num)
                        return done_reservation_message(room_name, reserved_time)
                    # 既に予約されていたら新規予約のメッセージテンプレートを返す
                    else:
                        reserved_room_name = [k for k, v in ROOM_NAME_MESSAGES.items() if v == reserved_room_num][0]
                        return confirm_new_reservation_message(reserved_room_name, room_data['name'])
            else:
                return TextSendMessage(text=f'{room_name}は空席があります。')
        else:
            return failed_to_get_data_message()
    else:
        return closing_day_message()
