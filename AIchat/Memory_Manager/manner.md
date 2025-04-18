# 極簡的Memory-Manager記憶調用程式

通過記憶調用，檢索json數據並生成臨時性上下文，通過AI API檢索臨時性上下文，達成「記憶檢索」或「知識檢索」的目標。

當數據不足時，基於上下文的「檢索」會產生嚴重的「AI幻覺」。請妥善修改AI的persona設定「註釋裏有標記位置」。當然如果你和我一樣做娛樂目的就無所謂。

這裏附四個簡單的json文件做範例演示。你可以閱讀這四個文件，並檢驗Python的檢索成果，文件的修改可以通過直接開文本管理器進行。如果需要添加新的自定義JSON數據文件，請使用AddTag.py

作者聯繫郵箱： ZoengGwanwei@outlook.com

# AddTag 自主標籤生成模式
該作的檢索方式包括兩種「全文檢索」和「標籤檢索」。其中「全文檢索」將記錄你輸入的正文，「標籤檢索」將記錄你輸入的標籤。

這裏的標籤是AI API自主生成的，通過AddTag.py來實現。由於這是文本標籤，沒有採取向量模式，所以AI API與你的main.py上是一樣的，請不要使用所謂的「嵌入式人工智慧」。這也使得集成這兩個python文件非常簡單，如果你有集成需求，請自行修改代碼。

在AddTag.py中將log_file變量從「默認知識庫.json」改爲你需要的文件名，就可以自動生成新的知識庫JSON數據。

默認設置爲標籤不超過4個，單個標籤不超過8個字，如果需要更改參數請修改AddTag.py上的AI描述。

