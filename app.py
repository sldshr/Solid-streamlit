import streamlit as st
import requests
import os
import random
import json
import urllib.parse

# Настройка страницы
st.set_page_config(page_title="Solid Community", page_icon="📝", layout="wide")

# Инициализация состояния
if "lang" not in st.session_state:
    st.session_state.lang = "EN"

# Словарь переводов
T = {
    "EN": {
        "title": "Solid Community",
        "tab_editor": "✍️ Editor",
        "tab_news": "📰 News",
        "tab_ai": "🤖 AI Prompt",
        "publish": "Publish",
        "content": "Write your post here...",
        "type_select": "Publication type",
        "type_post": "Post",
        "type_news": "News",
        "success": "Successfully published!",
        "link": "Link to your publication",
        "news_title": "Project News",
        "no_news": "No news yet.",
        "ai_title": "AI Prompt Generator",
        "ai_desc": "Enter your idea and generate a perfect prompt for AI.",
        "ai_input": "Your idea (e.g. Guide to Python)",
        "ai_gen": "Generate Prompt",
        "ai_out": "Generated Prompt",
        "lang": "Language"
    },
    "RU": {
        "title": "Solid Community",
        "tab_editor": "✍️ Редактор",
        "tab_news": "📰 Новости",
        "tab_ai": "🤖 ИИ Промпт",
        "publish": "Опубликовать",
        "content": "Напишите ваш пост здесь...",
        "type_select": "Тип публикации",
        "type_post": "Статья",
        "type_news": "Новость",
        "success": "Успешно опубликовано!",
        "link": "Ссылка на вашу публикацию",
        "news_title": "Новости проекта",
        "no_news": "Новостей пока нет.",
        "ai_title": "Генератор промптов для ИИ",
        "ai_desc": "Введите идею и сгенерируйте идеальный промпт для ИИ.",
        "ai_input": "Ваша идея (например: Гайд по Python)",
        "ai_gen": "Сгенерировать промпт",
        "ai_out": "Готовый промпт",
        "lang": "Язык"
    }
}

def t(key):
    return T[st.session_state.lang][key]

# Функция для работы с Supabase
def db_request(path, method="GET", payload=None):
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_KEY", "")
    
    if not url or not key:
        st.error("Supabase is not configured. Please set SUPABASE_URL and SUPABASE_KEY.")
        return None

    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    try:
        if method == "GET":
            r = requests.get(f"{url}/rest/v1/{path}", headers=headers)
        elif method == "POST":
            r = requests.post(f"{url}/rest/v1/{path}", json=payload, headers=headers)
        
        if r.status_code == 404:
            return None
        r.raise_for_status()
        if r.text:
            return r.json()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        return None

# Боковая панель
with st.sidebar:
    st.title("Solid Community")
    lang_choice = st.radio(t("lang"), ["EN", "RU"], index=0 if st.session_state.lang == "EN" else 1)
    if lang_choice != st.session_state.lang:
        st.session_state.lang = lang_choice
        st.rerun()

# Проверка параметра для просмотра поста
query_params = st.query_params
if "post" in query_params:
    slug = query_params["post"]
    res = db_request(f"posts?slug=eq.{slug}&select=content,created_at")
    
    if res and len(res) > 0:
        st.title(f"Post #{slug}")
        st.caption(f"Published at: {res[0]['created_at'][:10]}")
        st.divider()
        st.markdown(res[0]["content"])
        st.divider()
        if st.button("← Back to Home"):
            st.query_params.clear()
            st.rerun()
    else:
        st.error("Post not found.")
        if st.button("← Back to Home"):
            st.query_params.clear()
            st.rerun()
    st.stop()

# Главная страница с вкладками
st.title(t("title"))

tab1, tab2, tab3 = st.tabs([t("tab_editor"), t("tab_news"), t("tab_ai")])

# --- ВКЛАДКА РЕДАКТОРА ---
with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        content = st.text_area(t("content"), height=400)
        pub_type = st.selectbox(t("type_select"), [t("type_post"), t("type_news")])
        btn_publish = st.button(t("publish"), type="primary", use_container_width=True)
        
    with col2:
        st.markdown("### Live Preview")
        st.markdown(content if content else "*Nothing to preview yet...*")
    
    if btn_publish:
        if content.strip():
            new_slug = str(random.randint(10000, 99999))
            db_type = "post" if pub_type == t("type_post") else "news"
            
            payload = {"slug": new_slug, "content": content, "type": db_type}
            res = db_request("posts", "POST", payload)
            
            if res:
                st.success(t("success"))
                st.markdown(f"**{t('link')}:** [{new_slug}](/?post={new_slug})")
        else:
            st.warning("Content cannot be empty.")

# --- ВКЛАДКА НОВОСТЕЙ ---
with tab2:
    st.header(t("news_title"))
    res = db_request("posts?type=eq.news&select=slug,content,created_at&order=created_at.desc")
    
    if res and len(res) > 0:
        for item in res:
            with st.expander(f"News #{item['slug']} - {item['created_at'][:10]}", expanded=False):
                st.markdown(item["content"])
    else:
        st.info(t("no_news"))

# --- ВКЛАДКА ИИ ---
with tab3:
    st.header(t("ai_title"))
    st.write(t("ai_desc"))
    
    idea = st.text_input(t("ai_input"))
    
    if st.button(t("ai_gen")) and idea.strip():
        prompt_template = f"""You are a Markdown expert. Write the raw text for an article on the topic: "{idea}".

IMPORTANT: Your response will be inserted into a custom Markdown parser. Do not try to format the text for chat, do not use HTML. Just output raw text using STRICTLY these elements:
- Headings from 1 to 6 levels (e.g., # Heading, ## Subheading).
- Regular paragraphs of text.
- Lists: bulleted (-, *, +) and numbered (1., 2.).
- Quotes (starting with the > symbol).
- Horizontal rules (---, ***, ___).
- Text formatting: **bold**, *italic*, ~~strikethrough~~, `inline code`.
- Links: [link text](https://example.com).

PROHIBITED:
- Using HTML tags.
- Building tables.
- Inserting images.
- Using code blocks (triple backticks).

Volume requirement: up to 10,000 characters.
Output ONLY the raw Markdown text, without introductions or explanations."""
        
        st.text_area(t("ai_out"), value=prompt_template, height=300)
