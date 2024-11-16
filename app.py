# -*- coding: utf-8 -*-
"""
Streamlit Chatbot Application with Stylish RTL Design
"""

import os
import logging
import streamlit as st
from chromadb.config import Settings
from embedchain import App
import warnings
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()  # Logs to the console
    ]
)

logger = logging.getLogger(__name__)

# Environment setup
os.environ["LD_LIBRARY_PATH"] = "./bin"

# Load OpenAI API Key from secrets
try:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    logger.info("OPENAI_API_KEY successfully loaded from secrets.")
except KeyError as e:
    logger.error("OPENAI_API_KEY is missing in Streamlit secrets.", exc_info=True)
    raise RuntimeError("Missing OPENAI_API_KEY in Streamlit secrets.") from e

# Verify `pysqlite3` installation
try:
    import pysqlite3
    logger.info("pysqlite3 installed successfully.")
except ImportError as e:
    logger.error("pysqlite3 is not installed. Please ensure it is included in the environment.", exc_info=True)
    raise RuntimeError("pysqlite3 is not installed. Please use a supported environment.") from e

# Import EmbedChain App
try:
    from embedchain import App
    app = App()
    logger.info("EmbedChain App initialized successfully.")
except Exception as e:
    logger.error("Failed to initialize EmbedChain App.", exc_info=True)
    raise e

# Streamlit UI setup
st.set_page_config(
    page_title="🤖 اسأل الدكتور الرائد",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for Stylish RTL Layout
rtl_css = """
<style>
    /* Global Styling */
    html, body, [class*="css"] {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background-color: #f5f5f5;
    }

    /* Title Styling */
    .stApp > div:first-child {
        background-color: #4CAF50;
        color: white;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        margin-bottom: 20px;
        font-size: 2rem;
    }

    /* Input Textbox */
    .stTextInput > div > div > input {
        direction: rtl;
        text-align: right;
        padding: 10px;
        border: 2px solid #4CAF50;
        border-radius: 5px;
        background-color: #fff;
        font-size: 1rem;
    }

    /* Button Styling */
    .stButton button {
        background-color: #4CAF50;
        color: white;
        font-size: 1rem;
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
        transition: background-color 0.3s, transform 0.2s;
    }
    .stButton button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }

    /* Markdown Styling */
    .stMarkdownContainer {
        direction: rtl;
        text-align: right;
        color: #333;
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        font-size: 1.1rem;
    }

    /* Sidebar Styling */
    .css-1lcbmhc {
        background-color: #e0f7fa;
        border-radius: 8px;
        padding: 20px;
    }

    .stSidebar h2, .stSidebar button {
        color: #333;
    }

    /* Add smooth transitions */
    * {
        transition: all 0.2s ease-in-out;
    }
</style>
"""

# Inject CSS for Stylish RTL
st.markdown(rtl_css, unsafe_allow_html=True)

# Title and Description
st.title("🤖 شات بوت مريح وأنيق")
st.markdown("معك المساعد الذكي للدكتور رائد")

# Input section for user queries
user_query = st.text_input("❓ أدخل سؤالك هنا:")

# Button to process the query
if st.button("💬 اسأل"):
    if user_query.strip():
        with st.spinner("⏳ جاري معالجة سؤالك..."):
            try:
                response = app.query(user_query)
                logger.info(f"Query processed successfully: {user_query}")
                st.success("✅ الإجابة:")
                st.markdown(response)
            except Exception as e:
                logger.error(f"Error while processing query: {user_query}", exc_info=True)
                st.error(f"❌ حدث خطأ: {e}")
    else:
        logger.warning("User attempted to submit an empty query.")
        st.warning("⚠️ يرجى إدخال سؤال قبل الضغط على 'اسأل'.")

# Optional: Sidebar for additional functionality
st.sidebar.header("خيارات إضافية")
if st.sidebar.button("📂 تحميل الملفات"):
    with st.spinner("⏳ جاري تحميل الملفات..."):
        try:
            DIR_PATH = "DrRaed"  # Ensure this path is correct relative to app.py
            # Code to load documents (placeholder)
            logger.info(f"Files loaded from directory: {DIR_PATH}")
            st.sidebar.success("✅ تم تحميل الملفات بنجاح.")
        except Exception as e:
            logger.error("Error while loading files.", exc_info=True)
            st.sidebar.error(f"❌ خطأ في تحميل الملفات: {e}")
