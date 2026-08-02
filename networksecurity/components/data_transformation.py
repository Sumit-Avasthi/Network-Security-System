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
        try:
            self.data_validation_artifacts=data_validation_artifacts
            self.data_transformation_config=data_transformation_config
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info("Entered to get_data_transformer_object in data_transformation.py")
            imputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("KNN Imputer is initialized with params")
            processor=Pipeline([
                ("imputer",imputer)
            ])

            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def initiate_data_transformation(self)->DataTransformationArtifacts:
        logging.info("Entered to data transformation stage")
        try:
            logging.info("Data Transformation Initiated.")
            train_file_path=self.data_validation_artifacts.valid_train_file_path
            test_file_path=self.data_validation_artifacts.valid_test_file_path

            train_dataframe=pd.read_csv(train_file_path)
            test_dataframe=pd.read_csv(test_file_path)

            train_data_feature_column=train_dataframe.drop(columns=[TARGET_COLUMN])
            train_data_target_column=train_dataframe[TARGET_COLUMN]
            test_data_feature_column=test_dataframe.drop(columns=[TARGET_COLUMN])
            test_data_target_column=test_dataframe[TARGET_COLUMN]
            train_data_target_column=train_data_target_column.replace(-1,0)
            test_data_target_column=test_data_target_column.replace(-1,0)
            logging.info("Sperated Dependent and independent features")

            preprocessor_obj=self.get_data_transformer_object()

            preprocessor_obj.fit(train_data_feature_column)
            transformed_train_feature_data=preprocessor_obj.transform(train_data_feature_column)
            transformed_test_feature_data=preprocessor_obj.transform(test_data_feature_column)
            logging.info("Transfomed trained and test data")
            train_arr=np.c_[transformed_train_feature_data,train_data_target_column]
            test_arr=np.c_[transformed_test_feature_data,test_data_target_column]

            save_numpy_array(self.data_transformation_config.transformed_trained_file_path,train_arr)
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,test_arr)

            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_obj)
            logging.info("Saved Transformed Train and Test numpy arr.")


            data_transformation_artifacts=DataTransformationArtifacts(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_trained_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

