# chat_logic.py
from openai import OpenAI
from constants import API_KEY, BASE_URL
from utils import save_messages
from datetime import datetime, timedelta
from audio import synthesize_and_play  # 导入语音合成函数

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def send_message(messages, user_input):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    messages.append({"role": "user", "content": user_input, "timestamp": timestamp})

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        temperature=0.3,
    )

    response = completion.choices[0].message.content
    response = response.replace("*", "")

    messages.append({"role": "assistant", "content": response, "timestamp": timestamp})
    save_messages(messages)

    # 合成语音并播放
    synthesize_and_play(response)

    return response
