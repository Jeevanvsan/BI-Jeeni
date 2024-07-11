from flask import Flask, render_template, request , send_from_directory, redirect, url_for,flash,jsonify,send_file
from flask_cors import CORS
from utils.html_create import html_generate
from utils.meta_combiner import meta_combiner
from utils.graph_overview import create_graph_overview
from utils.doc_create_overview import doc_generator_overview
import zipfile
import os
import main
import shutil
import csv
import random
import re
import multiprocessing
import yaml
import webbrowser


app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = ['pbit','xlr']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'secret'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app._static_folder = "static"
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

with open('utils/helper/tips.csv', mode='r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    csv_data = list(csv_reader)

@app.route('/get_random_row')
def get_random_row():
    random_row = random.choice(csv_data)
    return random_row

@app.route('/')
def index():
    out = 'output'
    file_list = None
    subfolders = [f.path for f in os.scandir(out) if f.is_dir()]
    for subfolder in subfolders:
        shutil.rmtree(subfolder)
    out = 'static/img/layout'
    if os.path.exists(out):
        shutil.rmtree(out)
    if os.path.exists('static/img/report'):
        shutil.rmtree('static/img/report')
    if os.path.exists('loads'):
        shutil.rmtree('loads')
    if os.path.exists('loads') is False:
        os.mkdir('loads')
    if os.path.exists('uploads'):
        shutil.rmtree('uploads')
    if os.path.exists('templates'):
        shutil.rmtree('templates')

    shutil.copytree(f'temp_', 'templates')


    if os.path.exists('uploads') is False:
        os.mkdir('uploads')
    
    with open('output/overview.yaml','w') as f:
        yaml.safe_dump([],f)

    return render_template('index.html',page='main')

@app.route('/upload1/<file>', methods=['GET'])
def upload_file(file):
    if file == '':
        flash("No file found !")
    if 'xlr' in file.split('.')[1]:
        return jsonify({"type": "xlr", "file": file})            
    else:
        flash("Unsupported file !")
    return redirect(url_for('index'))

def get_name(file):
    # # print("reached")
    rtn = data_extract(file)

    if rtn:
        if os.path.exists(f"output/{file.split('.')[0]}/html") == False:
            os.mkdir(f"output/{file.split('.')[0]}/html")
        image_generate(file)
        html_generater(file)
        zip_generate(file)
        graph_generate(file)
    
@app.route('/startrunning',methods=['POST'])
def start_running():
    files = request.json
    pool_size = 5
    with open('output/file_list.yaml', 'w') as f:
        yaml.safe_dump(files, f)
    # # print(files)

    pool = multiprocessing.Pool(pool_size)
    pool.map(get_name, files)

    # with multiprocessing.Pool(pool_size) as pool:
    #     pool.map(get_name, files)

    pool.close()
    pool.join()
   
    return jsonify({"status":"done"})


@app.route('/uploadpbit',methods=['POST'])
def upload_pbit():
    files = request.files.getlist("file")
    rtn = False
    file_names = []

    out = 'output'
    file_list = None
    subfolders = [f.path for f in os.scandir(out) if f.is_dir()]
    for subfolder in subfolders:
        shutil.rmtree(subfolder)
        
    out = 'static/img/layout'
    if os.path.exists(out):
        shutil.rmtree(out)
    if os.path.exists('static/img/report'):
        shutil.rmtree('static/img/report')
    if os.path.exists('loads'):
        shutil.rmtree('loads')
    if os.path.exists('loads') is False:
        os.mkdir('loads')
    if os.path.exists('uploads'):
        shutil.rmtree('uploads')
    if os.path.exists('uploads') is False:
        os.mkdir('uploads')

    with open('output/overview.yaml','w') as f:
        yaml.safe_dump([],f)

    for file in files:
        file_names.append(file.filename)
        zip_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(zip_path)
        ob = main.extract_bi(file.filename)
        rtn = True

    if rtn:
        return jsonify({"type": "pbit", "file": file_names,"status":"done","fn": "pbit_up"})
    else:
        return jsonify({"type": "pbit", "file": file_names,"status":"fail","fn": "pbit_up"})

# @app.route('/data_extr',methods=['POST'])
def data_extract(file):
    # file = request.files["file"]
    # # print(file.filename)
    ob = main.extract_bi(file)
    ob.data_extract(file)
    return True
    # return jsonify({"type": "pbit", "file": file.filename,"status":"done","fn": "data extract"})

# @app.route('/image_generate',methods=['POST'])
def image_generate(file):
    # file = request.files["file"]
    # # print(file.filename)
    ob = main.extract_bi(file)
    ob.image_create(file)
    return True
    # return jsonify({"type": "pbit", "file": file.filename,"status":"done","fn": "image create"})
    
# @app.route('/html_generate',methods=['POST'])
def html_generater(file):
    # file = request.files["file"]
    # # print(file.filename)
    ob = main.extract_bi(file)
    ob.html_create(file)
    return True
    # return jsonify({"type": "pbit", "file": file.filename,"status":"done","fn": "html create"})

# @app.route('/zip_generate',methods=['POST'])
def zip_generate(file):
    # file = request.files["file"]
    # # print(file.filename)
    ob = main.extract_bi(file)
    ob.zip_create(file)
    return True
    # return jsonify({"type": "pbit", "file": file.filename,"status":"done","fn": "zip create"})

# @app.route('/graph_generate',methods=['POST'])
def graph_generate(file):
    # file = request.files["file"]
    # # print(file.filename)
    ob = main.extract_bi(file)
    ob.graph_create(file)
    return True
    # return jsonify({"type": "pbit", "file": file.filename,"status":"done","fn": "graph create"})

@app.route('/main/<file>',methods = ['GET'])
def main_view(file):
    file = file.replace(".pbit","")
    filled = request.args.get('filled')
    if filled is None:
        filled = False   
    # file = request.files['file'] 
    download_link = f'/download/{file}'
    return redirect(url_for('main_show',download_link=download_link,file=file))

@app.route('/main_show',methods = ['GET'])
def main_show():
    download_link = request.args['download_link']
    file = request.args['file']
    return render_template('main.html',download_link=download_link,file=file)

@app.route('/main_file',methods = ['POST'])
def main_():
    filled = request.args.get('filled')
    if filled is None:
        filled = False   
    file = request.files['file'] 
    meta_combiner.run()
    ov_graph = create_graph_overview()
    ov_graph.run()
    ov_doc = doc_generator_overview()
    ov_doc.run()
    return redirect(url_for('main_file_show',file=file.filename))

@app.route('/download-overview-doc')
def download_overview_doc():
    # download_link = request.args['download_link']
    path = 'output/BIx Overview.docx'
    return send_file(path, as_attachment=True, download_name="BIx Overview.docx")

@app.route('/main_file_show')
def main_file_show():
    # download_link = request.args['download_link']
    file = request.args['file']
    return render_template('files.html')
    # return render_template('main.html',download_link=download_link,file=file)

@app.route('/overview_lineage')
def overview_lineage():
    return render_template('lineage.html')

@app.route('/upload/<file>', methods=['GET'])
def load_data(file):
    if os.path.exists('loads') is False:
        os.mkdir('loads')
    path = os.path.join(os.path.expanduser('~'), 'Documents')

    with zipfile.ZipFile(f'{path}/BIX/{file}', 'r') as f:
        f.extractall('loads')
    file = file.split(".")[0]
    source_folder = [f'{file}',f'{file}_extract','zip']
    destination_folder = 'output'

    for folder in source_folder:
        if os.path.exists(f'{destination_folder}/{folder}'):
            shutil.rmtree(f'{destination_folder}/{folder}')
        shutil.copytree(f'loads/{folder}', f'{destination_folder}/{folder}')

    if os.path.exists('static/img/layout'):
        shutil.rmtree('static/img/layout')
    shutil.copytree(f'loads/{file}/img/layout', 'static/img/layout')
    shutil.copytree(f'loads/{file}/img/report', 'static/img/report')
    source_folder = 'loads'
    destination_folder = 'templates'
    file_list = ['page_1.html', 'reports.html', 'sample.html','schema.html','tree_structure.html','visual_data.html','visuals.html']

    for file_name in file_list:
        source_path = os.path.join(source_folder, file_name)
        destination_path = os.path.join(destination_folder, file_name)
        shutil.copy2(source_path, destination_path)
    return 'done'

@app.route('/uploads/<file>', methods=['GET'])
def upload_file_s(file):
    flash("The file has been saved to the Documents/BIX folder.")
    if file and allowed_file(file):
        download_link = f'/download/{file}'
        return render_template('main.html',download_link=download_link,file=file)
    return 'Invalid file type'

# @app.route('/download/<file>')
# def download_file(file):
#     file = file.split('.')[0]
#     return send_from_directory(os.path.join('output','zip'), f'{file}.zip', as_attachment=True)

@app.route('/preview/page/<filename>/<report>')
def visuals(filename,report):
    ob_html = html_generate()
    ob_html.visuals(filename,report)
    return render_template(f'{filename}_visuals.html', report = report)

@app.route('/preview/page/<filename>/<report>/<visual>/<id>')
def data(filename,report,visual,id):
    ob_html = html_generate()
    ob_html.data(filename,report,id)
    return render_template(f'{filename}_visual_data.html')

@app.route('/preview/page/<filename>/<report>/report-settings')
def report_settings(filename,report):
    ob_html = html_generate()
    ob_html.report_settings(filename,report)
    return render_template(f'{filename}_report_settings.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/download/<file>')
def download(file):
    return render_template('download.html',file=file)

@app.route('/download_val/<file>', methods = ['POST'])
def download_val(file):
    data = request.form.getlist('down')
    selected_files = []
    if "L" in data:
        selected_files.append("img/layout")
    if "D" in data:
        selected_files.append(f'{file.split(".")[0]}.docx')
    if "Y" in data:
        selected_files.append("data_structure.yaml")   
    if "G" in data:
        selected_files.append("lineage.html")   
    if "R" in data:
        selected_files.append("img/report")

    if selected_files:
        # # print(selected_files)
        file = re.sub(".pbit","",file)
        file = re.sub(".xlr","",file)
        if os.path.isdir(f'output/zip') is False:
            os.mkdir(f'output/zip')

        directory_path = f'output/{file}'
        zip_filename = f'{file}.zip'
        zip_path = f'output/zip/{file}.zip'
        with zipfile.ZipFile(f'output/zip/{file}.zip', 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(directory_path):
                # # print(foldername)

                for filename in filenames:
                    if f"output/{file}\img\layout" in foldername and "img/layout" in selected_files:
                        file_path = f"{foldername}/{filename}"
                        arcname = os.path.relpath(file_path, directory_path)
                        zipf.write(file_path, arcname)
                    
                    if f"output/{file}\img\Report" in foldername and "img/report" in selected_files:
                        # # print(121)
                        file_path = f"{foldername}/{filename}"                        
                        arcname = os.path.relpath(file_path, directory_path)
                        zipf.write(file_path, arcname)
                        
                    if filename in selected_files :
                        file_path = f"{foldername}/{filename}"
                        arcname = os.path.relpath(file_path, directory_path)
                        zipf.write(file_path, arcname)
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
        
    else:
        flash("Select at least one file !")
        return render_template('download.html',file=file)
    


@app.route('/lineage/<file>')
def lineage(file):
    return render_template(f'{file}_lineage.html', src= f"{file}/lineage.html")


@app.route('/preview/<file>')
def preview(file):
    return render_template(f'{file}_reports.html')

@app.route('/save/<file>',methods = ['GET'])
def save(file):
    file1 = file.split('.')[0]
    path = os.path.join(os.path.expanduser('~'), 'Documents')

    if os.path.isdir(f'{path}/BIX') is False:
            os.mkdir(f'{path}/BIX')

    folder1_name = 'output'
    folder2_name = 'templates'

    output_zip_path = f'{path}/BIX/{file1}.xlr'
    zip_folders(folder1_name, folder2_name, output_zip_path)
    return redirect(url_for('upload_file_s',file = file))

def zip_folders(folder1_path, folder2_path, output_zip_path):
    with zipfile.ZipFile(output_zip_path, 'w') as zip_file:
        for root, dirs, files in os.walk(folder1_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder1_path)
                zip_file.write(file_path, arcname)

        for root, dirs, files in os.walk(folder2_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder2_path)
                zip_file.write(file_path, arcname)
    
@app.route('/preview/page/<filename>/schema')
def schema(filename):
    ob_html = html_generate()
    ob_html.schema(filename)
    return render_template(f'{filename}_schema.html')

def unzip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(os.path.join(app.config['UPLOAD_FOLDER'], 'unzipped'))

if __name__ == '__main__':
    webbrowser.open_new_tab('http://127.0.0.1:5001/')
    app.run(debug=False,port = 5001)