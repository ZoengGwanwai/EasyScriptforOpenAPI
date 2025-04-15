import tkinter as tk
from tkinter import scrolledtext, messagebox
import json
import os
import subprocess

# 日誌定義
log_file = "future_events.json"

def load_data():
    """从 future_events.json 文件中加载数据"""
    if not os.path.exists(log_file):
        return {"future_events": [], "ai_suggestions": []}
    with open(log_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    future_events = [item["content"] for item in data if item["role"] == "system"]
    ai_suggestions = [item["content"] for item in data if item["role"] == "assistant"]
    return {"future_events": future_events, "ai_suggestions": ai_suggestions}

        
def format_future_events(events):
    """格式化未来行程内容"""
    formatted_events = []
    for event in events:
        # 去掉開頭的“行事曆中對於該事件的陳述如下：”字段
        event = event.replace("行事曆中對於該事件的陳述如下：", "")
        event = event.replace("今日、", "執行日誌緒：")
        event = event.replace("（", "\n")
        event = event.replace("）", "\n")
        # 增加分隔符和分段
        event_lines = event.split("；")
        formatted_event = "=========\n" + "\n".join([line.strip() for line in event_lines])
        formatted_events.append(formatted_event)
    return formatted_events

def display_data():
    """在GUI中顯示未來行程和AI建議"""
    data = load_data()
    future_events_text.delete(1.0, tk.END)
    ai_suggestions_text.delete(1.0, tk.END)
    
    # 格式化未來行程内容
    formatted_future_events = format_future_events(data["future_events"])
    
    if not formatted_future_events:
        future_events_text.insert(tk.END, "未來行程暫無")
    else:
        for event in formatted_future_events:
            future_events_text.insert(tk.END, event + "\n\n")
    
    if not data["ai_suggestions"]:
        ai_suggestions_text.insert(tk.END, "AI建議暫無")
    else:
        for suggestion in data["ai_suggestions"]:
            ai_suggestions_text.insert(tk.END, suggestion + "\n\n")



def main():
    global future_events_text, ai_suggestions_text

    # 創建主窗口
    root = tk.Tk()
    root.title("Amadius行事曆")
    root.geometry("1200x500")  # 设置窗口大小

    # 左右佈局框架
    left_frame = tk.Frame(root, borderwidth=1, relief="solid")  # 边框样式
    left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
    right_frame = tk.Frame(root, borderwidth=1, relief="solid")  # 边框样式
    right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

    # 未來行程顯示區域
    future_events_label = tk.Label(left_frame, text="未來事件：", font=("Arial", 16, "bold"))
    future_events_label.pack(pady=5)
    future_events_text = scrolledtext.ScrolledText(left_frame, width=50, height=20, font=("Arial", 16))
    future_events_text.pack(pady=10)

    # AI建議顯示區域
    ai_suggestions_label = tk.Label(right_frame, text="Amadius建議：", font=("Arial", 16, "bold"))
    ai_suggestions_label.pack(pady=5)
    ai_suggestions_text = scrolledtext.ScrolledText(right_frame, width=50, height=20, font=("Arial", 16))
    ai_suggestions_text.pack(pady=10)

 
    # 初始數據
    display_data()

    # 運行主循環
    root.mainloop()

if __name__ == "__main__":
    main()
