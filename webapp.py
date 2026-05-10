from flask import Flask, request, jsonify, render_template_string
import anthropic

app = Flask(__name__)
import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))


HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Crystal</title>
    <style>
        body { 
            font-family: Arial; 
            max-width: 800px; 
            margin: 50px auto; 
            padding: 20px;
            background: linear-gradient(135deg, #f8c8d4, #81d8d0);
            min-height: 100vh;
        }
        h1 {
            text-align: center;
            color: white;
            text-shadow: 1px 1px 4px rgba(0,0,0,0.2);
            font-size: 2em;
            margin-bottom: 20px;
        }
        #chat { 
            height: 500px; 
            overflow-y: auto; 
            background: rgba(255,255,255,0.85);
            padding: 20px; 
            margin-bottom: 20px; 
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .user { text-align: right; margin: 10px 0; }
        .assistant { text-align: left; margin: 10px 0; }
        .bubble { display: inline-block; padding: 10px 15px; border-radius: 15px; max-width: 70%; }
        .user .bubble { background: #81d8d0; color: white; }
        .assistant .bubble { background: #f8c8d4; color: #333; }
        #input { 
            width: 75%; 
            padding: 12px 18px; 
            border-radius: 25px; 
            border: none;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            font-size: 1em;
        }
        button { 
            padding: 12px 22px; 
            background: #81d8d0; 
            color: white; 
            border: none; 
            border-radius: 25px; 
            cursor: pointer;
            font-size: 1em;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        button:hover { background: #5ec8bf; }
    </style>
</head>
<body>
    <h1>Crystal</h1>
    <div id="chat"></div>
    <input id="input" placeholder="Type a message..." onkeypress="if(event.key==='Enter') send()">
    <button onclick="send()">Send</button>
    <script>
        let history = [];
        async function send() {
            const input = document.getElementById("input");
            const msg = input.value.trim();
            if (!msg) return;
            input.value = "";
            addMessage("user", msg);
            history.push({role: "user", content: msg});
            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({history})
            });
            const data = await res.json();
            addMessage("assistant", data.reply);
            history.push({role: "assistant", content: data.reply});
        }
        function addMessage(role, text) {
            const chat = document.getElementById("chat");
            chat.innerHTML += `<div class="${role}"><span class="bubble">${text}</span></div>`;
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
</body>
</html>
'''

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    history = request.json["history"]
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system="You are a helpful AI assistant named Crystal. Be concise and friendly.",
        messages=history
    )
    return jsonify({"reply": response.content[0].text})

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=int(__import__("os").environ.get("PORT", 5000)))