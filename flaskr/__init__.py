import os
from pymongo import MongoClient
from datetime import datetime
from flask import Flask, request, redirect, url_for, session, render_template
from .gpt3chat import chat_with_gpt3_5 
from .dalle import dalleapp
from flask import jsonify
from urllib.parse import urlparse
from bson.binary import Binary
conversation = []
client = MongoClient('mongodb://localhost:27017/')
db = client['mydatabase']
collection = db['mycollection']
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',  # In production, use a more secure key
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    

    @app.route('/get_new_messages/<int:last_index>', methods=['GET'])
    def get_new_messages(last_index):
        conversation = session.get('conversation', [])
        new_messages = conversation[last_index:]
        return jsonify(new_messages=new_messages, new_last_index=len(conversation))
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            key = request.form['key']
            if len(list(collection.find({"key":key}))) >0: 
                session['key'] = key
                session['conversation'] = session.get('conversation', [{ "content": "Hello, How can I assist you today?","role": "system"}])
                return redirect(url_for('dashboard'))
            else:
                return 'Invalid credentials'
        return render_template('login.html')

    @app.route('/dashboard')
    def dashboard():
        if 'key' not in session:
            return redirect(url_for('login'))
        return render_template('dashboard.html')

    @app.route('/gpt3_chat', methods=['GET', 'POST'])
    def gpt3_chat():
        if 'key' not in session:
            return redirect(url_for('login'))
        conversation = session.get('conversation', [{ "content": "Hello, How can I assist you today?","role": "system"}])
        session['conversation'] = conversation 

        output_type = "text"  # Default to text
        output_content = None
        new_messages = []
        if request.method == 'POST':
            user_input = request.form['prompt']
            conversation.append({"content": user_input,"role": "user"})

        # Logic to decide whether to call GPT-3.5 or DALL-E
            if "show me an image of" in user_input.lower():
                output_type = "image"
                output_content = dalleapp(user_input)  # Replace with your DALL-E function
                conversation.append({"content": Binary(output_content),"role": "assistant"})
            else:
                output_type = "text"
                new_conversation = [{"content": "You are a helpful assistant.","role": "system"}, {"content": user_input,"role": "user"}]
                new_conversation = chat_with_gpt3_5(user_input, new_conversation)
                output_content = new_conversation[-1]['content']
                conversation.append({"content": output_content,"role": "assistant"})
            if len(conversation) > 1:
                new_messages.append(conversation[-2])
            if len(conversation) > 0:
                new_messages.append(conversation[-1])
            session['conversation'] = conversation
        return render_template('gpt3_chat.html', 
                            new_messages=new_messages,
                            output_type=output_type,
                            output_content=output_content,
                            conversation=conversation)
    @app.route('/dalle', methods=['GET', 'POST'])
    def dalle():
        if 'key' not in session:
            return redirect(url_for('login'))
        if request.method == 'POST':
            prompt = request.form['prompt']
            # Assuming you have a function `call_dalle_api` to interact with DALL-E
            output = dalleapp(prompt)
            return render_template('dalle.html', output=output)
        return render_template('dalle.html')
    @app.route('/conversation_history', methods=['GET', 'POST'])
    def conversation_history():
        if 'key' not in session:
            return redirect(url_for('login'))
    
        conversations = []
        query_result = collection.find_one({"key": session['key']})
        if query_result:
            conversations = query_result.get('conversation_history', [])
        
        return render_template('conversation_history.html', conversations=conversations)
    @app.route('/logout')
    def logout():
        if len(session['conversation'])>1:
            collection.update_one({"key": session['key']}, {"$push": {"conversation_history": {"Date":datetime.now(),"conversation":session['conversation']}}})
        session.clear()  # Clear session data
        return render_template('logout.html')

    @app.template_filter('is_image_url')
    def is_image_url(url):
        try:
            # Check if the string is a valid URL
            result = urlparse(url)
            if all([result.scheme, result.netloc]):
                # Check if the URL has an image extension
                return True
            return False
        except ValueError:
            return False

    app.jinja_env.filters['is_image_url'] = is_image_url

    @app.route('/image/<key>')
    def serve_image(key):
    # Fetch the image binary from MongoDB
        data = collection.find_one({'key': session['key']})
        if data and 'image' in data:
            return Response(data['image'], content_type='image') # Adjust content_type based on the image format
        else:
            return "No image found for the given key", 404

    return app