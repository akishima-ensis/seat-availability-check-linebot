from linebot.models import TextSendMessage
from src.models import (
    get_rooms_data, check_reserve_notice, reserve_notice
)
from src.flex_message_template import (
    seats_info_message,  done_reservation_message, confirm_new_reservation_message,
    closing_day_message, failed_to_get_data_message, typing_failed_message
)


def crete_seats_info_message(room_name):
    if rooms_data := get_rooms_data():
        if not rooms_data['status']:
            return failed_to_get_data_message()
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                return seats_info_message(room_data, rooms_data['update'])
    else:
        return closing_day_message()


def create_reserve_notice_message(room_name, user_id):
    if rooms_data := get_rooms_data():
        if not rooms_data['status']:
            return failed_to_get_data_message()
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                if room_data['seats_num'] == 0:
                    is_reserved = check_reserve_notice(user_id)
                    if is_reserved['reserved']:
                        return confirm_new_reservation_message(is_reserved['name'], room_name)
                    else:
                        reserve_time = reserve_notice(user_id, room_name)
                        notice_time = f'{str(reserve_time.hour).zfill(2)}:{str(reserve_time.minute).zfill(2)}'
                        return done_reservation_message(room_name, notice_time)
                else:
                    return TextSendMessage(text=f'{room_name}は空席があります。')
    else:
        return closing_day_message()


def create_new_reserve_notice_message(room_name, user_id):
    if rooms_data := get_rooms_data():
        if not rooms_data['status']:
            return failed_to_get_data_message()
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                if room_data['seats_num'] == 0:
                    reserve_time = reserve_notice(user_id, room_name)
                    notice_time = f'{str(reserve_time.hour).zfill(2)}:{str(reserve_time.minute).zfill(2)}'
                    return done_reservation_message(room_name, notice_time)
                else:
                    return TextSendMessage(text=f'{room_name}は空席があります。')
    else:
        return closing_day_message()


def create_failure_message():
    return typing_failed_message()