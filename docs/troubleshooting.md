# Troubleshooting Guide

### ❌ Issue: "Google API Key Not Found"
**Fix:**  
- Ensure `.env` file contains: `GEMINI_API_KEY=your_api_key_here`
- Verify the API key is valid and has not expired
- Restart your terminal and the application after making changes

### ❌ Issue: "FAISS Index Not Found"
**Fix:**  
- Ensure you've uploaded and processed a book before chatting
- Check that the book was successfully processed (look for the success message)
- Verify the `book_embeddings.faiss` file exists in your project directory

### ❌ Issue: "spaCy Model Not Found"
**Fix:**  
- Run: `python -m spacy download en_core_web_sm`
- Restart the application

### ❌ Issue: "Response Not Visible in Chat"
**Fix:**  
- Try running: `streamlit run characterbot.py`
- Clear your browser cache or try a different browser
- Check your internet connection (needed for API calls)

### ❌ Issue: "No Characters Detected"
**Fix:**  
- Try with a different PDF that has clearer text
- If needed, manually enter character names in the text input field