import os
import re
import yaml
import json
from zipfile import ZipFile
from utils.data_extractor import dataExtractor
from utils.layout_image import Image_generator
from utils.doc_create import doc_generator
from utils.html_create import html_generate
from utils.graph import create_graph
import time
import shutil

class extract_bi:
    def __init__(self,filename):
        self.input_file = filename
        self.extract_file(self.input_file)
        self.load_layout()
        self.load_schema()
        self.load_config()
        self.load_custom_data(filename)
        # self.check_version()
        # self.data_extract(filename)
        
    def extract_file(self,filename):
        self.extract_data = f'output/{re.sub(".pbit","",filename)}_extract'
        if os.path.isdir("output") is False:
            os.mkdir('output')
        with ZipFile(f'uploads/{filename}', 'r') as f:
            f.extractall(self.extract_data)

    def load_custom_data(self,filename):
        customs = {}
        # name = ""
        # author = ""
        # desc = ""
        path = f'output/{re.sub(".pbit","",filename)}_extract/Report/CustomVisuals'
        if os.path.exists(path):
            for subfolders in os.listdir(path):
                # path2 = f'output/{re.sub(".pbit","",filename)}_extract/Report/CustomVisuals/{subfolders}'
                path2 = f'output/{re.sub(".pbit","",filename)}_extract/Report/CustomVisuals/{subfolders}/resources'
                if os.path.exists(path2):
                    # with open(f'{path2}/package.json', 'r') as f:
                    with open(f'{path2}/{subfolders}.pbiviz.json', 'r',encoding="ISO-8859-1") as f:
                        data = json.loads(f.read())
                        # if "author" in data:
                        author = data["author"]["name"]
                        # if "name" in data:
                        name = data["visual"]["name"]
                        # if "description" in data:
                        desc = data["visual"]["description"]
                customs[subfolders] = {"name": name, "author": author, "desc": desc}
        self.customs = customs

    def load_layout(self):
        with open(f'{self.extract_data}/Report/Layout', 'r') as f:
            # self.layout_data = json.loads(bytes(f.read(),"ISO-8859-1"))
            self.layout_data = json.loads(bytes(f.read(),"utf8"))

    def load_config(self):
        with open("utils/configs/visual_config.yaml", 'r',encoding='utf-8') as f:
            self.config = yaml.safe_load(bytes(f.read(),"ISO-8859-1"))

    def load_schema(self):
        with open(f'{self.extract_data}/DataModelSchema', 'r') as f:
            self.schema_data = json.loads(bytes(f.read(),"ISO-8859-1"))

    def data_extract(self,file):
        file = re.sub(".pbit","",file)
        ob_ext = dataExtractor()
        ob_ext.run(self.layout_data,self.customs,self.schema_data,file)
        
    # def check_version(self):
        # data = self.schema_data
        # for ver in data["model"]["annotations"]:
        #     if "PBIDesktopVersion" in ver["name"]:
        #         # print(ver["value"].split(" ")[1].replace(".","").replace('(', '').replace(')', ''))
        #         ver_ = int(ver["value"].split(" ")[1].replace(".","").replace('(', '').replace(')', ''))
        #         if ver_ < self.config["version"] or ver_ == self.config["version"]:
        #             # print("version check : ",ver_,"< = ", self.config["version"])
        #             return True

    def image_create(self,file):
        file = re.sub(".pbit","",file)
        Image_generator.run(file)
        ob_doc = doc_generator(file)
        ob_doc.run()

    def html_create(self,file):
        file = re.sub(".pbit","",file)
        ob_html = html_generate()
        ob_html.files()
        ob_html.reports(file)

    def zip_create(self,file):
        file = re.sub(".pbit","",file)
        if os.path.isdir(f'output/zip') is False:
            os.mkdir(f'output/zip')
        directory_path = f'output/{file}'
        with ZipFile(f'output/zip/{file}.zip', 'w') as zipf:
            for foldername, subfolders, filenames in os.walk(directory_path):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(file_path, directory_path)
                    zipf.write(file_path, arcname)

    def graph_create(self,file):
        file = re.sub(".pbit","",file)
        ob_graph = create_graph(file)

if __name__ == '__main__':
    input_file = 's2.pbit'
    obj = extract_bi(input_file)
