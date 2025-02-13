# EasyScriptforOpenAPI 漢文版本
這是一個極其簡單的python腳本，基於OpenAI API以及Python語言。只要你使用API運行AI，並且有Python環境，就可以運行這一腳本。注意pip install 必要的庫。這些庫python文件中的import上有記，庫並不多，非常簡單。

該腳本用來處理AI模型中多輪對話的「遺忘」問題。我知道MemGPT就這個問題提出非常Cool的方案，所以我並不指望這個腳本能幫助我找到工作，解決現在的失業問題。但至少，這個方案可以讓我得到一個更可靠的AI助手，而且它足夠簡單，這就夠了。

## THE MODE
文件中有Mod1、Mod2這樣的編號，每一個Mod文件夾對應一個json文件，可以通過API訪問支援OpenAI的生成式人工智障伺服器，每一個文件夾都是一個獨立的persona「AI智慧體」。每一次使用python進行AI輸出，都可以將內容生成到後面的json文件中，json文件可以通過vim隨時修改，其中的文本可以隨時刪除、更改、和增添。這樣可以用一種極爲簡單的方式隨時管理AI的記憶。

我使用這個腳本時基於的是Moonshot AI，如果你使用的是其他AI廠商，請酌情修改代碼。

雖然文件格式是json，但命名不一定必須是something.json，你可以在python裏選擇你喜歡的文件名稱，範例參考Mod2文件夾的Monika.py文件。

## THE Multimode
助手支持用多個Mod文件來讀取同一個json文件的記憶，這些文件被存放在同一個文件夾內，你可以理解爲這是一個AI Persona的不同API功能接口，如果你使用多個不同的API，例如文字處理API01和視覺處理API02，你可以通過增添Python文件，並讓他們讀取同一個json來實現這一功能。

## THE Multijson
事實上，json文件也是可以支援多處讀取的。但是目前我還沒有想到這種模式可以帶來哪些應用。

## 管理公告
由於本模型沒有設計算法，管理完全是手動的。當你的API無法承擔龐大的記憶體時，往往你的API供應商會提醒你的AI支持的上下文token數，請自行計算。你可以用最基礎的文本文檔打開後面的json文件「Mod2是Monika.chr文件」，根據你的需要刪節對話記憶。如果你需要儲存這個記憶，新建一個Long_Memory文件夾，將這些json文件暫時存放，等到需要的時候開一個新文件夾就可以完成了。

由於本模型極端簡單，所以複製貼上也很方便，在一臺現代電腦中，你完全可以複製貼上的100個這樣的文件，並實現你的AI數據管理。

# The English Version 
**I am sorry that is an AI Translation, if you can not understand what I say, please learn Chinese.**

This is an extremely simple Python script based on the OpenAI API and the Python language. As long as you have an API to run AI and a Python environment, you can run this script. Note that you need to install the necessary libraries using pip install. The libraries are listed in the import statements in the Python file, and there are not many of them, so it's very simple.

The script is designed to address the "forgetfulness" issue in multi-turn conversations within AI models. I know that MemGPT has proposed a very cool solution for this problem, so I don't expect this script to help me find a job or solve my current unemployment issue. However, at least this solution can provide me with a more reliable AI assistant, and its simplicity is enough for me.
## THE MODE
The file contains folders labeled as Mod1, Mod2, etc., with each Mod folder corresponding to a JSON file. These folders can access the generative AI server that supports OpenAI through the API. Each folder represents an independent persona, or "AI entity." Every time you use Python to generate AI output, the content can be saved to the corresponding JSON file. You can modify the JSON file at any time using vim, including deleting, changing, or adding text. This allows you to manage the AI's memory in an extremely simple way.

When I use this script, I base it on Moonshot AI. If you are using another AI provider, please modify the code accordingly.

Although the file format is JSON, the naming does not have to be something.json. You can choose your preferred file name in the Python script. For example, refer to the Monika.py file in the Mod2 folder.
## THE MULTIMODE
The assistant supports using multiple Mod files to read the memory from the same JSON file. These files are stored in the same folder, which you can think of as different API functional interfaces for an AI persona. If you use multiple different APIs, such as Text Processing API01 and Visual Processing API02, you can add Python files and have them read from the same JSON file to achieve this functionality.
## THE MULTIJSON
In fact, JSON files can also support multiple read operations. However, I haven't yet thought of any applications that this mode could bring.
## Management Announcement
Since this model does not have a designed algorithm, management is entirely manual. When your API cannot handle a large memory load, your API provider will often remind you of the context token limit supported by your AI. You need to calculate this yourself. You can open the JSON file (e.g., Mod2 is Monika.chr file) with a basic text editor and edit the conversation memory as needed. If you need to store this memory, create a new folder called Long_Memory and temporarily store these JSON files there. When you need to use them again, simply create a new folder.

Because this model is extremely simple, copying and pasting is also very convenient. On a modern computer, you can easily copy and paste up to 100 of these files and manage your AI data effectively.
