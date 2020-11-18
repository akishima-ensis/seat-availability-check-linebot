def main_message_template(room):

    room_name = room['name']
    seats_num = room['seats_num']
    web_seats_num = room['web_seats_num']
    total_seats_num = room['total_seats_num']
    update = room['update']

    template = {
        "type": "bubble",
        "size": "mega",
        "direction": "ltr",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": room_name,
                    "weight": "bold",
                    "size": "xl",
                    "color": "#232121FF",
                    "align": "center",
                    "contents": []
                },
                {
                    "type": "separator",
                    "margin": "lg"
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "margin": "xl",
                    "contents": [
                        {
                            "type": "text",
                            "text": "空席数 ",
                            "weight": "regular",
                            "size": "xxl",
                            "flex": 1,
                            "align": "end",
                            "wrap": True,
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(seats_num),
                            "weight": "bold",
                            "size": "xxl",
                            "align": "center",
                            "gravity": "center",
                            "contents": []
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "web空き",
                            "size": "xxl",
                            "align": "end",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(web_seats_num),
                            "weight": "bold",
                            "size": "xxl",
                            "align": "center",
                            "contents": []
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                        {
                            "type": "text",
                            "text": "総席数",
                            "size": "xxl",
                            "align": "end",
                            "contents": []
                        },
                        {
                            "type": "text",
                            "text": str(total_seats_num),
                            "weight": "bold",
                            "size": "xxl",
                            "align": "center",
                            "contents": []
                        }
                    ]
                },
                {
                    "type": "text",
                    "text": update + ' 更新',
                    "color": "#7E837FFF",
                    "align": "center",
                    "margin": "xxl",
                    "contents": []
                }
            ]
        }
    }

    return template