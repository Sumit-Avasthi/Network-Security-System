import os
import sys
import numpy as np
import pandas as pd
import mlflow


from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException


from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifacts_entity import ModelTrainerArtifacts,ClassificationMetricArtifacts,DataTransformationArtifacts
from networksecurity.utils.utils import save_object,load_object
from networksecurity.utils.utils import load_numpy_array_data


from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.utils import evaluate_model,load_object


from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier


class ModelTrainer:
    def __init__(self,model_trainer_config:ModelTrainerConfig,data_transformation_artifacts:DataTransformationArtifacts):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifacts=data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def track_mlflow(self,best_model,classificationmertics):
        logging.info("Starting a MLflow Experiment.")
        with mlflow.start_run():
            f1_score=classificationmertics.f1_score
            precision_score=classificationmertics.precision_score
            recall_score=classificationmertics.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    def train_model(self,X_train,y_train,X_test,y_test):
        try:
            models={
                "Random Forest":RandomForestClassifier(verbose=1),
                "Logistic Classifier":LogisticRegression(verbose=1),
                "Ada Boost Classifier":AdaBoostClassifier(),
                "Gradient Boosting Classifier":GradientBoostingClassifier(verbose=1),
                "Decision Tree Classifier":DecisionTreeClassifier()
            }

            params = {
                        "Random Forest": {
                            "n_estimators": [100, 200, 300],
                            "max_depth": [None, 10, 20, 30],
                            "min_samples_split": [2, 5, 10],
                            "min_samples_leaf": [1, 2, 4]
                        },

                        "Logistic Classifier": {
                            "C": [0.01, 0.1, 1, 10, 100],
                            "solver": ["liblinear", "lbfgs"],
                            "penalty": ["l2"]
                        },

                        "Ada Boost Classifier": {
                            "n_estimators": [50, 100, 200],
                            "learning_rate": [0.01, 0.1, 1.0]
                        },

                        "Gradient Boosting Classifier": {
                            "n_estimators": [100, 200],
                            "learning_rate": [0.01, 0.1, 0.2],
                            "max_depth": [3, 5, 7],
                            "subsample": [0.8, 1.0]
                        },

                        "Decision Tree Classifier": {
                            "criterion": ["gini", "entropy"],
                            "max_depth": [None, 10, 20, 30],
                            "min_samples_split": [2, 5, 10],
                            "min_samples_leaf": [1, 2, 4]
                        }
                    }

            logging.info("Training our model with provided dataset")
            model_report:dict=evaluate_model(X_train,y_train,X_test,y_test,models,params)
            best_model_score=max(sorted(list(model_report.values())))
            best_model_name=list(model_report.keys())[list(model_report.values()).index(best_model_score)]

            logging.info(f"Model Training is completed , Best model is {best_model_name} with score of {best_model_score}")

            # print(best_model_name,best_model_score)

            best_model=models[best_model_name]

            y_train_pred=best_model.predict(X_train)
            training_report=get_classification_score(y_train,y_train_pred)

            logging.info("mlflow for trainig report")
            self.track_mlflow(best_model,training_report)
            
            y_test_pred=best_model.predict(X_test)
            testing_report=get_classification_score(y_test,y_test_pred)

            logging.info("mlflow for testing report")
            self.track_mlflow(best_model,testing_report)

            logging.info("MlFlow Completed")

            logging.info("Testing and evaluating our best model")

            preprocessor=load_object(self.data_transformation_artifacts.transformed_object_file_path)

            model_trainer_dir=os.path.dirname(self.model_trainer_config.trained_model_file_path)

            os.makedirs(model_trainer_dir,exist_ok=True)

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)

            save_object(self.model_trainer_config.trained_model_file_path,network_model)

            logging.info("Saving our Network Model")

            return ModelTrainerArtifacts(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                trained_metric_artifacts=training_report,
                test_metric_artifacts=testing_report
            )

        except Exception as e :
            raise NetworkSecurityException(e,sys) from None


    def initiate_model_trainer(self):
        try:
            logging.info("Entered into model trainer")
            train_file_path=self.data_transformation_artifacts.transformed_train_file_path
            test_file_path=self.data_transformation_artifacts.transformed_test_file_path

            train_data=load_numpy_array_data(train_file_path)
            test_data=load_numpy_array_data(test_file_path)

            logging.info("Train and Test data has been loaded")


            X_train,X_test,y_train,y_test=(
                train_data[:,:-1],
                test_data[:,:-1],
                train_data[:,-1],
                test_data[:,-1]
            )
            model_trainer_artifacts=self.train_model(X_train,y_train,X_test,y_test)

            return model_trainer_artifacts

        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

