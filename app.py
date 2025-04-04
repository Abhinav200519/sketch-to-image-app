from flask import Flask, render_template, request, send_file
import requests
import os
from io import BytesIO
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CLIPDROP_API_KEY = os.getenv('CLIPDROP_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        if 'sketch' not in request.files:
            return "No sketch file provided", 400
        
        if 'prompt' not in request.form:
            return "No prompt provided", 400

        sketch = request.files['sketch']
        prompt = request.form['prompt']
        
        if not sketch or not prompt:
            return "Missing sketch or prompt", 400
        
        files = {'sketch_file': (sketch.filename, sketch.stream, sketch.content_type)}
        data = {'prompt': prompt}
        headers = {'x-api-key': CLIPDROP_API_KEY}
        
        response = requests.post(
            'https://clipdrop-api.co/sketch-to-image/v1/sketch-to-image',
            files=files,
            data=data,
            headers=headers
        )
        
        if response.ok:
            return send_file(BytesIO(response.content), mimetype='image/jpeg')
        else:
            return f"API Error: {response.text}", response.status_code
            
    except Exception as e:
        print(f"Error in generate endpoint: {str(e)}")
        return f"Server Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(debug=True)