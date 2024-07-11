import yaml


datas = {
   "name":"83f90bda3f3e26de13d7",
   "layouts":[
      {
         "id":0,
         "position":{
            "x":10,
            "y":0,
            "width":280,
            "height":280,
            "z":0
         }
      }
   ],
   "singleVisual":{
      "visualType":"pythonVisual",
      "projections":{
         "Values":[
            {
               "queryRef":"financials. Sales"
            }
         ]
      },
      "prototypeQuery":{
         "Version":2,
         "From":[
            {
               "Name":"f",
               "Entity":"financials",
               "Type":0
            }
         ],
         "Select":[
            {
               "Column":{
                  "Expression":{
                     "SourceRef":{
                        "Source":"f"
                     }
                  },
                  "Property":" Sales"
               },
               "Name":"financials. Sales"
            }
         ]
      },
      "drillFilterOtherVisuals":True,
      "objects":{
         "script":[
            {
               "properties":{
                  "source":{
                     "expr":{
                        "Literal":{
                           "Value":"'# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: \n\n# dataset = pandas.DataFrame( Sales)\n# dataset = dataset.drop_duplicates()\n\n# Paste or type your script code here:\n\nsome thinng to say !!!!!!!!!!!!!!!!!!!'"
                        }
                     }
                  },
                  "provider":{
                     "expr":{
                        "Literal":{
                           "Value":"'Python'"
                        }
                     }
                  }
               }
            }
         ]
      }
   }
}


path_ = {}

def img_path(data,path,path_key,paths):
    if isinstance(data,list):
        for list_data in data:
            img_path(list_data,path,path_key,paths)
    if isinstance(data,dict):
        for key, item in data.items():
            if key not in ["PackageName","PackageType"]:
                path.append(key)
            img_path(item,path,path_key,paths)
    else:
        path_val = '.'.join(path)
        paths[path_key] = path_val
    
def path_extract(data,path,path_key,paths):
    if isinstance(data,list):
            path_extract(data,path,path_key,paths)
    if isinstance(data,dict):
 
        for key, item in data.items():
            if 'image' in key:
                path1 = path + [key]
                for img_key, item in item.items():
                    path2 = path1 + [img_key]
                    img_path(item,path2,path_key +"_"+ img_key,paths)
                    path2.pop()
            else:
                if "ColorId" in key:
                    path_key = path_key + "_id"
                elif "Percent" in key:
                    path_key = path_key + "_per"
                if "ColorId" in path:
                    val = path.pop()

                path.append(key)
                path_extract(item,path,path_key,paths)
    else:
        path_val = '.'.join(path)
        paths[path_key] = path_val
        
def run(datas,type):

   with open('utils/configs/visual_config.yaml', 'r') as f:
      config = yaml.safe_load(bytes(f.read(),"utf-8"))
   
   print(datas)

   path_[type] = {}
   paths = path_[type]
   paths["position"] = "layouts.position"
   for key1,data in datas['singleVisual']['objects'].items():
      path = ["singleVisual","objects"]
      path.append(key1)
      for each_data in data:
         for key2, item in each_data.items():
               path1 = path + [key2]
               for key, item2 in item.items():
                  path_key = F"{key1}_{key}"
                  path2 = path1 + [key]  
                  path_extract(item2,path2,path_key,paths)
   
   if "projections" in datas['singleVisual']:
      paths["column"] = "singleVisual.projections.Values.queryRef"
   

    
   config.update(path_)

   with open('utils/configs/visual_config.yaml', 'w',encoding='utf-8') as f:
      yaml.safe_dump(config, f,indent=4)

   with open("path.yaml", "w") as f:
      yaml.safe_dump(path_, f)
   
   return True

   
# run(datas,"pythonVisual")



    