from flask import Flask, render_template, jsonify
from PIL import Image

import numpy as np

import os

app = Flask(__name__)

# Конфигурация
STEP = 30  # Должен соответствовать значению в static/js/main.js
WIDTH, HEIGHT = 960, 720


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_data/<int:frame_index>')
def get_frame(frame_index):
    try:
        img_path = f'static/img/frames/frame_{frame_index}.jpg'  # <--- path to frames
        img = Image.open(img_path)
        pixel_array = np.array(img)
        cols, rows = WIDTH // STEP, HEIGHT // STEP
        colors = pixel_array[::STEP, ::STEP]
        
        return jsonify({
            "cols": cols,
            "rows": rows,
            "colors": colors.tolist()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 404


if __name__ == '__main__':
    app.run(threaded=True, debug=True)
