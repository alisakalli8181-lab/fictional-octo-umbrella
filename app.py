import streamlit as st
from google import genai
from google.genai import types

# Sayfa Ayarları
st.set_page_config(page_title="Benim Yapay Zekam AI", page_icon="🧠", layout="centered")
st.title("🧠 Benim Yapay Zekam")
st.write("Merhaba İREM ERTUĞRUL, senin için nasıl bir araştırma yapmamı istersin?")

# Google AI Studio API anahtarını güvenli şekilde çekiyoruz
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Lütfen Secrets bölümünden GEMINI_API_KEY tanımlayın!")
    st.stop()

# Google GenAI istemcisini başlatıyoruz
client = genai.Client(api_key=api_key)

# Sohbet geçmişini tarayıcı hafızasında tutmak için
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski konuşmaları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan girdi al
if prompt := st.chat_input("Mesajınızı yazın..."):
    # Kullanıcı mesajını hafızaya ekle ve ekrana yaz
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Gemini için sistem talimatı
    system_instruction = """
    Sen İREM ERTUĞRUL tarafından geliştirilmiş, sadece ona özel çalışan gelişmiş bir yapay zeka asistanısın. 
    Karşındaki kişinin adı İREM ERTUĞRUL. Ona ismiyle hitap edebilirsin. 
    Sorulara her zaman samimi, profesyonel, doğru ve Türkçe olarak yanıt vermelisin.
    """

    # Gemini'dan yanıt üret
    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model='gemini-3.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.7
                )
            )
            answer = response.text
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
