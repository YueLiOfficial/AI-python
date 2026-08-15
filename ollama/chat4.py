import requests
import json
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "请用简洁的语言回答"}
    ]

st.title("My first AI Chat Assistant")

for msg in st.session_state.messages:
    if msg.get("role") == "system":
        continue

    with st.chat_message(msg.get("role")):
        st.write(msg.get("content"))

prompt = st.chat_input("请输入消息")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.write(prompt)

    resp = requests.post(
        url="http://localhost:11434/api/chat",
        json={
            "model": "qwen3.5:4b",
            "messages": st.session_state.messages,
            "stream": True,
            "think": False
        },
        stream=True
    )

    with st.chat_message("assistant"):
        reply = ""
        box = st.empty()
        for lines in resp.iter_lines():
            if not lines:
                continue

            msg = json.loads(lines)

            if msg.get("done"):
                break

            reply_content = msg.get("message", {}).get("content", "")
            reply += reply_content

            box.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})
