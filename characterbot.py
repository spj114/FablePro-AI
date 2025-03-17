import os
import streamlit as st
import faiss
import numpy as np
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import google.generativeai as genai  
from langchain_google_genai import GoogleGenerativeAIEmbeddings  
import spacy
from collections import Counter

# Load API key
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Set the API key as an environment variable for langchain
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY

# Paths
VECTOR_DB_PATH = "book_embeddings.faiss"

# Initialize Google Generative AI Embeddings with explicit API key
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GEMINI_API_KEY
)

# Load spaCy model for character extraction
nlp = spacy.load("en_core_web_sm")

# Function to extract character names
def extract_characters(text, top_n=5):
    doc = nlp(text)
    character_names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return [name for name, _ in Counter(character_names).most_common(top_n)]

# Function to generate embeddings
def get_embedding(text):
    return np.array(embedding_model.embed_query(text))

# Function to split text into chunks
def split_text(text, chunk_size=500, overlap=100):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks

# Function to process uploaded PDF
def process_pdf(uploaded_file):
    pdf_reader = PdfReader(uploaded_file)
    text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])

    # Extract character names
    character_list = extract_characters(text)
    st.session_state["character_list"] = character_list

    # Split into chunks and generate embeddings
    text_chunks = split_text(text)
    embeddings = np.array([get_embedding(chunk) for chunk in text_chunks])

    # Store text chunks in session state
    st.session_state["text_chunks"] = text_chunks  

    # Store in FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, VECTOR_DB_PATH)
    
    st.success("✅ Book processed successfully! You can now chat with its characters.")

# Function to load FAISS index
def load_faiss_index():
    if os.path.exists(VECTOR_DB_PATH):
        return faiss.read_index(VECTOR_DB_PATH)
    return None

# Load index at startup
index = load_faiss_index()

# Function to retrieve relevant book passages
def retrieve_context(query, top_k=5):
    if "text_chunks" not in st.session_state:
        return "⚠️ No book data found. Please upload a book first."

    index = load_faiss_index()
    if index is None:
        return "⚠️ No book data found. Please upload a book first."

    query_embedding = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_embedding, top_k)

    retrieved_texts = []
    for i in range(top_k):
        if indices[0][i] != -1:
            retrieved_texts.append(st.session_state["text_chunks"][indices[0][i]])

    return "\n".join(retrieved_texts)

# Function to generate response
def generate_response(context, query, character):
    prompt = f"You are {character} from the book. Based on the following context, respond as {character} would:\n\n{context}\n\nUser: {query}\n{character}:"
    
    model = genai.GenerativeModel("gemini-1.5-pro-latest")  
    response = model.generate_content(prompt)
    return response.text if response else "Error: No response generated."

# 🎨 Apply Custom Styling
st.markdown("""
    <style>
        /* Background & Text */
        body { background-color: #f4f4f4; color: #333; }

        /* Page Title */
        .title { text-align: center; font-size: 32px; font-weight: bold; color: #4A4A4A; }

        /* Sidebar */
        .sidebar .sidebar-content { background-color: #EAEAEA; padding: 20px; border-radius: 10px; }

        /* Chat Input */
        .stTextArea textarea { font-size: 16px; }

        /* Success Message */
        .stAlert { border-radius: 10px; }

        /* Chat Output */
        .chat-message { 
            background-color: #222222; /* Change to dark gray */
            padding: 10px; 
            border-radius: 10px; 
            margin-top: 10px;
            color: white; /* Ensure text is visible */
        }
        .chat-character { color: #FFD700; font-weight: bold; } /* Gold color for character name */
    </style>
""", unsafe_allow_html=True)


# 🏛️ FablePro AI Header
st.markdown("<h1 class='title'>FablePro AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Step into the story. Talk to any character from your favorite books.</p>", unsafe_allow_html=True)

# 📂 File Upload
st.sidebar.header("📖 Upload Your Book (PDF)")
uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file and st.sidebar.button("📜 Process Book"):
    process_pdf(uploaded_file)

# 🎭 Character Selection
st.sidebar.header("🎭 Choose a Character")
if "character_list" in st.session_state and st.session_state["character_list"]:
    selected_character = st.sidebar.selectbox("Select a character:", st.session_state["character_list"])
else:
    selected_character = st.sidebar.text_input("Enter character name:", "Sherlock Holmes")

# 💬 Chat Section
st.markdown("### 💬 Chat with a Character")
user_input = st.text_area("Ask something from the book:", "")

if st.button("Send"):
    if not user_input:
        st.warning("Please enter a question or message.")
    elif "text_chunks" not in st.session_state:
        st.error("⚠️ Please upload and process a book first.")
    else:
        context = retrieve_context(user_input)
        response = generate_response(context, user_input, selected_character)
        
        # 🛠️ Ensure response is fully visible
        st.markdown(f"""
            <div class='chat-message'>
                <span class='chat-character'>{selected_character}:</span> 
                <p style='white-space: pre-wrap; font-size: 16px;'>{response}</p>
            </div>
        """, unsafe_allow_html=True)
