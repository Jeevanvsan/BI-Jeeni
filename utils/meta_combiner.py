import yaml

class meta_combiner:
    def run():
        with open('output/file_list.yaml','r') as f:
            files = yaml.safe_load(f.read())

        with open('output/overview.yaml','r') as f:
            over_ = yaml.safe_load(f.read())

        for file in files:
            file = file.replace('.pbit','')
            with open(f'output/{file}/data_structure.yaml','r') as f:
                data = yaml.safe_load(f.read())
            over_.append({"file": file,"meta": data})

        with open('output/overview.yaml','w') as f:
            over_ = yaml.safe_dump(over_,f)

        