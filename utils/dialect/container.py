import json
import yaml
from utils.helper import json_path
from utils import extract_path
import ast


class extr_data:
    def get_data(v_type,visual,data={}):
        with open('utils/configs/visual_config.yaml', 'r') as f:
            config = yaml.safe_load(bytes(f.read(),"utf-8")) 
        exclude = ["vcObjects","class","charts","line_charts","pie_charts","treemap","properties","visual_link","objects","icon","type"]
        _data = data.copy()
        v_data = json.loads(visual['config'])
        linechart_cols = ["column_y","Y",]
        cols=[]
        # print(v_type)

        if v_type in config:
            # print("====================")
            for key , items in config[v_type].items():
                if key not in exclude:
                    # if "projections" in items:
                    #     if json_path.rtn_get_json_keypaths(v_data,config.get(v_type).get(key), top_level=True):
                    #         val = json_path.rtn_get_json_keypaths(v_data,config.get(v_type).get(key), top_level=True)
                    #         cols.append({key:val})

                    if json_path.rtn_get_json_keypaths(v_data,config.get(v_type).get(key), top_level=True):
                        val = json_path.rtn_get_json_keypaths(v_data,config.get(v_type).get(key), top_level=True)
                        # if "text" not in  key:
                        #     val = val[0]
                        if len(val) == 1:
                            val = val[0]
                        
                        _data.update({key:val})

                    
            if cols:
                _data['columns'] = cols

            # print(_data)
        else:
            # print("nothing got -----------------------------------")
            flag = extract_path.run(v_data,v_type)
            if flag:
                with open('utils/configs/visual_config.yaml', 'r') as f:
                    config = yaml.safe_load(bytes(f.read(),"utf-8")) 
                if v_type in config:
                    extr_data.get_data(v_type,visual,_data)
                else:
                    raise Exception("Visual path adding to config failed 1")
            else:
                raise Exception("Visual path adding to config failed 2")
        # print(_data)
        # print("data got --------------------------------------------------")

        return _data
    
    def get_canvas(type,data):
        with open('utils/configs/visual_config.yaml', 'r') as f:
            config = yaml.safe_load(bytes(f.read(),"utf-8")) 
        exclude = ["vcObjects","class","charts","line_charts","pie_charts","treemap","properties","visual_link","objects","icon"]
        # _data = data.copy()
        data = json.loads(data)
        # print(data)
        c_data = {}

        for key , items in config[type].items():
            if key not in exclude:
                if json_path.rtn_get_json_keypaths(data,config.get(type).get(key), top_level=True):
                    val = json_path.rtn_get_json_keypaths(data,config.get(type).get(key), top_level=True)
                    c_data.update({key:val[0]})
        return c_data
    
    def get_wallpaper(type,data):
        with open('utils/configs/visual_config.yaml', 'r') as f:
            config = yaml.safe_load(bytes(f.read(),"utf-8")) 
        exclude = ["vcObjects","class","charts","line_charts","pie_charts","treemap","properties","visual_link","objects","icon"]
        # _data = data.copy()
        data = json.loads(data)
        # print(data)
        v_data = {}

        for key , items in config[type].items():
            if key not in exclude:
                if json_path.rtn_get_json_keypaths(data,config.get(type).get(key), top_level=True):
                    val = json_path.rtn_get_json_keypaths(data,config.get(type).get(key), top_level=True)
                    v_data.update({key:val[0]})
        return v_data

