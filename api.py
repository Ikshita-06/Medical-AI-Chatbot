from flask import Flask, request, jsonify
from flask_cors import CORS
from router import process_query 

app = Flask(__name__)
CORS(app) # Allows React to connect safely

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_query = data.get("message", "")
    
    # Passes the message to your existing router logic
    bot_response = process_query(user_query)
    
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    print("✅ Web API Started! React can now connect.")
    app.run(port=5000, debug=True, use_reloader=False)