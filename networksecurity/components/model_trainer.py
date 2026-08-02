import os
import sys
import numpy as np
import pandas as pd


from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifacts_entity import ModelTrainerArtifacts,ClassificationMetricArtifacts,DataTransformationArtifacts
from networksecurity.utils.utils import save_object,load_object
from networksecurity.utils.utils import load_numpy_array_data


from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifacts=data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            pass
        except Exception as e :
            raise NetworkSecurityException(e,sys) from None


    def initiate_model_trainer(self):
        try:
            logging.info("Entered into model trainer")
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path

            train_data=load_numpy_array_data(train_file_path)
            test_data=load_numpy_array_data(test_data)

            logging.info("Train and Test data has been loaded")


            X_train,X_test,y_train,y_test=(
                train_data[:,:-1],
                test_data[:,:-1],
                train_data[:,-1],
                test_data[:,-1]
            )


        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

