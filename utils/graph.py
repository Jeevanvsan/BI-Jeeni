import json
import os
import yaml
from pyvis.network import Network 
from jinja2 import Environment, FileSystemLoader
import yaml

class create_graph():
    def __init__(self,file):
        self.filename = file
        with open(f'output/{self.filename}/data_structure.yaml','r') as f:
            self.file = yaml.safe_load(f)

        self.g = Network(directed=True, layout=True,select_menu=True,cdn_resources='remote')
        # self.g.barnes_hut()
        # self.g.toggle_physics(True)
        
        self.g.options.layout.hierarchical.direction = 'LR'
        self.g.options.layout.hierarchical.levelSeparation = 400
        self.g.options.layout.hierarchical.nodeSpacing = 130
        self.g.options.layout.hierarchical.navigationButtons = True
        self.g.options.interaction.zoomSpeed = 0.4
        self.g.options.edges.smooth.type = "cubicBezier"
        self.g.options.edges.arrowStrikethrough = False
        self.g.options.edges.strokeWidth = 5

        
        # self.g.set_options("""var options = {
        #   "edges": {
        #     "color": {
        #       "inherit": true
        #     },
        #     "smooth": false
        #   },
        #   "layout": {
        #     "hierarchical": {
        #       "enabled": true,
        #       "levelSeparation": 300,
        #       "nodeSpacing": 130,
        #       "direction": "LR",
        #       "sortMethod": "directed"
        #     }
        #   },
        #   "physics": {
        #     "hierarchicalRepulsion": {
        #       "centralGravity": 0
        #     },
        #     "minVelocity": 0.75,
        #     "solver": "hierarchicalRepulsion"
        #   }
        # }""")

        self.run()
        
    def json_create(self):
        main_dict = {
            'node': self.filename,
            'relation': 'file',
            'sub_nodes': [],
        }
        self.add_node(main_dict)
    
    def run(self):
        self.json_create()
        with open(f'output/{self.filename}/out_json.json') as f:
          json_file = json.load(f)
        self.graph_create(json_file)

        print(self.g.html)

        grph_html = self.g.html
        # self.g.save_graph('templates/sample.html')
        with open(f'output/{self.filename}/lineage.html', 'w', encoding='utf-8') as out:
            out.write(self.g.generate_html())
        # self.g.save_graph(f'output/{self.filename}/lineage.html')

        if not os.path.exists(f'templates/{self.filename}'):
            os.mkdir(f'templates/{self.filename}')

        # self.g.save_graph(f'templates/{self.filename}/lineage.html')

        with open(f'templates/{self.filename}/lineage.html', 'w', encoding='utf-8') as out:
            out.write(self.g.generate_html())

        # self.g.save_graph(f'templates/{self.filename}_lineage.html')
        
        self.generate_html()
        # self.g.show('templates/sample.html', notebook=False)

    def generate_html(self):

        with open("utils/templates/jinja_lineage.html", "r") as f:
            temp = f.read()

        with open(f'templates/{self.filename}_lineage.html','w',encoding="utf-8")as f1:
            f1.write(temp)

    def graph_create(self,file,level=1):
        node = ''
        relation = ''
        # Adjust node style for tree-like appearance
        # node_options = {
        #     "shape": "box",
        #     "font": {"size": 15},
        #     "title": node_label,
        #     "label": node_label[:30] + "..." if len(node_label) > 30 else node_label,
        #     "level": level,
        #     "group": level
        # }
        if isinstance(file,dict):
            for key,value in file.items():
                if isinstance(value,str):
                    if key == 'node':
                        node = value
                        self.g.add_node(n_id=value,label=value,shape="box",level=level,group = level)
                    if key == 'relation':
                        relation = value
                    if key == 'parent':
                        self.g.add_edge(value,node,label=relation)
                else:
                    self.graph_create(value,level=level+1)
        elif isinstance(file,list):
            for i, value in enumerate(file):
                if isinstance(value,dict):
                    self.graph_create(value,level=level+1)
                if isinstance(value,list):
                    self.graph_create(value,level=level+1)


    def add_node(self, main_dict):
        if main_dict.get('relation') == 'file':
            sub_node = main_dict.get('subnodes')
            rtn_subnode = self.add_subnode(sub_node)
            main_dict.get('sub_nodes').append(rtn_subnode)
        # # print(json.dumps(main_dict, indent=4))
        with open(f'output/{self.filename}/out_json.json','w') as f:
            f.write(json.dumps(main_dict, indent=4))

    def add_subnode(self,sub_node):
        node = []
        sub_node = {}
        query_sub_node = {}
        query_sub_node = []
        stmt = None
        if sub_node:
            print('value found')
        else:
            lineage = self.file
            for val in lineage['layout']:
                parent = self.filename
                report = val['report_name']
                sub_node = {'node': report, 'relation':'report','parent':parent,'sub_nodes':[]}
                for i,visual in enumerate(val['visualContainers']):
                    for k,v in visual.items():
                        # # print(v['visual_type'][0])
                        parent = report



                        visual_sub_node = {'node': f"{v['id']}", 'relation': k,'parent': parent}
                        # # print(visual_sub_node)
                        # print(v)
                        vis_keys = v.keys()

                        col_list = [vis_key for vis_key in vis_keys if 'col_' in vis_key]

                        if col_list:
                            visual_sub_node = {'node': f"{v['id']}", 'relation': k,'parent': parent,"sub_nodes":[]}

                            for vis_key in col_list:
                                parent = report
                                if isinstance(v[vis_key], list):
                                    for col_ in v[vis_key]:  
                                        parent = v['id']
                                        col_sub_node = {}
                                        col_sub_node ['node']= col_ 
                                        col_sub_node ['relation']= 'column'
                                        col_sub_node['parent']= parent
                                        col_sub_node['sub_nodes']= []
                                        source = None
                                        if '(' in col_:
                                            source = col_.split('(')[1].split('.')[0]
                                        else:
                                            source = col_.split('.')[0]
                                        source_sub_node = {'node': source, 'relation': 'source','parent': col_,}
                                        col_sub_node.get('sub_nodes').append(source_sub_node)
                                        visual_sub_node.get('sub_nodes').append(col_sub_node)
                                else:
                                    col_ = v[vis_key]
                                    parent = v['id']
                                    col_sub_node = {}
                                    col_sub_node ['node']= col_ 
                                    col_sub_node ['relation']= 'column'
                                    col_sub_node['parent']= parent
                                    col_sub_node['sub_nodes']= []
                                    source = None
                                    if '(' in col_:
                                        source = col_.split('(')[1].split('.')[0]
                                    else:
                                        source = col_.split('.')[0]
                                    source_sub_node = {'node': source, 'relation': 'source','parent': col_,}
                                    col_sub_node.get('sub_nodes').append(source_sub_node)
                                    visual_sub_node.get('sub_nodes').append(col_sub_node)

                            
                        sub_node.get('sub_nodes').append(visual_sub_node)
                node.append(sub_node)
        return node
            

if __name__ == '__main__':
    ob = create_graph("s1")
    ob.run()





