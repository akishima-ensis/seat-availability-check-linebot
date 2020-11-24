from linebot.models import FlexSendMessage


def seats_info_message(room):

    room_name = room['name']
    seats_num = room['seats_num']
    total_seats_num = room['total_seats_num']
    update = room['update']

    seats_status_color_code = '#94D0B6'
    if seats_num == 0:
        seats_status_color_code = '#F7A5AB'

    alt_text = f'空席: {seats_num} {update} 更新'

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
                    'weight': 'regular',
                    'size': 'xl',
                    'align': 'center',
                },
                {
                    'type': 'separator',
                    'margin': 'lg'
                },
                {
                    'type': 'text',
                    'text': '空席あり',
                    'weight': 'bold',
                    'size': 'xxl',
                    'color': seats_status_color_code,
                    'align': 'center',
                    'margin': 'lg',
                },
                {
                    'type': 'text',
                    'text': f'{seats_num} / {total_seats_num}',
                    'weight': 'bold',
                    'size': '4xl',
                    'align': 'center',
                },
                {
                    'type': 'text',
                    'text': f'{update} 更新',
                    'size': 'lg',
                    'color': '#7E837FFF',
                    'align': 'center',
                    'margin': 'lg',
                }
            ]
        }
    }

    return FlexSendMessage(alt_text=alt_text, contents=contents)


def closing_day_message_template():
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
                    'text': '現在は閉館しています。',
                    'weight': 'bold',
                    'size': 'xl',
                    'align': 'center',
                    'gravity': 'center',
                    'wrap': True,
                    'contents': []
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
                                    'size': 'md',
                                    'color': '#A3A3A3FF',
                                    'flex': 2,
                                    'align': 'center',
                                    'contents': []
                                },
                                {
                                    'type': 'text',
                                    'text': '火〜金（10:00-20:00）\n土日祝（10:00～18:00）',
                                    'size': 'md',
                                    'color': '#666666',
                                    'flex': 4,
                                    'align': 'center',
                                    'wrap': True,
                                    'contents': []
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
                                    'size': 'md',
                                    'color': '#A3A3A3FF',
                                    'flex': 1,
                                    'align': 'center',
                                    'contents': []
                                },
                                {
                                    'type': 'text',
                                    'text': ' 毎週月曜日(休日の場合は次の平日)、年末年始、特別整理期間',
                                    'size': 'sm',
                                    'color': '#666666',
                                    'flex': 4,
                                    'align': 'center',
                                    'wrap': True,
                                    'contents': []
                                }
                            ]
                        }
                    ]
                }
            ]
        },
        'footer': {
            'type': 'box',
            'layout': 'horizontal',
            'flex': 1,
            'contents': [
              {
                  'type': 'button',
                  'action': {
                      'type': 'uri',
                      'label': '公式サイト',
                      'uri': 'https://www.akishimaensis.jp/'
                  }
              }
            ]
        }
    }

    return FlexSendMessage(alt_text=alt_text, contents=contents)


def failure_message_template():
    alt_text = '正しい部屋名を入力してください'
    contents = {
      'type': 'bubble',
      'body': {
        'type': 'box',
        'layout': 'vertical',
        'contents': [
          {
            'type': 'text',
            'text': '正しい部屋を入力してください',
            'size': 'lg',
            'align': 'center',
            'contents': []
          },
          {
            'type': 'separator',
            'margin': 'lg'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': '学習席（有線LAN有）',
              'text': '学習席（有線LAN有）'
            },
            'height': 'sm',
            'style': 'secondary'
          },
          {
            'type': 'separator',
            'margin': 'xs'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': '学習席',
              'text': '学習席'
            },
            'height': 'sm',
            'style': 'secondary'
          },
          {
            'type': 'separator',
            'margin': 'xs'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': '研究個室',
              'text': '研究個室'
            },
            'height': 'sm',
            'style': 'secondary'
          },
          {
            'type': 'separator',
            'margin': 'xs'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': 'インターネット・DB席',
              'text': 'インターネット・DB席'
            },
            'height': 'sm',
            'style': 'secondary'
          },
          {
            'type': 'separator',
            'margin': 'xs'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': 'グループ学習室',
              'text': 'グループ学習室'
            },
            'height': 'sm',
            'style': 'secondary'
          },
          {
            'type': 'separator',
            'margin': 'xs'
          },
          {
            'type': 'button',
            'action': {
              'type': 'message',
              'label': 'ティーンズ学習室',
              'text': 'ティーンズ学習室'
            },
            'height': 'sm',
            'style': 'secondary'
          }
        ]
      }
    }

    return FlexSendMessage(alt_text=alt_text, contents=contents)
