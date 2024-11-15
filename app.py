# -*- coding: utf-8 -*-
"""
Streamlit Chatbot Application with Stylish RTL Design
"""

import os
import streamlit as st

os.environ["LD_LIBRARY_PATH"] = "./bin"

os.environ["OPENAI_API_KEY"]  = st.secrets["OPENAI_API_KEY"]
x = st.secrets["OPENAI_API_KEY"]
print(f"Hello >>> OPENAI_API_KEY >> {x}")

try:
    import pysqlite3
    print("pysqlite3 installed successfully.")
except ImportError:
    raise RuntimeError("pysqlite3 is not installed. Please use a supported environment.")
    
    
from embedchain import App


# Initialize EmbedChain application
app = App()

# Function to load data (if applicable, from documents)
# def load_documents(directory_path):
#     for filename in os.listdir(directory_path):
#         file_path = os.path.join(directory_path, filename)
#         if os.path.isfile(file_path):
#             app.add(file_path)

# Streamlit UI
st.set_page_config(
    page_title="🤖 اسأل الدكتور الرائد",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# Custom CSS for Stylish and Cozy RTL Layout
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
st.markdown("معك المساعد الذكي للدكتور رائد ")

# Input section for user queries
user_query = st.text_input("❓ أدخل سؤالك هنا:")

# Button to process the query
if st.button("💬 اسأل"):
    if user_query.strip():
        with st.spinner("⏳ جاري معالجة سؤالك..."):
            # Query the RAG-based model
            try:
                response = app.query(user_query)
                st.success("✅ الإجابة:")
                st.markdown(response)
            except Exception as e:
                st.error(f"❌ حدث خطأ: {e}")
    else:
        st.warning("⚠️ يرجى إدخال سؤال قبل الضغط على 'اسأل'.")

# Optional: Sidebar for additional functionality
st.sidebar.header("خيارات إضافية")
if st.sidebar.button("📂 تحميل الملفات"):
    with st.spinner("⏳ جاري تحميل الملفات..."):
        try:
            DIR_PATH = "DrRaed"  # Ensure this path is correct relative to app.py
            
            st.sidebar.success("✅ تم تحميل الملفات بنجاح.")
        except Exception as e:
            st.sidebar.error(f"❌ خطأ في تحميل الملفات: {e}")
