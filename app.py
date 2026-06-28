from flask import Flask, render_template, redirect, session, request
from groq import Groq
from dotenv import load_dotenv
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
        session['history'] = []

    if len(session["history"]) == 1:
        item = {"role": "system", "content": "You are a helpful study assistant. Answer questions clearly and concisely."}
        list.insert(0, item)

    if request.method == "POST":
         
        message = request.form["message"]
            
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