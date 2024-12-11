from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from rembg import remove
from PIL import Image, ImageOps
import os

app = Flask(__name__)

# Folder untuk menyimpan gambar
UPLOAD_FOLDER = './static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Memastikan folder upload ada
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Ambil file dari form
        file = request.files['image']
        if file:
            filename = file.filename
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], 'input_' + filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output_' + filename)

            # Simpan file input
            file.save(input_path)

            # Hapus latar belakang
            input_image = Image.open(input_path)
            input_image = input_image.convert("RGBA")  # Pastikan mode RGBA
            output_image_data = remove(input_image)

            # Terapkan latar belakang transparan checkerboard
            checkerboard = Image.new("RGBA", input_image.size, (0, 0, 0, 0))
            output_image = Image.alpha_composite(checkerboard, output_image_data)

            # Simpan file output
            output_image.save(output_path, format="PNG")

            # Redirect ke halaman utama dengan parameter hasil
            return redirect(url_for('index', input_image='input_' + filename, output_image='output_' + filename))

    # Ambil parameter input dan output dari URL
    input_image = request.args.get('input_image')
    output_image = request.args.get('output_image')
    return render_template('index.html', input_image=input_image, output_image=output_image)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
