import streamlit as st
import google.generativeai as genai

st.set_page_config(
    page_title="Guru AI Elite",
    page_icon="👨‍🏫",
    layout="centered"
)

st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 20px;
        padding: 15px;
        margin-bottom: 10px;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Perbaikan Gradasi Sidebar agar tidak kontras */
    [data-testid="stSidebar"] {
        background-image: linear-gradient(to bottom, rgba(26, 115, 232, 0.1), rgba(0, 0, 0, 0));
    }
    
    .stButton button {
        width: 100%;
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

if "GOOGLE_API_KEY" not in st.secrets:
    st.error("Konfigurasi API Key diperlukan di bagian Secrets.")
    st.stop()

genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

with st.sidebar:
    st.title("👨‍🏫 Kontrol Guru")
    st.subheader("Fitur Unggulan")
    st.write("🔹 **Ringkasan Kilat**: Materi berat jadi ringan.")
    st.write("🔹 **Analogi Cerdas**: Penjelasan lewat perumpamaan.")
    st.write("🔹 **Cek Paham**: Pertanyaan interaktif di akhir.")
    
    st.write("---")
    with st.expander("🗑️ Bersihkan Percakapan", expanded=False):
        st.write("Tindakan ini akan menghapus seluruh percakapan saat ini.")
        if st.button("Hapus Semua Riwayat", type="primary"):
            st.session_state.messages = []
            st.rerun()

st.title("Selamat Datang di Kelas AI")
st.caption("Belajar apapun, kapanpun, tanpa pusing.")

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Kamu adalah Guru Professional. Jelaskan materi dengan sangat mudah, ringkas, dan singkat.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tulis topik yang ingin kamu pelajari..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Guru sedang merangkum materi..."):
            try:
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error("Terjadi kendala koneksi. Coba lagi sebentar lagi.")
