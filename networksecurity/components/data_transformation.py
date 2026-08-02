import os
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline


from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifacts_entity import DataTransformationArtifacts,DataValidationArtifacts


from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


from networksecurity.utils.utils import save_numpy_array,save_object


class DataTransformation:
    def __init__(self,data_validation_artifacts:DataValidationArtifacts,data_transformation_config:DataTransformationConfig):
        self.data_validation_artifacts=data_validation_artifacts
        self.data_transformation_config=data_transformation_config
        
