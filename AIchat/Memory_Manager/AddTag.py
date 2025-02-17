from openai import OpenAI
import json
import os

# 輸入代碼，定義你要增添的文本知識庫文件名
log_file = "默認知識庫.json"

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key="你訂閱的AI",
    base_url="選擇訂閱地址",
)

# 檢查該知識庫是否存在，存在則直接讀取
if os.path.exists(log_file):
    with open(log_file, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    # 如果文件不存在，则初始化 messages 列表創建
    messages = [
        {"role": "system", "content": "你是Amadius，負責將用戶提供的文字段落提取關鍵詞，關鍵詞最多爲8個字，關鍵詞不能超過4個，分隔只能用「,」符號。如果文字數量過短，則輸出「===」。除非用戶回覆「調試模式」，否則不進行提取關鍵詞以外的對話。"}
    ]

# 客户端交互界面
while True:
    Q1 = input("請輸入一段文字或文件內容（輸入'exit'結束標籤生成程式）：")
    if Q1.lower() == 'exit':
        print("標籤生成程式結束。")
        break

    print("輸入的內容爲：", Q1)
    print("===========")
    print("標籤生成中")

    # 添加用戶需要輸入的文字
    messages.append({"role": "user", "content": Q1})

    # 調取 OpenAI 模型獲得回覆
    completion = client.chat.completions.create(
        model="選擇AI模型",
        messages=messages,
        temperature=0.3,
    )

    # 獲得模型的回覆
    A1 = completion.choices[0].message.content
    A1 = A1.replace("*", "").strip()

    # 如果回覆 "===”，則跳過標籤處理
    if A1 == "===":
        print("標籤生成結果：", A1)
    else:
        # 將生成標籤寫入到對應的user記錄，成爲可讀取的JSON數據
        for message in messages:
            if message["role"] == "user" and message["content"] == Q1:
                # 確保標籤以「,」爲符號分隔存儲
                message["tag"] = A1.replace("[", "")  # 去掉多餘的[
                message["tag"] = A1.replace("]", "")  # 去掉多餘的]
                message["tag"] = A1.replace("\n", "")  # 去掉多餘的換行符號
                break
        print("標籤生成結果：", message["tag"])



    # 保存對話記錄爲JSON知識庫數據
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

    print("===========")
