import telebot
import requests
import sys
from langchain.document_loaders import PyPDFLoader 
from langchain.embeddings import OpenAIEmbeddings 
from langchain.vectorstores import Chroma 
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms import OpenAI

import os
os.environ["OPENAI_API_KEY"] = "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"

bot_access_token = '6174341898:AAEZuZIdQnJ4Xr8REGrt5Wij6mREK2Jefmg'
PINE_CONE_API_KEY = "1b431132-8c4f-4824-8f5d-399cb1a18b3b"
PINE_CONE_ENVIRONMENT = "asia-southeast1-gcp-free"

bot = telebot.TeleBot(bot_access_token)


@bot.message_handler(commands=['start'])  # welcome message handler
def send_welcome(message):
    bot.reply_to(message, 'Welcome user ! Join us here @russion_telegram_bot for any query related to our company.')


@bot.message_handler()
def handle_query(message):
    print(message.text)
    result = pdf_qa({"question": message.text})
    print("Answer:", result["answer"])


pdf_path = "./FAQ.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load_and_split()


embeddings = OpenAIEmbeddings()
vectordb = Chroma.from_documents(pages, embedding=embeddings, 
                                 persist_directory=".")
vectordb.persist()
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
pdf_qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0.8) , vectordb.as_retriever(), memory=memory)

query = "What is Bitcoin?"


while True:
    try:
        bot.polling(none_stop=False)
        sys.exit()
        print ('polling ///')
    except Exception:
        print("Fallen in exception ")
        time.sleep(15)