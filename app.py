import os
import subprocess
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename
from processor import process_file# Make sure processor.py is in the same folder


app = Flask(__name__)

# Folder setup
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# ----------------- Existing functionality -----------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run/<script_name>', methods=['GET'])
def run_validation(script_name):
    print(f"Received validation request: {script_name}")

    # Map each button to its script
    scripts = {
        "name": r"C:\Users\skedare\Documents\workspace\python-project\script\name.py",
        "status": r"C:\Users\skedare\Documents\workspace\python-project\script\status.py",
        "category": r"C:\Users\skedare\Documents\workspace\python-project\script\category.py",
        "location": r"C:\Users\skedare\Documents\workspace\python-project\script\Location.py"
    }

    script_path = scripts.get(script_name)
    if not script_path:
        return jsonify(message="Invalid validation type."), 400

    try:
        # Run script and capture output
        result = subprocess.run(['python', script_path], capture_output=True, text=True)
        print("STDOUT:\n", result.stdout)
        print("STDERR:\n", result.stderr)

        return jsonify(message=result.stdout.strip() or "Validation completed.")
    except Exception as e:
        print(f"Error: {e}")
        return jsonify(message=f"Script execution failed: {str(e)}"), 500


def run_script(script_name):
    try:
        # Placeholder logic
        return jsonify({'message': f'{script_name.capitalize()} validation completed.'})
    except subprocess.CalledProcessError as e:
        return jsonify({'message': f'Error running {script_name}: {str(e)}'}), 500

# ----------------- New upload route -----------------

@app.route("/upload", methods=["POST"])
def upload_file():
    try:
        print("Received upload request")
        uploaded_file = request.files.get('file')
        action = request.form.get('process_type', 'default')
        print(f"Action: {action}")

        if not uploaded_file:
            print("No file part in request")
            return jsonify({"message": "No file uploaded"}), 400

        filename = secure_filename(uploaded_file.filename)
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(input_path)
        print(f"Saved input to: {input_path}")

        # Output file paths
        # output_path1 = os.path.join(OUTPUT_FOLDER, f"output1_{filename}")
        # output_path2 = os.path.join(OUTPUT_FOLDER, f"output2_{filename}")

        # # Call processor
        output_path1, output_path2 = process_file(action, input_path, app.config['OUTPUT_FOLDER'])
        # output_path2 = process_file(action + "_alt", input_path, app.config['OUTPUT_FOLDER'])
        # print(output_path1)
        # print(output_path2)

        # return jsonify({
        #     "message": "Files processed",
        #     "download1": f"/download/{os.path.basename(output_path1)}",
        #     "download2": f"/download/{os.path.basename(output_path2)}"
        # })
        # output1, output2 = process_file(input_path, app.config['OUTPUT_FOLDER'])
        # output_dir = os.path.join("outputs/", file_id)
        # Return paths for download
        # return jsonify({
        #     'output1':  os.path.join("outputs/", output1),
        #     'output2': os.path.join("outputs/", output2)
        # })
        # output_path1 = 
        return jsonify({
        'output1': output_path1.replace("outputs\\", ""),
        'output2': output_path2.replace("outputs\\", "")
    
       # 'output1': os.path.basename(output_path1),
        #'output2': os.path.basename(output_path2)
})

        
        # return jsonify({
        # 'output1': "output1_Sydney_Name.csv",
        # 'output2': "output2_Sydney_Name.csv"
        # })

    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"message": f"Error: {str(e)}"}), 500

# ----------------- Download route -----------------

@app.route("/download/<filename>")
def download_file(filename):
    full_path = os.path.join(OUTPUT_FOLDER, filename)
    print(f"Trying to serve file: {full_path}")
    
    if not os.path.exists(full_path):
        print("File not found!")
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=True)

# ----------------- Main entry -----------------

if __name__ == '__main__':
    app.run(debug=True)
   
