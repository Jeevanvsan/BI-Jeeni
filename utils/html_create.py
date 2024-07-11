from jinja2 import Environment, FileSystemLoader
import yaml

class html_generate:
    def __init__(self):
        pass
        # self.file = file
        # self.reports(file)
        # self.visuals(file)
    def files(self):
        # Create a Jinja environment
        env = Environment(loader=FileSystemLoader('utils/templates'))

        with open('output/file_list.yaml','r') as f:
            files = yaml.safe_load(f.read())
       
        template = env.get_template('jinja_files.html')
        output = template.render(files = files)


        with open(f'templates/files.html','w',encoding="utf-8")as f:
            f.write(output)

    def reports(self,file):
        # Create a Jinja environment
        env = Environment(loader=FileSystemLoader('utils/templates'))
        file = file
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)
        # Define some data
        reports = []
        
        for report in data['layout']:
            reports.append(report['report_name'])

        # items = ['Item 1', 'Item 2', 'Item 3']

        # Render the template with the data
        template = env.get_template('jinja_reports.html')
        output = template.render(reports = reports,filename = file)


        with open(f'output/{file}/html/{file}_reports.html','w',encoding="utf-8")as f:
            f.write(output)
        
        with open(f'templates/{file}_reports.html','w',encoding="utf-8")as f:
            f.write(output)

    def visuals(self,file,report_name):
        env = Environment(loader=FileSystemLoader('utils/templates'))
        file = file
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)

        src = "[[url_for('static',filename='img/layout/"+file+"/"+report_name+".png')]]"
        # src1 = "{{url_for('static',filename='img/{visuals[k]['visual_type']}.png')}}"
                    
        template = env.get_template('jinja_visuals.html')
        output = template.render(data = data['layout'], report = report_name, src = src) 

        with open(f'output/{file}/html/{file}_visuals.html','w',encoding="utf-8")as f:
            f.write(output)

        with open(f'templates/{file}_visuals.html','w',encoding="utf-8")as f:
            f.write(output)

    def schema(self,file):
        env = Environment(loader=FileSystemLoader('utils/templates'))
        file = file
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)            
        template = env.get_template('jinja_schema.html')
        output = template.render(schema = data['schema']['tables'],relations = data['schema']['relations'],filename = file,url_for='url_for' ) 

        with open(f'output/{file}/html/{file}_schema.html','w',encoding="utf-8")as f:
            f.write(output)
        
        with open(f'templates/{file}_schema.html','w',encoding="utf-8")as f:
            f.write(output)
    
    def report_settings(self,file,report_name):
        env = Environment(loader=FileSystemLoader('utils/templates'))
        file = file
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)    
        
        for reports in data['layout']:
            if report_name in reports['report_name']:
                canvas = reports["canvas_settings"][0]
                wallpaper = reports["wallpaper"][0]

        template = env.get_template('jinja_report_settings.html')
        output = template.render(file= file,report_name = report_name,wallpaper = wallpaper, canvas = canvas) 

        with open(f'output/{file}/html/{file}_report_settings.html','w',encoding="utf-8")as f:
            f.write(output)

        with open(f'templates/{file}_report_settings.html','w',encoding="utf-8")as f:
            f.write(output)

    def data(self,file,report_name,id):
        env = Environment(loader=FileSystemLoader('utils/templates'))
        file = file
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)    
        
        position = None
        title = None
        columns = None
        text = None
        name = None
        img_url = None
        ignore_list = ["x","y","legend","value","size","secondary_line","X","Y","Category","image_url","position","visual_type","column","id"]


        for reports in data['layout']:
            if report_name in reports['report_name']:
                for visuals in reports['visualContainers']:
                    for k,v in visuals.items():
                        if id in visuals[k]['id'] :
                            data = visuals[k]

                            data_keys = data.keys()
                            col_list = [vis_key for vis_key in data_keys if 'col_' in vis_key]
                            ignore_list = ignore_list + col_list

                            print(ignore_list)

                            position = visuals[k]['position']
                            visual = visuals[k]['visual_type']
                            if 'title' in visuals[k]:
                                if visuals[k]['title']:
                                    title = visuals[k]['title'].replace("'", "")
                            if col_list:
                                columns = col_list

                            if 'name' in visuals[k]:
                                name = visuals[k]['name']

                            if "image_url" in v:
                                img_url = v.get("image_url")

                            if 'text' in v:
                                txt = v["text"]
                                if txt:
                                    text = txt
                                
        

        template = env.get_template('jinja_visual_data.html')
        output = template.render(file= file,img_url=img_url,visual = visual,name=name,report_name = report_name,position=position,title = title,columns = columns,text = text,data = data,ig_list = ignore_list) 
        # output = template.render(file= file,img_url=img_url ,author=author,desc= desc,visual = visual,name=name,report_name = report_name,position=position,title = title,columns = columns,style = style, filter = filter, text = text) 
        
        # # # print(output)
        # # # print(columns)
        with open(f'output/{file}/html/{file}_visual_data.html','w',encoding="utf-8")as f:
            f.write(output)

        with open(f'templates/{file}_visual_data.html','w',encoding="utf-8")as f:
            f.write(output)
    
        
if __name__ == '__main__':
    # file = 'samp_1'
    file = 'Day2Practice'
    id = 'textbox7'
    report = 'Sales and profit'
    ob = html_generate()
    ob.visuals(file,report)