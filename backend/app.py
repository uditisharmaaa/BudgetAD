from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from parser import parse_fab_html
from analysis import plot_all_charts


app = Flask(__name__)
CORS(app)


UPLOAD_FOLDER = 'uploads'
STATIC_FOLDER = 'static'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)


@app.route('/upload', methods=['POST'])
def upload_file():
   if 'file' not in request.files:
       return jsonify({'error': 'No file uploaded'}), 400


   file = request.files['file']
   file_path = os.path.join(UPLOAD_FOLDER, file.filename)
   file.save(file_path)


   try:
       df = parse_fab_html(file_path)
       if df is None or df.empty:
           return jsonify({'error': 'Invalid HTML file or no data found'}), 400


       image_filenames, years = plot_all_charts(df, STATIC_FOLDER)


       return jsonify({
           'status': 'success',
           'images': image_filenames,
           'years': list(map(int, years))
       })


   except Exception as e:
       print('❌ Error during file processing:', e)
       return jsonify({'error': str(e)}), 500


@app.route('/static/<path:filename>')
def static_files(filename):
   return send_from_directory(STATIC_FOLDER, filename)


if __name__ == '__main__':
   app.run(debug=True, port=5002)



