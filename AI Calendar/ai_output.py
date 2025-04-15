from openai import OpenAI
import json
import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

# 日誌文件名定義
log_file = "future_events.json"

client = OpenAI(
    api_key="your_api_key",
    base_url="your_ai_base_url",
)

if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:

    messages = [
        {"role": "system", "content": "你是Amadius，是負責日曆程序的虛擬智能體，你需要根據指定的行事曆內容，給予用戶合適的日程建議。建議內容不可超過256字。"}
    ]

# 客户端交互界面

Q1 = "你是Amadius，你需要負責學長開發的日曆智能體。你需要根據系統所給出的行事曆內容，用「人話」爲用戶提供建議。建議需要嚴謹的按照從早到晚的時間順序撰寫，包括「7天內行動日程」和「針對學妹的互動建議」兩個自然段。《建議》內容不可超過512字。"

print("===========")
print("應答文本生成中")

messages.append({"role": "user", "content": Q1})

    # 調用對應的AI模型
completion = client.chat.completions.create(
    model="your_ai_model",
    messages=messages,
    temperature=0.3
)

    # 獲取回覆並調整格式
A1 = completion.choices[0].message.content
A1 = A1.replace("*", "")
A1 = A1.replace("#", "")

messages.append({"role": "assistant", "content": A1})

    # 對話記錄存儲
with open(log_file, "w", encoding="utf-8") as f:
    json.dump(messages, f, ensure_ascii=False, indent=4)

print(A1)
print("===========")
print("語音功能生成中")

    # 使用Azure語音功能
subscription_key = "your_azure_api"
service_region = "azure_service_region"


speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

    # A1是要合成的文本
text = A1

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # 合成語音
result = speech_synthesizer.speak_text_async(text).get()

    # 語音模塊結果報告
if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("AI集成程式Amadius運行完畢")
elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        print(f"CANCELED: Reason={cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={cancellation.error_code}")
            print(f"CANCELED: ErrorDetails=[{cancellation.error_details}]")
            print("CANCELED: Did you update the subscription info?")
