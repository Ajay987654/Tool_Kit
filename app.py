from flask import Flask, render_template, request, url_for
import os
from utils.file_converter import convert_file
from utils.video_downloader import download_video

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join("static", "downloads")
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Home
@app.route('/')
def index():
    return render_template("index.html")

# File Convert Route
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    target = request.form['target']

    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Convert file
        output_file = convert_file(filepath, target)
        file_url = url_for('static', filename='downloads/' + os.path.basename(output_file))

        return render_template("result.html", file_url=file_url)

    return "No file uploaded", 400

# Video Download Route
@app.route('/download_video', methods=['POST'])
def download_vid():
    url = request.form['url']
    quality = request.form['quality']

    try:
        output_file = download_video(url, quality, app.config['UPLOAD_FOLDER'])
        file_url = url_for('static', filename='downloads/' + os.path.basename(output_file))
        return render_template("result.html", file_url=file_url)
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
