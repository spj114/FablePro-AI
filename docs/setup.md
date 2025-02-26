# FablePro AI - Setup Guide

## 📌 Prerequisites
Ensure you have the following installed:
- **Python 3.8+**
- **pip** (comes with Python)
- **Google Gemini API Key**

## 🔹 Step 1: Clone the Repository
Open **Command Prompt (CMD)** and run:
```cmd
git clone https://github.com/yourusername/FablePro-AI.git
cd FablePro-AI
```

## 🔹 Step 2: Create & Activate Virtual Environment
Create a virtual environment to keep dependencies isolated:
```cmd
python -m venv venv
venv\Scripts\activate
```

## 🔹 Step 3: Install Dependencies
Once the virtual environment is activated, install required packages:
```cmd
pip install -r requirements.txt
```
After installing requirements,  download the language model:
```cmd
python -m spacy download en_core_web_sm
```

## 🔹 Step 4: Set Up Google Gemini API
1. Go to [Google AI](https://ai.google.dev/) and generate an API key.
2. Create a `.env` file in the project folder:
   ```cmd
   type NUL > .env
   ```
3. Open `.env` in a text editor and add:
   ```env
   GEMINI_API_KEY=your_api_key_here
   ```

## 🔹 Step 5: Run the Application
Start the chatbot interface using Streamlit:
```cmd
streamlit run characterbot.py
```

Your FablePro AI should now be running locally in your browser at http://localhost:8501!

## 🔹 Troubleshooting
- If you get errors about missing packages, try reinstalling from requirements.txt
- Make sure your API key is correctly set in the .env file
- If you have issues with spaCy, try running: `python -m spacy validate`
