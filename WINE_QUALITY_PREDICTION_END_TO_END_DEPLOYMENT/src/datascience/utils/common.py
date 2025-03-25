import os
import yaml
from src.datascience import logger
import json,joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError

# ConfigBox: A class from the box package, which is used to work with dictionaries 
# (configurations in this case) 
# with dot notation (accessing keys as if they were attributes).

@ensure_annotations # iit helps to ensure that return type of function is fixed 
def read_yml(path_to_yml:Path)->ConfigBox:

    try:
        with open(path_to_yml) as yml_file:
            content=yaml.safe_load(yml_file)
            logger.info(f'yaml file {path_to_yml} loaded succesfully')
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError('yaml file is empty')

    except Exception as e:
        raise e
    
@ensure_annotations
def create_directories(path_to_directories:list,verbose=True):    
    for path in path_to_directories:
        os.makedirs(path,exist_ok=True)

    if verbose:
        logger.info(f'created directory at path {path}')    

@ensure_annotations
def save_json(path:Path,data:dict):
    with open(path,'w') as f: # with automatically closes even after error snd by opening in write mode ensure that file is created iif it does not exist
        json.dump(data,f,indent=4)
    logger.info(f'json file saved  at path :{path}')            

@ensure_annotations
def load_json(path:Path)->ConfigBox:
    with open(path) as f: 
        content=json.load(f)
    logger.info(f'file loaded  from path :{path}')            
    return ConfigBox(content)

@ensure_annotations
def save_bin(data:Any,path:Path):
    joblib.dump(value=data,filename=path)
    logger.info(f'bnary file saved at path:{path}')

@ensure_annotations
def save_bin(path:Path):
    content=joblib.load(filename=path)
    logger.info(f'bnary file loaded from path:{path}')
    return content