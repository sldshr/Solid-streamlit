import streamlit as st
import time
import random
import uuid
from datetime import datetime

# ============================================================
# НАСТРОЙКА СТРАНИЦЫ
# ============================================================
st.set_page_config(
    page_title="AI Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CSS СТИЛИ
# ============================================================
st.markdown("""
<style>
    /* Основной фон */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a2e 50%, #16213e 100%);
    }

    /* Скрыть дефолтный header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Сообщения чата */
    .chat-message {
        padding: 16px 20px;
        border-radius: 16px;
        margin: 10px 0;
        display: flex;
        gap: 12px;
        animation: fadeIn 0.3s ease-in;
        max-width: 90%;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(6px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .chat-user {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 4px;
    }

    .chat-ai {
        background: rgba(255, 255, 255, 0.06);
        color: #e4e4e7;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-bottom-left-radius: 4px;
    }

    .avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }

    .avatar-user { background: rgba(255,255,255,0.2); }
    .avatar-ai {
        background: linear-gradient(135deg, #22c55e, #16a34a);
    }

    /* Заголовок */
    .main-title {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #a78bfa, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }
    .main-subtitle {
        text-align: center;
        color: #94a3b8;
        margin-bottom: 30px;
        font-size: 0.95rem;
    }

    /* Поле ввода */
    .stChatInput textarea {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border-radius: 24px !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
    }

    /* Сайдбар */
    section[data-testid="stSidebar"] {
        background: rgba(10, 10, 20, 0.95);
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    /* Кнопки в сайдбаре */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.04);
        color: #e4e4e7;
        transition: all 0.2s ease;
        text-align: left;
        padding: 8px 12px;
    }
    .stButton > button:hover {
        background: rgba(139, 92, 246, 0.2);
        border-color: #8b5cf6;
        color: white;
    }

    /* Кнопка "Новый чат" */
    div[data-testid="stButton"]:has(button[kind="primary"]) button {
        background: linear-gradient(135deg, #8b5cf6, #06b6d4);
        border: none;
        font-weight: 600;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)


# ============================================================
# СОСТОЯНИЕ (SESSION STATE)
# ============================================================
def new_chat_id() -> str:
    return str(uuid.uuid4())


if "chats" not in st.session_state:
    # chats: {chat_id: {"title": str, "messages": [ {role, content} ]}}
    st.session_state.chats = {}

if "current_chat" not in st.session_state:
    cid = new_chat_id()
    st.session_state.chats[cid] = {"title": "Новый чат", "messages": []}
    st.session_state.current_chat = cid


# ============================================================
# ЗАГЛУШКА ИИ (замените эту функцию на реальный вызов)
# ============================================================
def fake_ai_response(user_text: str) -> str:
    """Имитация ответа ИИ. Замените на реальный API-вызов."""
    time.sleep(1.0)  # имитация задержки

    responses = [
        f"Я получил ваш запрос: **«{user_text}»**.\n\n"
        f"Это заглушка — реальная интеграция с моделью пока не подключена. "
        f"Но интерфейс полностью готов к тому, чтобы вы вставили сюда вызов "
        f"OpenAI / Anthropic / локальной модели.",

        f"Интересный вопрос! 🤔\n\n"
        f"Вы написали: `{user_text}`.\n\n"
        f"Это демо-ответ. Чтобы подключить настоящий ИИ — "
        f"отредактируйте функцию `fake_ai_response()` в коде.",

        f"Принято! 📨\n\n"
        f"- Ваш текст: {user_text}\n"
        f"- Длина: {len(user_text)} символов\n"
        f"- Время: {datetime.now().strftime('%H:%M:%S')}\n\n"
        f"_Это автоматическая заглушка вместо ответа ИИ._",
    ]
    return random.choice(responses)


# ============================================================
# ФУНКЦИЯ РЕНДЕРА СООБЩЕНИЯ
# ============================================================
def render_message(role: str, content: str):
    if role == "user":
        st.markdown(f"""
        <div class="chat-message chat-user">
            <div class="avatar avatar-user">👤</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-message chat-ai">
            <div class="avatar avatar-ai">🤖</div>
            <div>{content}</div>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# БОКОВАЯ ПАНЕЛЬ
# ============================================================
with st.sidebar:
    st.markdown("### 🤖 **AI Chat**")
    st.caption("Демо-интерфейс")

    if st.button("➕ Новый чат", type="primary", use_container_width=True):
        cid = new_chat_id()
        st.session_state.chats[cid] = {"title": "Новый чат", "messages": []}
        st.session_state.current_chat = cid
        st.rerun()

    st.markdown("---")
    st.markdown("**История чатов**")

    # Список чатов (сначала новые)
    for cid, chat in list(st.session_state.chats.items())[::-1]:
        title = chat["title"][:28] + ("…" if len(chat["title"]) > 28 else "")
        is_active = cid == st.session_state.current_chat
        prefix = "🟣" if is_active else "💬"

        col1, col2 = st.columns([5, 1])
        with col1:
            if st.button(f"{prefix} {title}", key=f"chat_{cid}", use_container_width=True):
                st.session_state.current_chat = cid
                st.rerun()
        with col2:
            if st.button("🗑", key=f"del_{cid}", help="Удалить чат"):
                del st.session_state.chats[cid]
                if st.session_state.current_chat == cid:
                    if st.session_state.chats:
                        st.session_state.current_chat = list(st.session_state.chats.keys())[0]
                    else:
                        new_id = new_chat_id()
                        st.session_state.chats[new_id] = {"title": "Новый чат", "messages": []}
                        st.session_state.current_chat = new_id
                st.rerun()

    st.markdown("---")
    st.caption("⚠️ Это интерфейс без ИИ. Подключите свою модель в `fake_ai_response()`.")


# ============================================================
# ОСНОВНОЙ ЭКРАН
# ============================================================
chat = st.session_state.chats[st.session_state.current_chat]

# Заголовок
st.markdown('<div class="main-title">AI Chat</div>', unsafe_allow_html=True)
st.markdown('<div class="main-subtitle">Интерфейс готов · Модель не подключена</div>',
            unsafe_allow_html=True)

# Приветствие при пустом чате
if not chat["messages"]:
    st.markdown("""
    <div style="text-align:center; padding: 40px 20px; color:#94a3b8;">
        <div style="font-size: 56px; margin-bottom: 12px;">💬</div>
        <div style="font-size: 1.1rem; margin-bottom: 6px;">
            Начните диалог — напишите что-нибудь ниже
        </div>
        <div style="font-size: 0.85rem; opacity: 0.7;">
            (Ответы — заглушки, пока не подключена реальная модель)
        </div>
    </div>
    """, unsafe_allow_html=True)

# История сообщений
for msg in chat["messages"]:
    render_message(msg["role"], msg["content"])

# Поле ввода
user_input = st.chat_input("Напишите сообщение…")

if user_input:
    # 1. Добавляем сообщение пользователя
    chat["messages"].append({"role": "user", "content": user_input})

    # Обновляем заголовок чата по первому сообщению
    if chat["title"] == "Новый чат":
        chat["title"] = user_input[:40]

    # 2. Показываем сообщение пользователя
    render_message("user", user_input)

    # 3. Генерируем "ответ ИИ" (заглушка)
    with st.spinner("Думаю…"):
        ai_reply = fake_ai_response(user_input)

    chat["messages"].append({"role": "assistant", "content": ai_reply})
    render_message("assistant", ai_reply)

    st.rerun()
