from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form['video_url']
    save_path = request.form['save_path']

    if not video_url or not save_path:
        return jsonify({'message': 'Please enter a video URL and a save path.'}), 400

    try:
        response = requests.get(video_url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return jsonify({'message': f'Video downloaded to {save_path}'}), 200
        else:
            return jsonify({'message': f'Failed to download video. Status code: {response.status_code}'}), 400
    except Exception as e:
        return jsonify({'message': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
    