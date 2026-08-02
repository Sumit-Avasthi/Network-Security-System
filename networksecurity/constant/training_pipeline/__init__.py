import os
import pandas as pd
import numpy as np
import sys


TARGET_COLUMN="Result"
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACTS_DIR:str="Artifacts"

### Inside Feature store folder (raw data)
FILE_NAME:str="phisingData.csv"


## Inside ingested folder
TRAIN_DATA_FILE="train.csv"
TEST_DATA_FILE="test.csv"
TRANSFORMER_OBJECT_FILE="preprocessor.pkl"
MODEL_FILE_NAME="model.pkl"

SAVED_MODEL_DIR="saved_model"
SAVED_MODEL_FILE_NAME="model.pkl"


DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="SUMITAV"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str="feature_store"  ## Raw Data
DATA_INGESTION_INGESTED_STORE_DIR:str="ingested" ## Train and Test Data
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float = 0.2

SCHEMA_FILE_PATH=os.path.join("data_schema","schema.yaml")

DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validated"
DATA_VALIDATION_INVALID_DIR="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME="report.yaml"


DATA_TRANSFORMATION_DIR="data_transformation"
DATA_TRANSFORMATION_TRANSFORMED_DATA_DIR="transformed_data"
DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR="transformer_obj"
DATA_TRANSFORMATION_IMPUTER_PARAMS:dict = {
    "missing_values":np.nan,
    "n_neighbors" : 3,
    "weights":"uniform"
}




MODEL_TRAINER_DIR_NAME="model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR="trained_model"
MODEL_TRAINER_EXPECTED_SCORE:float=0.6
MODEL_TRAINER_OVERFITTING_AND_UNDERFITTING_THRESHOLD:float=0.05