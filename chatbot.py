import streamlit as st
import google.generativeai as genai
import time
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# stream機能の設定
def stream_res(prompt):
    try:
        # AI応答を生成
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(  # 応答生成の設定
                candidate_count=1,
                stop_sequences=["x"],
                max_output_tokens=1000,
                temperature=temperature,
            ),
            # 安全設定を追加
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            }
        )
        
        # 応答のパーツを確認
        if response.parts and len(response.parts) > 0:  # partsが空でないことを確認
            candidate = response.parts[0]  # 最初のパーツを取得

            # フィールドが存在し、かつ空でないか確認
            if hasattr(candidate, 'text') and candidate.text.strip():
                full_response = ""
                for word in candidate.text.split():
                    full_response += word + " "
                    yield word + " "
                    time.sleep(0.05)  # ストリーミングの速度を調整
            else:
                st.warning("The model did not return a valid 'text' field.")
        else: # 安全性に問題がある場合
            st.error("No valid response was returned by the model.")  # エラーメッセージを表示
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

# ページの設定
st.set_page_config(page_title="Gemini Chatbot", page_icon=":)", layout="wide", initial_sidebar_state="auto")
st.title('Gemini Chatbot')
st.caption("🚀 A Streamlit chatbot powered by Gemini")

# サイドバーの設定
with st.sidebar:
    # APIキーを設定
    api_key = st.text_input("Gemini API Key", key="chatbot_api_key", type="password")
    "[Get a Gemini API key](https://aistudio.google.com/app/apikey)"
    if api_key:
        st.write("API key set successfully!")
    else:
        st.write("Please set an API")
    # modelを選択
    model_name = st.selectbox("Select a model", ["gemini-1.5-flash", "gemini-1.5-pro"])
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.01) # min, max, default, step
    # 会話のリセット
    if st.button("Reset chat"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Get started by typing something!"}
        ]

genai.configure(api_key=api_key)  # APIキーを設定

# モデルを選択
model = genai.GenerativeModel(model_name= model_name)

# チャット履歴の初期化
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Get started by typing something!"}
    ]

# メッセージを表示
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
        
# チャット入力欄を表示
if prompt := st.chat_input("Type something..."):
    if not api_key:
        st.info("Please add your Gemini API key to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for word in stream_res(prompt):
            full_response += word
            message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})