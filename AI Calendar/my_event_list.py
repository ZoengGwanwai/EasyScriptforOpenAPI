from icalendar import Calendar, Event
from datetime import datetime, timedelta
import json
import os

# 當前時間
current_time = datetime.now()

# 讀取本機日曆文件地址
calendar_file_path = os.path.expanduser("/share/evolution/calendar/system/calendar.ics")  # 示例路径，根据实际情况修改

if not os.path.exists(calendar_file_path):
    raise FileNotFoundError(f"文件 {calendar_file_path} 不存在，请检查路径是否正确。")

with open(calendar_file_path, 'rb') as f:
    cal = Calendar.from_ical(f.read())

# 提取事件存儲信息
future_events = []

# 日曆事件遍歷
for component in cal.walk():
    if component.name == "VEVENT":
        # 開始時間、結束時間提取
        dtstart = component.get('dtstart').dt
        dtend = component.get('dtend').dt
        # 如果 dtstart 或 dtend 是 datetime.date ，將其轉換爲 datetime.datetime 
        if not isinstance(dtstart, datetime):
            dtstart = datetime.combine(dtstart, datetime.min.time())
        if not isinstance(dtend, datetime):
            dtend = datetime.combine(dtend, datetime.min.time())

        # 時區轉換
        if dtstart.tzinfo is not None:
            dtstart = dtstart.replace(tzinfo=None)
        if dtend.tzinfo is not None:
            dtend = dtend.replace(tzinfo=None)



        # 註釋包括「搜索全部未來事件」和「專注於未來72小時之內的事件」兩種模式。如果需要援引全部未來事件進行綜合分析，請選擇第1條代碼。如果專注於72小時之內，選擇第2條代碼。
        # The comment includes two modes: "Search all future events" and "Focus on events within the next 72 hours." If you need to reference all future events for comprehensive analysis, please choose the first code. If you want to focus on the next 72 hours, choose the second code.
        if dtstart >= current_time:
        # if dtstart >= current_time and dtstart <= current_time + timedelta(hours=72):

            # AI計算的星期往往是錯的，使用漢字「月火水木金土日」進行標記可以讓AI瞭解正確的星期。
            weekdays = ["月", "火", "水", "木", "金", "土", "日"]
            weekday = weekdays[current_time.weekday()]
            # 提取事件訊息形成格式化文字給ai作爲前置環境
            event_info = {
                "role": "system",
                "content": f"今日、{current_time}({weekday})；行事曆中對於該事件的陳述如下：{component.get('summary')}（開始時間：{dtstart.isoformat()}；結束時間：{dtend.isoformat()}；描述：{component.get('description') if 'description' in component else '無'}）"
            }
            future_events.append(event_info)

# 將提取信息記錄爲json
output_file = "future_events.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(future_events, f, ensure_ascii=False, indent=4)

print(f"提取事件信息已存儲於 {output_file} 中。")
