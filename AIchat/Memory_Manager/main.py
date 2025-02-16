from openai import OpenAI
import json
import os
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="你訂閱的AI API",
    base_url="你訂閱的AI地址",
)

# 定義變量，加載文件名
log_file = "dialogue_log.json"

# 第一部分：檢索記憶庫生成臨時性上下文文件

def retrieve_memory_by_criteria(criteria_type, criteria_value, memory_folder="."):
    """
    根據用戶選擇的方式，檢索該文件夾出現的全部 JSON 文件。
    :param criteria_type: 檢索方式（"role", "text"）
    :param criteria_value: 檢索的具體值
    :param memory_folder: 存儲記憶文件夾，默認爲當前文件夾
    :return: 檢索到的記憶列表
    """
    if not os.path.exists(memory_folder):
        print("指定的文件夾不存在。")
        return []

    # 获取文件夹中所有.json文件
    json_files = [f for f in os.listdir(memory_folder) if f.endswith(".json")]

    if not json_files:
        print("文件夾中未找到任何 JSON 文件。")
        return []

    results = []
    for file in json_files:
        file_path = os.path.join(memory_folder, file)
        try:
            with open(file_path, "r") as f:
                memory = json.load(f)
        except json.JSONDecodeError:
            print(f"文件 {file} 不是有效的 JSON 文件，已略過。")
            continue

        for entry in memory:
            if criteria_type == "role" and entry.get("role") == criteria_value:
                results.append(entry)
            elif criteria_type == "text" and criteria_value in entry.get("content", ""):
                results.append(entry)
            elif criteria_type == "tag" and criteria_value in entry.get("tag", ""):
                results.append(entry)

    return results

def display_retrieved_entries(entries):
    """
    顯示檢索到的記憶。
    :param entries: 檢索到的記憶列表
    """
    if not entries:
        print("未找到記憶。")
        return

# 只保留role、content字段下進行寫入，生成臨時性對話文本。

    for entry in entries:
        print("尋到記憶：")
        print(f"  - 角色：{entry.get('role', '未知')}")
        print(f"  - 內容：{entry.get('content', '未知')}")
        print("-" * 40)

def save_to_dialogue_log(entries, output_file="dialogue_log.json"):
    """
    將檢索到的記憶保存到一个 JSON 文件中，該 JSON 文件系「臨時的對話文件」，將被AI API的上下文檢索調用。
    :param entries: 檢索到的記憶列表
    :param output_file: 輸出文件名，默認爲 "dialogue_log.json"
    """
    if not entries:
        print("沒有檢索到記憶可被用來保存。")
        return

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=4)
        print(f"檢索到的記憶已成功保存到 {output_file}。")
    except Exception as e:
        print(f"保存到文件时出錯：{e}")

# 示例：用户输入检索方式和值
if __name__ == "__main__":
    print("在使用AI前，可以通過「關鍵詞」對AI儲存的「知識庫」進行先期檢索，通過記憶整理幫助AI處理龐大的數據文件，這樣可以讓AI突破常規token的限制，回覆也可以更精確。")
    print("==============")
    print("請選擇檢索方式：")
#    身分檢索不可使用，僅供測試。
#    print("0. 身份檢索 (role)")
    print("1. 文章檢索 (text)")
    print("2. 標籤檢索 (tag)")   

    choice = input("請輸入選項編號 (0-1): ")
    criteria_type = ""

    if choice == "1":
        criteria_type = "text"
        criteria_value = input("請輸入檢索文本「寧要少字不可多字」: ")    
#   elif choice == "0":
#       criteria_type = "role"
#       criteria_value = input("请输入角色类型 (如 'user' 或 'assistant'): ")
    elif choice == "2":
        criteria_type = "tag"
        criteria_value = input("請輸入標籤關鍵詞「寧要少字不可多字」: ")
    else:
        print("選項無效，不要輸入選項編號以外的內容。")
        exit()

    retrieved_entries = retrieve_memory_by_criteria(criteria_type, criteria_value)
    display_retrieved_entries(retrieved_entries)
    save_to_dialogue_log(retrieved_entries)

# 第二部分：檢索記憶後開始使用API進行問答
print("==============")
print("知識記憶整理完成")
print("==============")
print("OpenAI開始啓動")

# 检查是否存在之前的臨時性對話記錄文件，如果存在则加载persona設定。
# Persona設定會檢索對話的上下文，完成用戶的應答。
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
        messages.append({"role": "system", "content": "你是Amadius，一個回顧過去對話的知識助手。面對用戶的問題，你需要通過檢索你曾經進行過的對話，並整理出準確明確的答覆。對於過去對話中不存在的內容，則不要進行過多闡釋。"})
else:
    # 如果文件不存在，则初始化 messages 列表並進入一般閒聊模式
    messages = [
        {"role": "system", "content": "這是一次臨時性的會話。"}
    ]

# 客户端交互界面
while True:
    Q1 = input("請輸入一個問題（輸入'exit'結束對話）：")
    if Q1.lower() == 'exit':
        print("對話結束。")
        print("==============")
        print("監測臨時對話文件")
        break


    print("問題爲：", Q1)
    print("===========")
    print("應答文本生成中")

    # 添加用户的新問題到消息列表
    messages.append({"role": "user", "content": Q1})

    # 調取 OpenAI 模型獲取回覆
    completion = client.chat.completions.create(
        model="moonshot-v1-128k",
        messages=messages,
        temperature=0.3,
    )

    # 獲取模型的回复
    A1 = completion.choices[0].message.content
    A1 = A1.replace("*", "")

    # 將回覆添加到消息列表中
    messages.append({"role": "assistant", "content": A1})

    # 保存對話記錄到文件，確保一次對話內的上下文聯動對話。
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    print(A1)
    print("===========")
    print("語音功能生成中")

    # 配置 Azure 訂閱密鑰和服務區域
    subscription_key = "微軟Azure的訂閱地址"
    service_region = "你的訂閱區域"

    # 創建語音配置
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

    # 設置語音名稱
    speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

    # 要合成的文本
    text = A1

    # 創建語音合成器
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # 合成語音
    result = speech_synthesizer.speak_text_async(text).get()

    # 檢查結果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("AI集成程式Amadius運行完畢")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        print(f"CANCELED: Reason={cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={cancellation.error_code}")
            print(f"CANCELED: ErrorDetails=[{cancellation.error_details}]")
            print("CANCELED: Did you update the subscription info?")
       
# 退出循環後，需要刪除「臨時對話」dialogue_log.json      
if os.path.exists("dialogue_log.json"):
   os.remove("dialogue_log.json")
   print("==============")
   print("臨時對話文件已删除。")
else:
   print("==============")
   print("臨時對話文件不存在。")    
       
