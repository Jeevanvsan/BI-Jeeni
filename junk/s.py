from zipfile import ZipFile
import os
import json



# directory_path = f'output/Day2Practice_extract'

# # with ZipFile(f's.pbit', 'w') as zipf:
# #     for foldername, subfolders, filenames in os.walk(directory_path):
# #         for filename in filenames:
# #             file_path = os.path.join(foldername, filename)
# #             arcname = os.path.relpath(file_path, directory_path)
# #             zipf.write(file_path, arcname)

# path = os.path.join(os.path.expanduser('~'), 'Documents')


# with ZipFile(f'{path}/BIX/s1.xlr', 'r') as f:
#             f.extractall('loads')
str = "{\"name\":\"ca5d63c76c20ad37c235\",\"layouts\":[{\"id\":0,\"position\":{\"x\":735.1004016064257,\"y\":344.41767068273094,\"z\":8,\"width\":149.07630522088354,\"height\":150.36144578313255,\"tabOrder\":8}}],\"singleVisual\":{\"visualType\":\"cardVisual\",\"projections\":{\"Data\":[{\"queryRef\":\"Sum(Sheet1.MRP)\"}],\"Tooltips\":[{\"queryRef\":\"Min(Sheet1.Size)\"}]},\"prototypeQuery\":{\"Version\":2,\"From\":[{\"Name\":\"s\",\"Entity\":\"Sheet1\",\"Type\":0}],\"Select\":[{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"MRP\"}},\"Function\":0},\"Name\":\"Sum(Sheet1.MRP)\",\"NativeReferenceName\":\"Sum of MRP\"},{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"Size\"}},\"Function\":3},\"Name\":\"Min(Sheet1.Size)\",\"NativeReferenceName\":\"First Size\"}],\"OrderBy\":[{\"Direction\":2,\"Expression\":{\"Aggregation\":{\"Expression\":{\"Column\":{\"Expression\":{\"SourceRef\":{\"Source\":\"s\"}},\"Property\":\"MRP\"}},\"Function\":0}}}]},\"drillFilterOtherVisuals\":true,\"hasDefaultSort\":true}}"
print(json.loads(str))