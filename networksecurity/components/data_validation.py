from networksecurity.entity.artifacts_entity import DataIngestionArtifacts,DataValidationArtifacts
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.utils.utils import read_yaml
from networksecurity.logging.logger import logging

from scipy.stats import ks_2samp
import pandas as pd
import sys
import os


class DataValidation:
    def __init__(self,data_ingestion_artifacts:DataIngestionArtifacts,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifacts=data_ingestion_artifacts
            self.data_validation_config=data_validation_config
            self._schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None