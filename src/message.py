from src import firebase, flex_message_template

rooms = [
    '学習席（有線LAN有）',
    '学習席',
    '研究個室',
    'インターネット・DB席',
    'グループ学習室',
    'ティーンズ学習室'
]


def create(message):
    if message in rooms:
        room_name = message
        rooms_data = firebase.get_rooms_data()
        if rooms_data:
            for room in rooms_data['data']:
                if room_name == room['name']:
                    return flex_message_template.seats_info_message(room, rooms_data['update'])

        return flex_message_template.closing_day_message_template()

    else:
        return flex_message_template.failure_message_template()