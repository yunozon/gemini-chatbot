import streamlit as st
import google.generativeai as genai
import os

st.title('Streamlit Chatbot') # タイトルを表示


genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # APIキーを設定

model = genai.GenerativeModel('gemini-1.5-flash') # モデルを選択

prompt = "geminiについて教えて"
response = model.generate_content(prompt) # テキストを生成
print(response.text) # 生成されたテキストを表示

# st.write('ここにチャットボットのコードを書いてください')
