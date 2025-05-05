import os
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import tempfile
from algorithm import *
from Crypto.Hash import SHA256

app = Flask(__name__)
app.secret_key = 'hazwanravanza'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
KEY_FOLDER = os.path.join('static', 'keys')
os.makedirs(KEY_FOLDER, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate')
def generate_key():
    return render_template('generate.html')

@app.route('/sign')
def sign_file():
    return render_template('sign.html') 
    
@app.route('/verify')
def verify_file():
    return render_template('verify.html')

@app.route('/generate_keys', methods=['POST'])
def generate_keys_route():
    size = request.get_json()
    key_size = int(size.get('key_size'))
    key_data = PembangkitanKunciRSA(key_size)

    private_key_path = os.path.join(KEY_FOLDER, 'private.pem')
    public_key_path = os.path.join(KEY_FOLDER, 'public.pem')

    with open(private_key_path, 'w') as priv:
        priv.write(key_data["privateKey"])
    with open(public_key_path, 'w') as pub:
        pub.write(key_data["publicKey"])

    return jsonify(key_data)

@app.route('/sign_generic_file', methods=['POST'])
def sign_generic_file():
    file = request.files['genericFile']
    data = file.read()

    key_path = None

    if 'privateKeyText' in request.form and request.form['privateKeyText'].strip():
        private_key = request.form['privateKeyText']
        temp_key_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
        with open(temp_key_path.name, 'w') as f:
            f.write(private_key)
        key_path = temp_key_path.name
    elif 'privateKeyFile' in request.files:
        private_key_file = request.files['privateKeyFile']
        filename = secure_filename(private_key_file.filename)
        key_path = os.path.join(tempfile.gettempdir(), filename)
        private_key_file.save(key_path)
    else:
        return jsonify({"success": False, "message": "Private key tidak ditemukan!"}), 400

    signature = menandatangani(data.decode('latin1'), key_path)

    temp_sig = tempfile.NamedTemporaryFile(delete=False, suffix=".sig")
    with open(temp_sig.name, 'wb') as f:
        f.write(signature)

    return send_file(temp_sig.name, as_attachment=True, download_name='signature.sig')


@app.route('/verify_generic_file', methods=['POST'])
def verify_generic_file():
    original_file = request.files['original_file']
    signature_file = request.files['signature_file']
    data = original_file.read()
    signature = signature_file.read()

    public_key = None
    temp_key_path = None

    if 'publicKeyText' in request.form and request.form['publicKeyText'].strip():
        public_key = request.form['publicKeyText']
        temp_key_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
        with open(temp_key_path.name, 'w') as f:
            f.write(public_key)
    elif 'publicKeyFile' in request.files and request.files['publicKeyFile'].filename != '':
        public_key_file = request.files['publicKeyFile']
        temp_key_path = tempfile.NamedTemporaryFile(delete=False, suffix='.pem')
        public_key_file.save(temp_key_path.name)
    else:
        return jsonify({"success": False, "message": "Public key tidak ditemukan!"}), 400

    result = memverifikasi(signature, data.decode('latin1'), temp_key_path.name)

    if result:
        return jsonify({"success": True, "message": "Tanda tangan valid!"})
    else:
        return jsonify({"success": False, "message": "Tanda tangan tidak valid!"})
