import json
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain_community.chat_message_histories import FileChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain.schema import AIMessage, HumanMessage
# from langchain.prompts import ChatPromptTemplate,MessagesPlaceholder,SystemMessagePromptTemplate,HumanMessagePromptTemplate
#from langchain.schema import messages_to_dict
from langchain.prompts.chat import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from google.generativeai.types import HarmCategory, HarmBlockThreshold

class llm_function():
    def __init__(self):
        # ChatOpenAIクラスのインスタンスを作成、temperatureは0.7を指定
        self.chat = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",#"gemini-1.5-pro-latest",#"gemini-pro",
            convert_system_message_to_human=True,
            max_output_tokens=256,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
                },temperature=0.7)

        memory_path = "conversation_history.json"

        # FileChatMessageHistoryインスタンスを作成
        self.file_history = FileChatMessageHistory(memory_path)

        # 会話の履歴を保持するためのオブジェクト
        self.memory = ConversationBufferMemory(return_messages=True)

        # 既存の履歴がある場合、メモリに読み込む
        for message in self.file_history.messages:
            if isinstance(message, HumanMessage):
                self.memory.chat_memory.add_user_message(message.content)
            elif isinstance(message, AIMessage):
                self.memory.chat_memory.add_ai_message(message.content)

    def set_template(self):

        with open('prompt.txt', 'r', encoding='utf-8') as file:
            # ファイル全体を一度に読み込む
            self.template = file.read()

    def create_comversation(self):

        # テンプレートを用いてプロンプトを作成
        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessagePromptTemplate.from_template(self.template),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("{input}")
        ])

        # AIとの会話を管理
        self.conversation = ConversationChain(llm=self.chat, memory=self.memory, prompt=self.prompt)

    def send_message(self,message):


        # ユーザからの入力を受け取り、変数commandに代入
        #command = f"{self.template}に従って回答してください\n{message}"
        command = f"{message}"
        response = self.conversation.predict(input=command)

        # 会話をファイルに保存
        self.file_history.add_user_message(f"User:{message}")
        self.file_history.add_ai_message(f"AI:{response}")


        return response
    
    def send_photos(self,pthoto_path,before_message):
        # Geminiに送る文章の作成
        message = HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": before_message,
                },
                {"type": "image_url", "image_url": pthoto_path},
            ]
        )
        print("事前:" + before_message)

        response = self.chat.invoke([message].content)
        print("回答:" + response)

        # 会話をファイルに保存
        self.file_history.add_user_message(f"User:{before_message}")
        self.file_history.add_ai_message(f"AI:{response}")

        return response



