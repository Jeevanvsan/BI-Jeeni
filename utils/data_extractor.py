import json
import ast
import yaml
import re
import os
import importlib
from utils.helper import json_path
from utils.dialect.container import extr_data

class dataExtractor():
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    def run(self,layout_data,custom_files,schema_data,file):
        self.customs = custom_files
       

        main_dict = {"schema":None,"layout":None}
        schema = self.extract_schema(schema_data)
        # # print(schema)
        main_dict['schema'] = schema
    
        layout = self.extract_layout(layout_data)
        main_dict['layout'] = layout
        # # print(layout)

        if os.path.isdir(f"output/{file}") is False:
            os.mkdir(f"output/{file}")
                
        with open(f'output/{file}/data_structure.yaml', 'w') as f:
            yaml.safe_dump(main_dict,f,indent=4,sort_keys=False)

        with open('D:/xlerate/BI_temp/input/meta.yaml', 'w') as f:
            yaml.safe_dump(main_dict,f,indent=4,sort_keys=False)
        


    def extract_schema(self,files):
        # extract_data = f'output/samp_1_extract'
        # with open(f'{extract_data}/DataModelSchema', 'r') as f:
        #     files = json.loads(bytes(f.read(),"utf-8"))
        with open('utils/configs/schema_config.yaml', 'r') as f:
            config = yaml.safe_load(bytes(f.read(),"utf-8"))

        tables1 = json_path.rtn_get_json_keypaths(files, config["table"], top_level=True)[0]
        hierarchies1 = json_path.rtn_get_json_keypaths(files, config["table"], top_level=True)
        tables = []
        relations = []
        for tbl in tables1:
            if 'isHidden' in tbl:
                if tbl['isHidden']:
                    pass
            elif tbl['name'] in ['Date','Time Intelligence','Key Measures']:
                pass
            else:
                # # print(tbl)
                table = {"table_name":None,"columns":None}
                columns = []
                table['table_name'] = tbl['name']
                if "columns" in tbl:
                    for col in tbl['columns']:
                        if 'type' not in col :
                            column = {"name":None,"datatype":None}
                            column['name'] = col['name']
                            column['datatype'] = col['dataType']
                            columns.append(column)
                table['columns'] = columns
                for expr in tbl['partitions']:
                    table['mode'] = expr['mode']
                    table['m_code'] = expr['source']['expression']

                if "measures" in tbl:
                    measures = []
                    for msr in tbl["measures"]:
                        msr_ = {}
                        msr_['name'] = msr['name']
                        msr_['expression'] = msr['expression']

                        measures.append(msr_)
                    table["DAX"] = measures
                
                if "hierarchies" in tbl:
                    hierarchies = []
                    for hir in tbl["hierarchies"]:
                        hir_ = {}
                        if "ordinal" in hir:
                            hir_['ordinal'] = hir['ordinal']
                        if "name" in hir:
                            hir_['name'] = hir['name']
                        if "column" in hir:
                            hir_['column'] = hir['column']

                        hierarchies.append(hir_)
                    table["hierarchies"] = hierarchies
                    # # print(table)
                tables.append(table)
        if "relationships" in files['model']:
            relations1 = json_path.rtn_get_json_keypaths(files, config["relationships"], top_level=True)[0]
            for i, rel in enumerate(relations1):
                rel_ = {}
                rel_['id'] = i
                rel_['from_table'] = rel['fromTable']
                rel_['from_column'] = rel['fromColumn']
                rel_['to_table'] = rel['toTable']
                rel_['to_column'] = rel['toColumn']
                relations.append(rel_)   
        # # print(json.dumps(tables,indent=4))
        return {'tables': tables,'relations':relations}
    
    def extract_layout(self,data):
      

        with open('utils/configs/visual_config.yaml', 'r') as f:
            config = yaml.safe_load(bytes(f.read(),"utf-8"))

        reports = []
        charts = config.get('chart').get('charts')
        maps = config.get('map').get('maps')
        cards = config.get('card').get('cards')
        tables = config.get('table').get('tables')
        navigators = config.get('navigator').get('navigators')
        others = config.get('others')
        skip_ = []

        layout_data = data
        for section in layout_data['sections']:
            # # print(section)
            report = {"report_name": None, "canvas_settings": [],"wallpaper": [], "visualContainers": []}
            report['report_name'] = section['displayName']

            report_config = section['config']


            
            report['canvas_settings'].append(extr_data.get_canvas('canvasSettings',report_config))

            report['canvas_settings'][0].update({"width": section['width'], "height": section['height']})

            report['wallpaper'].append(extr_data.get_wallpaper('wallpaper',report_config))

            
            containers = []  
            for i, visual in enumerate(section['visualContainers']):
                columns = []
                module = None
    
                styles = []
                filters = []
                v_data = json.loads(visual['config'])
                # # print(v_data)
                # # print(visual)
                v_type = json_path.rtn_get_json_keypaths(v_data,'singleVisual.visualType', top_level=True)
                if v_type:
                    v_type = v_type[0]
                elif json_path.rtn_get_json_keypaths(v_data,'singleVisualGroup', top_level=True):
                    v_type = "singleVisualGroup"
                
                # print(v_type)

                og_type = v_type
                if og_type in charts:
                    v_type = "chart"
                elif og_type in maps:
                    v_type = "map"
                elif og_type in cards:
                    v_type = "card"
                elif og_type in tables:
                    v_type = "table"
                elif og_type in navigators:
                    v_type = "navigator"
                
                if v_type:
                    if v_type not in self.customs:
                        final_data = extr_data.get_data(v_type,visual)
                        # # print(final_data)
                        if final_data:
                            id = f"{report['report_name']}_{v_type}{i}"
                            final_data["id"] = id
                            final_data["visual_type"] = og_type
                            containers.append({v_type+"_container": final_data})
                    elif v_type in self.customs:
                        id = f"{report['report_name']}_{v_type}{i}"
                        final_data = extr_data.get_data("CustomVisual",visual)
                        final_data["id"] = id
                        final_data["name"] = self.customs[v_type]['name'] 
                        final_data["author"] = self.customs[v_type]['author'] 
                        final_data["desc"] = self.customs[v_type]['desc'] 
                        final_data["visual_type"] = "CustomVisual"
                        containers.append({"CustomVisual_container": final_data})

                # # print(containers)
                report['visualContainers'] = containers
            reports.append(report)
        return reports
        
    
if __name__ == '__main__':
    ob = dataExtractor()