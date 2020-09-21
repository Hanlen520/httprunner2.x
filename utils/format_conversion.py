'''
Created on 2020年9月21日

@author: qguan
'''
import yaml
import json

def json_to_yaml(json_file):
    """支持json格式转yaml"""
    if json_file.endswith("json"):
        with open(json_file,"r") as pf:
            json_to_dict = json.loads(pf.read())
        yaml_file=json_file.replace(".json",".yaml")
        with open(yaml_file,"w") as fp:
            yaml.safe_dump(json_to_dict,stream=fp,default_flow_style=False)
            print("json转yaml成功!!!")
    else:
        print("不是json结尾的文件!!!")

def yaml_to_yaml(yaml_file):
    """支持json格式转yaml"""
    if yaml_file.endswith("yaml"):
        with open(yaml_file,"r") as pf:
            #先将yaml转换为dict格式
            yaml_to_dict = yaml.load(pf,Loader=yaml.FullLoader)
            dict_to_json = json.dumps(yaml_to_dict,sort_keys=False,indent=4,separators=(',',': '))
        json_file=yaml_file.replace(".yaml",".json")
        with open(json_file,"w") as fp:
            fp.write(dict_to_json)
            print("yaml转json成功!!!")
    else:
        print("不是yaml结尾的文件!!!")

# json_to_yaml("exam.json")
yaml_to_yaml("exam.yaml")