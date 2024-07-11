import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import json
import yaml
import os
import shutil


class Image_generator:
    def run(file):
        with open(f'output/{file}/data_structure.yaml','r') as f:
            data = yaml.safe_load(f)

        if os.path.isdir(f"output/{file}/img") is False:
            os.mkdir(f"output/{file}/img")

        if os.path.isdir(f"output/{file}/img/layout") is False:
            os.mkdir(f"output/{file}/img/layout")
        
        # if os.path.exists(f"output/{file}/img/report") is False:
        #     os.mkdir(f"output/{file}/img/report")


        for report in data['layout']:
            fig, ax = plt.subplots()
            ax.set_xlim(0, 1280)
            ax.set_ylim(0, 720)
            plt.axis('off')
            plt.gca().invert_yaxis()
            for cont in report['visualContainers']: 
                for key, visual in cont.items():
                # for visual in cont:
                    # # print(key,"   :    ",visual["position"])
                    x= visual['position']['x']
                    y= visual['position']['y']
                    width= visual['position']['width']
                    height= visual['position']['height']
                    text = visual['visual_type']
                    rectangle = Rectangle((x, y), width, height, linewidth=1, edgecolor='r', facecolor='none')
                    text_x = x + width / 2
                    text_y = y + height / 2
                    plt.text(text_x, text_y, text, ha='center', va='center', fontsize=12, color='r')
                    ax.add_patch(rectangle)
            if os.path.isdir("static/img/layout") is False:
                    os.mkdir('static/img/layout')

            if os.path.isdir(f'static/img/layout/{file}') is False:
                os.mkdir(f'static/img/layout/{file}')

            plt.savefig(f'output/{file}/img/layout/{report["report_name"]}.png')
            plt.savefig(f'static/img/layout/{file}/{report["report_name"]}.png')
        
        if os.path.exists(f'output/{file}_extract/Report/StaticResources/RegisteredResources'):
            shutil.copytree(f'output/{file}_extract/Report/StaticResources/RegisteredResources', f"output/{file}/img/Report")
            shutil.copytree(f'output/{file}_extract/Report/StaticResources/RegisteredResources', f"static/img/report/{file}")
    
