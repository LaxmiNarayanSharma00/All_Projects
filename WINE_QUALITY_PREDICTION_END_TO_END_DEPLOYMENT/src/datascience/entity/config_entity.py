from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_url: str
    local_data_file: Path
    unzip_dir: Path

@dataclass
class Datavalidationconfig:
    root_dir:Path
    unzip_data_dir:Path
    STATUS_FILE:str
    all_schema:dict

@dataclass
class Datatransformation_config:
    root_dir: Path
    data_path: Path    


@dataclass
class Datatrainer_config:
    root_dir: Path
    train_data: Path
    test_data: Path
    model_name: str
    alpha: float
    l1_ratio: float
    target_col: str    

@dataclass
class model_evaluation_config:
    root_dir: Path
    test_data_path: Path
    model_path: Path
    metric_file_path: Path
    all_params: dict
    target_column: str
