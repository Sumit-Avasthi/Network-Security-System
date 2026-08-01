from dataclasses import dataclass

@dataclass
class DataIngestionArtifacts:
    train_data_path:str
    test_data_path:str