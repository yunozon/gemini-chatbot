import streamlit as st
import google.generativeai as genai
import os

st.title('Streamlit Chatbot') # タイトルを表示

# # ユーザーが入力したテキストを取得
# with st.chat_message("user"):
#     st.write("こんにちはだよ")

# # チャット入力欄を表示
# prompt = st.text_input("チャットを入力してください")
# if prompt:
#     st.write(f"ユーザー: {prompt}")

# Initialize chat history
# chat_history = []
# チャット履歴の初期化: st.session_state というストレージを使って、アプリの実行が繰り返されてもチャットの履歴を保持します。アプリが初めて実行されたとき、チャット履歴はまだないため、空のリストを作成します。
if "message" not in st.session_state: # session_stateにmessageがない場合
    st.session_state.message = [] # session_stateに空のリストを代入

# メッセージを表示
for message in st.session_state.message:
    with st.chat_message(message["role"]):
        st.write(message["content"])