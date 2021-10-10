from linebot.models import StickerSendMessage


ROOM_NAME_MESSAGES = {
  '学習席（有線LAN有）': 0,
  '学習席': 1,
  '研究個室': 2,
  'インターネット・DB席': 3,
  'グループ学習室': 4,
  'ティーンズ学習室': 5,
}

ROOM_RESERVATION_MESSAGES = {
  '学習席（有線LAN有） 予約': 0,
  '学習席 予約': 1,
  '研究個室 予約': 2,
  'インターネット・DB席 予約': 3,
  'グループ学習室 予約': 4,
  'ティーンズ学習室 予約': 5,
}

ROOM_NEW_RESERVATION_MESSAGES = {
  '学習席（有線LAN有） 新規予約': 0,
  '学習席 新規予約': 1,
  '研究個室 新規予約': 2,
  'インターネット・DB席 新規予約': 3,
  'グループ学習室 新規予約': 4,
  'ティーンズ学習室 新規予約': 5,
}

STICKER_MESSAGES = [
  StickerSendMessage(package_id=11537, sticker_id=52002753),
  StickerSendMessage(package_id=11537, sticker_id=52002739),
  StickerSendMessage(package_id=11537, sticker_id=52002757),
  StickerSendMessage(package_id=11539, sticker_id=52114110),
  StickerSendMessage(package_id=11539, sticker_id=52114121),
]
