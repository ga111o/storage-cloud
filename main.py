from flask import Flask, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
import os
from collections import defaultdict

BASE_UPLOAD_FOLDER = 'directory'
FOLDERS = ['share', 'test', 'backup']

app = Flask(__name__)

def list_files(directory):
    files_dict = defaultdict(list)
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            relative_path = os.path.relpath(path, directory)
            dir_name = os.path.dirname(relative_path)
            files_dict[dir_name].append(file)
    return dict(files_dict)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files or 'folder' not in request.form:
            return redirect(request.url)
        file = request.files['file']
        folder = request.form['folder']
        if file.filename == '':
            return redirect(request.url)

        filename = secure_filename(file.filename)
        upload_folder_path = os.path.join(BASE_UPLOAD_FOLDER, folder)
        os.makedirs(upload_folder_path, exist_ok=True)
        file.save(os.path.join(upload_folder_path, filename))

    all_files_and_dirs=list_files(BASE_UPLOAD_FOLDER)
    files_list_html =''    

    for dir_name, file_names in all_files_and_dirs.items():
        if dir_name == '':
            for filename in file_names:
                files_list_html += f'<li>{filename}</li>'    
        else:
            details_block=f'''
                <details>
                    <summary>{dir_name}</summary>
                    <ul>'''
            for filename in file_names:
                details_block += f'<li>{filename}</li>'
            details_block += '''
                    </ul>
                </details>'''
            if details_block not in files_list_html:
                files_list_html+=details_block
                
    folders_options_html =''
    
    for folder_name in FOLDERS:
         folders_options_html += f'<option value="{folder_name}">{folder_name}</option>'

    return f'''
     <!doctype html>
     <title>Upload File</title>
     <h1>Upload File</h1>
      <form method=post enctype=multipart/form-data>
       Select a folder: 
       <select name=folder>{folders_options_html}</select><br/>
       Select a file to upload: 
       <input type=file name=file><br/>
       <input type=submit value=Upload>
      </form>
      Uploaded Files:<br/>
      {files_list_html}
     '''

if __name__ == '__main__':
     app.run(debug=True)