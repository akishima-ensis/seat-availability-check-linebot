from linebot.models import FlexSendMessage


def seats_info_message(room, update):
    room_name = room['name']
    seats_num = room['seats_num']
    web_seats_num = room['web_seats_num']
    total_seats_num = room['total_seats_num']

    seats_status_text = '空席あり'
    seats_status_color_code = '#94D0B6'
    if seats_num == 0:
        seats_status_text = '満席'
        seats_status_color_code = '#F7A5AB'

    alt_text = f'空席: {seats_num} web空き: {web_seats_num} 総数: {total_seats_num} {update}更新'
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents': [
                {
                    'type': 'text',
                    'text': room_name,
                    'weight': 'bold',
                    'size': 'xl',
                    'align': 'center',
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'text',
                    'text': seats_status_text,
                    'weight': 'bold',
                    'size': 'xxl',
                    'color': seats_status_color_code,
                    'align': 'center',
                    'margin': 'xxl',
                },
                {
                    'type': 'text',
                    'text': f'残り {seats_num} / {total_seats_num}',
                    'weight': 'bold',
                    'size': '3xl',
                    'align': 'center',
                    'margin': 'md',
                },
                {
                    'type': 'text',
                    'text': f'{update} 更新',
                    'size': 'lg',
                    'color': '#7E837FFF',
                    'align': 'center',
                    'margin': 'xxl',
                }
            ]
        }
    }

    if seats_num == 0:
        contents.update({
            'footer': {
                'type': 'box',
                'layout': 'horizontal',
                'contents': [
                    {
                        'type': 'button',
                        'action': {
                            'type': 'message',
                            'label': '(β) 空席ができたら通知する',
                            'text': f'{room_name} 予約'
                        },
                        'color': '#FF6E6C',
                        'height': 'sm',
                        'style': 'primary',
                        'position': 'relative'
                    }
                ]
            }
        })
    return FlexSendMessage(alt_text=alt_text, contents=contents)


def confirm_new_reservation_message(reserved_room_name, new_reserve_room_name):
    alt_text = '新規予約'
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents':
                [
                    {
                        'type': 'text',
                        'text': f'既に"{reserved_room_name}"の空席通知予約をしています。既に予約されている場合、その予約をキャンセルして新規に空席通知予約を行う必要があります。',
                        'size': 'lg',
                        'align': 'start',
                        'wrap': True,
                    }
                ]
        },
        'footer': {
            'type': 'box',
            'layout': 'horizontal',
            'contents': [
                {
                    'type': 'button',
                    'action': {
                        'type': 'message',
                        'label': '(β) 新規予約',
                        'text': f'{new_reserve_room_name} 新規予約'
                    },
                    'color': '#FF6E6C',
                    'height': 'sm',
                    'style': 'primary'
                }
            ]
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=contents)


def done_reservation_message(room_name, notice_time):
    alt_text = '空席通知予約完了'
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents': [
                {
                    'type': 'text',
                    'text': room_name,
                    'size': 'xl',
                    'align': 'center',
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'text',
                    'text': f'予約完了 {notice_time}',
                    'weight': 'bold',
                    'size': 'lg',
                    'align': 'center',
                    'margin': 'lg',
                },
                {
                    'type': 'text',
                    'text': '上記の時間から1時間以内に空席ができた場合に通知します。空席ができなかった場合、閉館時間になった場合、予約は自動的にキャンセルされます。',
                    'size': 'lg',
                    'align': 'start',
                    'margin': 'lg',
                    'wrap': True,
                }
            ]
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=contents)


def closing_day_message():
    alt_text = '現在は閉館しています。'
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'spacing': 'md',
            'contents': [
                {
                    'type': 'text',
                    'text': '現在は閉館しています',
                    'weight': 'regular',
                    'size': 'xl',
                    'align': 'center',
                    'gravity': 'center',
                    'wrap': True,
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'box',
                    'layout': 'vertical',
                    'spacing': 'sm',
                    'margin': 'lg',
                    'contents': [
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'spacing': 'sm',
                            'contents': [
                                {
                                    'type': 'text',
                                    'text': '開館時間',
                                    'size': 'xl',
                                    'color': '#A3A3A3FF',
                                    'flex': 2,
                                    'align': 'center',
                                },
                                {
                                    'type': 'text',
                                    'text': '火〜金（10:00-20:00）\n土日祝（10:00～18:00）',
                                    'size': 'lg',
                                    'color': '#666666',
                                    'flex': 4,
                                    'align': 'center',
                                    'wrap': True,
                                },
                                {
                                    'type': 'spacer'
                                }
                            ]
                        },
                        {
                            'type': 'box',
                            'layout': 'vertical',
                            'spacing': 'md',
                            'contents': [
                                {
                                    'type': 'text',
                                    'text': '休館日',
                                    'size': 'xl',
                                    'color': '#A3A3A3FF',
                                    'flex': 1,
                                    'align': 'center',
                                },
                                {
                                    'type': 'text',
                                    'text': ' 毎週月曜日(休日の場合は次の平日)、年末年始、特別整理期間',
                                    'size': 'lg',
                                    'color': '#666666',
                                    'flex': 4,
                                    'align': 'start',
                                    'wrap': True,
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=contents)


def failed_to_get_data_message():
    alt_text = 'データの取得に失敗しました。'
    contents = {
        'type': 'bubble',
        'direction': 'ltr',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents': [
                {
                    'type': 'text',
                    'text': 'データ取得失敗',
                    'size': 'xl',
                    'align': 'center',
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'text',
                    'text': 'データの取得に失敗しました。数分経ってからもう一度お試しください。',
                    'size': 'lg',
                    'align': 'start',
                    'margin': 'lg',
                    'wrap': True,
                }
            ]
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=contents)


def typing_failed_message():
    alt_text = '入力された値が間違っています。'
    contents = {
        'type': 'bubble',
        'body': {
            'type': 'box',
            'layout': 'vertical',
            'contents': [
                {
                    'type': 'text',
                    'text': '正しく入力してください',
                    'size': 'xl',
                    'align': 'center',
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'text',
                    'text': 'リッチメニューに存在する学習室名を入力してください。このLINEbotについて詳しい情報は下記のリンクにある当プログラムのGitHubリポジトリをご覧ください。',
                    'size': 'lg',
                    'align': 'start',
                    'margin': 'md',
                    'wrap': True,
                }
            ]
        },
        'footer': {
            'type': 'box',
            'layout': 'vertical',
            'flex': 0,
            'spacing': 'sm',
            'contents': [
                {
                    'type': 'button',
                    'action': {
                        'type': 'uri',
                        'label': 'GitHub',
                        'uri': 'https://github.com/akishima-ensis/seat-availability-check-linebot'
                    },
                    'style': 'link'
                }
            ]
        }
    }
    return FlexSendMessage(alt_text=alt_text, contents=contents)
