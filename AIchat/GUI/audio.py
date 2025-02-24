# audio.py
import azure.cognitiveservices.speech as speechsdk

# 配置 Azure 订阅密钥和服务区域
subscription_key = "ffb8ad6c8c6f462188bb9361437522a3"
service_region = "eastasia"

# 创建语音配置
speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"

def synthesize_and_play(text):
    """将文本合成语音并播放"""
    # 创建语音合成器
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # 合成语音
    result = speech_synthesizer.speak_text_async(text).get()

    # 检查结果
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("语音合成成功并播放完成")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = speechsdk.SpeechSynthesisCancellationDetails.from_result(result)
        print(f"CANCELED: Reason={cancellation.reason}")
        if cancellation.reason == speechsdk.CancellationReason.Error:
            print(f"CANCELED: ErrorCode={cancellation.error_code}")
            print(f"CANCELED: ErrorDetails=[{cancellation.error_details}]")
            print("CANCELED: Did you update the subscription info?")
