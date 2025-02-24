# utils.py
import json
import os
from datetime import datetime, timedelta
from constants import log_file

def forget_algorithm(messages):
    print("程序数据整理中...")
    current_time = datetime.now()
    for message in messages:
        if "timestamp" not in message:
            message["timestamp"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 添加时间戳

    # 标记超过3天的对话为B
    for message in messages:
        message_time = datetime.strptime(message["timestamp"], '%Y-%m-%d %H:%M:%S')
        if current_time - message_time > timedelta(days=3):
            message["forget_level"] = "B"
            message["content"] = compress_message(message["content"])

    # 标记超过7天的对话为C，并进行压缩
    for message in messages:
        if "forget_level" in message and message["forget_level"] == "B":
            message_time = datetime.strptime(message["timestamp"], '%Y-%m-%d %H:%M:%S')
            if current_time - message_time > timedelta(days=7):
                message["forget_level"] = "C"
                message["content"] = compress_message(message["content"])

    # 合并标记为C的对话
    new_messages = []
    temp_message = {"role": None, "content": ""}
    for message in messages:
        if "forget_level" in message and message["forget_level"] == "C":
            if message["role"] == temp_message["role"]:
                temp_message["content"] += " " + message["content"]
            else:
                if temp_message["role"]:
                    new_messages.append(temp_message)
                temp_message = message
        else:
            new_messages.append(message)
    if temp_message["role"]:
        new_messages.append(temp_message)

    # 保存更新后的对话记录
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(new_messages, f, ensure_ascii=False, indent=4)
    print("数据整理完成。")

def compress_message(content):
    return content[:64] + "..." if len(content) > 64 else content

def load_messages():
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

def save_messages(messages):
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
