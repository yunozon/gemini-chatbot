import streamlit as st
import google.generativeai as genai
import time
import os

# stream機能の設定
def stream_res():
    response = model.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig( # 応答生成の設定
            candidate_count=1,
            stop_sequences=["x"],
            max_output_tokens=200,
            temperature=1.0,
        ),
    )
    for word in response.text.split():
        yield word + " "
        time.sleep(0.05)

# ページの設定(1度だけ実行)
st.set_page_config(page_title="Gemini Chatbot", page_icon=":)", layout="wide", initial_sidebar_state="auto")

genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # APIキーを設定
# TODO: モデルを選択変更予定
model = genai.GenerativeModel('gemini-1.5-flash') # モデルを選択 (gemini-1.5-flash)

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# メッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# チャット入力欄を表示
if prompt := st.chat_input("Type something..."):
    # ユーザが入力したテキストを履歴に追加
    st.session_state.messages.append({"role": "user", "content": prompt})
    # ユーザーが入力したテキストを表示
    with st.chat_message("user"):
        st.markdown(prompt)

    # # 応答を生成
    # response = model.generate_content(
    #     prompt,
    #     generation_config=genai.types.GenerationConfig( # 応答生成の設定
    #         candidate_count=1,
    #         stop_sequences=["x"],
    #         max_output_tokens=200,
    #         temperature=1.0,
    #     ),
    # ) 
    # 応答を表示
    with st.chat_message("assistant"):
        # st.write_stream(response.text)
        response = st.write_stream(stream_res())
    
    # 応答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": response})

