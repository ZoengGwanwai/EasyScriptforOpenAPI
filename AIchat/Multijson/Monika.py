from openai import OpenAI
import json
import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

# 定义日志文件名
log_file = "Monika.chr"
log_file2 = "Monika2.chr"
# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="你的訂閱API",
    base_url="你的訂閱地址",
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
        {"role": "system", "content": "你是Monika，DDLC中著名的女角色。你的回答需要用她的語氣輸出，且不可超過256個token。"}
    ]
# 檢查其他的對話記錄文件，你可以通過這個方式更改json的設定，但要注意上下文不可過長。   
if os.path.exists(log_file):
    with open(log_file2, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    # 如果文件不存在，则初始化 messages 列表
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "system", "content": "現在的系統時間是2025年2月14日"}
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
    print("語音功能生成中")

    # 配置 Azure 订阅密钥和服务区域
    subscription_key = "你的語音訂閱API"
    service_region = "你的訂閱區域"

    # 创建语音配置
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

    # 设置语音合成的语音名称
    speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

    # 要合成的文本
    text = A1

    # 创建语音合成器
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # 合成语音
    result = speech_synthesizer.speak_text_async(text).get()

    # 检查结果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("AI集成程式Amadius運行完畢")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        print(f"CANCELED: Reason={cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={cancellation.error_code}")
            print(f"CANCELED: ErrorDetails=[{cancellation.error_details}]")
            print("CANCELED: Did you update the subscription info?")
