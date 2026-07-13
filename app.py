from flask import Flask, render_template, redirect, session, request
from groq import Groq
from dotenv import load_dotenv
from rag import chunk_text, score_chunks
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "randomstringofintegers"
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

@app.route('/', methods=['GET', 'POST'])
def home():

    if "history" not in session:
        session["history"] = [{"role": "system", "content": "You are a helpful study assistant. Answer questions clearly and concisely."}]
      

    if request.method == "POST":
        
        message = request.form["message"]
        file = request.files["file"]
        
        if file.filename:

            text = file.read()
            clean_text = text.decode("utf-8")
            
            chunks = chunk_text(clean_text)
            
            relevant_info = score_chunks(chunks, message)
            
            session["history"][0]["content"] = f"You are a helpful study assistant. Answer questions clearly and concisely. Use the relevant information to better help the user: {relevant_info}"

        session["history"].append({"role": "user", "content": message})

        chat_completion = client.chat.completions.create(
            messages= session["history"],
            model="llama-3.3-70b-versatile",
        )
        
        result = chat_completion.choices[0].message.content
        session["history"].append({"role": "assistant", "content": result})
        session.modified = True

        return render_template('index.html', history = session["history"])
    
    return render_template('index.html', history = session["history"])


if __name__ == '__main__':
        app.run(debug=True)