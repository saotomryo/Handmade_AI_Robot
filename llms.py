import json
from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage
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

        # 会話の履歴を保持するためのオブジェクト
        self.memory = ConversationBufferMemory(return_messages=True)

    def set_template(self):

        # テンプレートを定義
        self.template = f"""
あなたは、子供用の玩具ロボットです。
おしゃべりと会話内容に応じで、前に進むこと、後ろに下がること、写真を撮って質問に答えることができます。

以下の手順で対応を行なってください。
1.質問に対して、幼児向けに向けに非常に分かりやすい言葉で、50文字以内で返事を「返事」に記載する。
2.質問に「こっちに来て」、「前に進む」に近い内容があれば「前進」に1を記載する
3.質問に「あっち行って」、「後ろに行く」に近い内容があれば「後退」に1を記載します。
4.質問内容で、映像を見ないと判断できないような内容がある場合は「撮影」に1を記載します。
5.質問内容がうれしいと感じた時は「感情」に1を記載する

出力形式はJSONで以下の項目で出力してください。
返事：
前進：
後退：
撮影：
感情：
        """

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

        print("test")

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

        return response



