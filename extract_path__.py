import yaml
import json


# with open("s.json","r") as f:
#    datas = json.loads(f.read())

path_ = {}

def get_json():
   with open("lay.json", "r") as f:
      lay = json.loads(bytes(f.read(),"utf8"))
   
   datas = json.loads(lay["sections"][0]["visualContainers"][0]["config"])
   print(datas)
   run(datas,"chart")


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
   #  print(path)
    if isinstance(data,list):
            path_extract(data,path,path_key,paths)
    if isinstance(data,dict):
 
        for key, item in data.items():
            if key not in ["Conditional"]:
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
      config = yaml.safe_load(f.read())

   path_[type] = {}
   paths = path_[type]
   paths["position"] = "layouts.position"
   for key1,data in datas['singleVisual']['objects'].items():
      path = ["singleVisual","objects"]
      path.append(key1)
      for each_data in data:
         for key2, item in each_data.items():
            # print(key2)
            if key2 not in ["selector"]:
               path1 = path + [key2]
               for key, item2 in item.items():
                  if key not in ["paragraphs"]:
                     path_key = F"{key1}_{key}"
                     path2 = path1 + [key]  
                     path_extract(item2,path2,path_key,paths)
   
   for key1,data in datas['singleVisual']['vcObjects'].items():
      path = ["singleVisual","vcObjects"]
      path.append(key1)
      for each_data in data:
         for key2, item in each_data.items():
            if key2 not in ["selector"]:
               path1 = path + [key2]
               for key, item2 in item.items():
                  path_key = F"{key1}_{key}"
                  path2 = path1 + [key]  
                  path_extract(item2,path2,path_key,paths)
   
   if "projections" in datas['singleVisual']:
      paths["column"] = "singleVisual.projections.Values.queryRef"
   

    
   config.update(path_)

   # with open('utils/configs/visual_config.yaml', 'w') as f:
   #    yaml.safe_dump(config, f)

   # with open("path.yaml", "w") as f:
   #    yaml.safe_dump(path_, f)
   
   return True

   
get_json()


    