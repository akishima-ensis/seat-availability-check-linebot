import datetime
from linebot.models import TextSendMessage

from src import firebase, flex_message_template


def crete_seats_info_message(room_name):
    if rooms_data := firebase.get_rooms_data():
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                return flex_message_template.seats_info_message(room_data, rooms_data['update'])
    else:
        return flex_message_template.closing_day_message()


def create_reserve_notice_message(room_name, user_id):
    if rooms_data := firebase.get_rooms_data():
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                if room_data['seats_num'] == 0:
                    is_reserved = firebase.check_reserve_notice(user_id)
                    if is_reserved['reserved']:
                        return flex_message_template.confirm_new_reservation_message(is_reserved['name'], room_name)
                    else:
                        reserve_time = firebase.reserve_notice(user_id, room_name)
                        reserve_time_delta = reserve_time + datetime.timedelta(hours=1)
                        notice_time = f'{reserve_time.hour}:{reserve_time.minute} 〜 {reserve_time_delta.hour}:{reserve_time_delta.minute}'
                        return flex_message_template.done_reservation_message(room_name, notice_time)
                else:
                    return TextSendMessage(text=f'{room_name}は空席があります。')
    else:
        return flex_message_template.closing_day_message()


def create_new_reserve_notice_message(room_name, user_id):
    if rooms_data := firebase.get_rooms_data():
        for room_data in rooms_data['data']:
            if room_name == room_data['name']:
                if room_data['seats_num'] == 0:
                    reserve_time = firebase.reserve_notice(user_id, room_name)
                    reserve_time_delta = reserve_time + datetime.timedelta(hours=1)
                    notice_time = f'{str(reserve_time.hour).zfill(2)}:{str(reserve_time.minute).zfill(2)} 〜 {str(reserve_time_delta.hour).zfill(2)}:{str(reserve_time_delta.minute).zfill(2)}'
                    return flex_message_template.done_reservation_message(room_name, notice_time)
                else:
                    return TextSendMessage(text=f'{room_name}は空席があります。')
    else:
        return flex_message_template.closing_day_message()


def create_failure_message():
    return TextSendMessage(text='入力に謝りががります')