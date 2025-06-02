from flask import Flask, request, jsonify
import face_recognition
import os
from supabase import create_client, Client
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure Supabase
SUPABASE_URL = 'https://otgiyovvviqcxpbqbekr.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im90Z2l5b3Z2dmlxY3hwYnFiZWtyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDg4NTQ1ODMsImV4cCI6MjA2NDQzMDU4M30.EU9yzGjMC6cuw_9k3gxp4fBWIMBGsfOL_NDMorDg240'
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

UPLOAD_FOLDER = 'known_faces'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Your recognition route
@app.route('/recognize', methods=['POST'])
def recognize():
    # 1. Receive and save image
    file = request.files['image']
    filename = secure_filename(file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    # 2. Perform face recognition
    # (your face recognition logic here)

    # 3. If user not recognized, return: {"status": "not_found"}
    # 4. If recognized, return user details

    return jsonify({'status': 'not_found'})  # Example

# Save user details to Supabase
@app.route('/register', methods=['POST'])
def register():
    data = request.form
    name = data['name']
    age = data['age']
    student_class = data['class']
    file = request.files['image']
    filename = secure_filename(file.filename)

    # Upload to Supabase Storage
    storage_response = supabase.storage().from_('users').upload(filename, file)

    # Get public URL
    public_url = supabase.storage().from_('users').get_public_url(filename)

    # Insert metadata
    supabase.table('users').insert({
        'name': name,
        'age': age,
        'class': student_class,
        'image_url': public_url
    }).execute()

    return jsonify({'status': 'saved'})
