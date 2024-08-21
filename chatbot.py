import streamlit as st
import google.generativeai as genai
import time
import os

# stream機能の設定
def stream_res(prompt):
    try: # APIが正しく動作しているか確認
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(  # 応答生成の設定
                candidate_count=1,
                stop_sequences=["x"],
                max_output_tokens=200,
                temperature=1.0,
            ),
        )
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return
    
    # 応答候補をチェック
    if response.candidates and len(response.candidates) > 0:
        candidate = response.candidates[0]

        # 安全性の確認
        if candidate.safety_ratings and len(candidate.safety_ratings) > 0:
            # 安全性に問題がある場合はエラーメッセージを表示
            st.error("安全性に関わるため、この内容には応答できません。")
            return
        
    # 正常な場合は応答を生成
    if candidate.text.strip():  # 応答が空でないことを確認
        full_response = ""  # ループ外で初期化
        for word in response.text.split():
            full_response += word + " "  # 応答全体を蓄積
            yield word + " "  # 部分的な応答をリアルタイムで返す
            time.sleep(0.05)
        return full_response  # 必要ないが明示的に応答全体を返す
    else:
        st.warning()
    """
        # 正常な応答の場合、部分的に応答を返す
        if candidate.text.strip():  # 応答が空でないことを確認
            full_response = ""
            for word in candidate.text.split():
                full_response += word + " "
                yield word + " "
                time.sleep(0.05)
            return full_response
        else:
            st.warning("The model did not return any valid response.")
            return "I'm sorry, I couldn't generate a response. Can you try again?"
    else:
        st.error("No valid response was returned by the model.")
        return "I'm sorry, I couldn't generate a response."

"""

# ページの設定(1度だけ実行)
st.set_page_config(page_title="Gemini Chatbot", page_icon=":)", layout="wide", initial_sidebar_state="auto")
st.title('Gemini Chatbot') # タイトルを表示
st.caption("🚀 A streamlit chatbot powered by Gemini") # キャプションを表示

genai.configure(api_key=os.environ["GOOGLE_API_KEY"]) # APIキーを設定
# TODO: モデルを選択変更予定
model = genai.GenerativeModel('gemini-1.5-flash') # モデルを選択 (gemini-1.5-flash)

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
# AIの応答を生成し、流れるように表示
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # ジェネレータを使って、部分的に応答を表示
        for word in stream_res(prompt):
            full_response += word  # 全体の応答を蓄積
            message_placeholder.markdown(full_response)  # 部分的な応答をリアルタイムで表示

    
    # 応答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": full_response})

