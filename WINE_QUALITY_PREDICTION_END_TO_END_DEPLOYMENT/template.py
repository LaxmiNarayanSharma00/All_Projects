import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO,format='[%(asctime)s]: %(message)s:')

project_name='datascience'

list_of_files=[
    '.github/workflows/.gitkeep',
    f'src/{project_name}/__init__.py',
    f'src/{project_name}/components/__init__.py',
    f'src/{project_name}/utils/__init__.py',
    f'src/{project_name}/utils/common.py',
    f'src/{project_name}/config/__init__.py',
    f'src/{project_name}/config/configuration.py',
    f'src/{project_name}/pipeline/__init__.py',
    f'src/{project_name}/entity/__init__.py',
    f'src/{project_name}/entity/config_entity.py',
    f'src/{project_name}/constants/__init__.py',
    'config/config.yaml',
    'params.yaml',
    'schema.yaml',
    'main.py',
    'Dockerfile',
    'setup.py',
    'research/research.ipynb',
    'templates/index.html'
]

for filepath in list_of_files:
    file_path=Path(filepath)
    
    dir_name,filename=os.path.split(filepath)
    # print(dir_name)
    if dir_name!='':
        os.makedirs(dir_name,exist_ok=True)
        logging.info(f'creating directory {dir_name} for file {filename}')

    if not os.path.exists(file_path) or (os.path.getsize(file_path)==0):
        with open(file_path,'w') as f:
            pass
            logging.info(f'creating empty file {file_path}')    

    else:
        logging.info(f'{file_path} already exist')

        
                