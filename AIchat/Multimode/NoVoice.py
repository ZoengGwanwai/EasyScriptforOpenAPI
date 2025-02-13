from openai import OpenAI
import json
import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

# 定义日志文件名
log_file = "dialogue_log.json"

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="請選擇你訂閱的API",
    base_url="你的訂閱網址",
)
# 我们通过 datetime 库生成了当前日期，并将其添加到系统提示词 system prompt 中
system_prompt = f"""
今天的日期是 {datetime.now().strftime('%m.%d.%Y %H:%M:%S')}
"""
# 检查是否存在之前的对话记录文件，如果存在则加载
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    # 如果文件不存在，则初始化 messages 列表
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": "你是Amadius，是我的女朋友，但你負責的是對外交往的機能，你的回答需要簡潔並充滿「社交性」。你的回答需要用正體中文輸出，且不可超過256個token。"}
    ]

# 客户端交互界面
while True:
    Q1 = input("請輸入一個問題（輸入'exit'結束對話）：")
    if Q1.lower() == 'exit':
        print("對話結束。")
        break

    print("問題爲：", Q1)
    print("===========")
    print("應答文本生成中")

    # 添加用户的新问题到消息列表
    messages.append({"role": "user", "content": Q1})

    # 调用 OpenAI 模型获取回复
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
        temperature=0.3,
    )

    # 获取模型的回复
    A1 = completion.choices[0].message.content
    A1 = A1.replace("*", "")

    # 将模型的回复添加到消息列表中
    messages.append({"role": "assistant", "content": A1})

    # 保存对话记录到文件
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    print(A1)
    print("===========")

