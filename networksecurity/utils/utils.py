import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import sys
import os
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml(file_path:str)->dict:
    try:
        with open(file_path,'rb') as file_obj:
            return yaml.safe_load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None



def write_yaml_file(file_path:str,content):
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file_obj:
            yaml.dump(content,file_obj)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None



def save_numpy_array(file_path:str,array:np.array):
    try:
        dir_name=os.path.dirname(file_path)
        os.makedirs(dir_name,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None


def save_object(file_path:str,obj):
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as file:
            pickle.dump(object,file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None

def load_object(file_path:str):
    try:
        if not os.path.exists(file_path):
            raise NetworkSecurityException(FileExistsError,sys) from None

        with open(file_path,"rb") as file:
            return pickle.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None


def load_numpy_array_data(file_path:str):
    try:
        with open(file_path,"rb") as file:
            return np.load(file)
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None


def evaluate_model(X_train,y_train,X_test,y_test,models,params):
    try:
        report={}

        for model_n in models.keys():
            model_name=model_n
            model=models[model_n]
            param=params[model_n]

            gridcv=GridSearchCV(estimator=model,param_grid=param,cv=5)

            gridcv.fit(X_train,y_train)

            model.set_params(**gridcv.best_params_)
            model.fit(X_train,y_train)

            y_train_pred=model.predict(X_train)
            y_test_pred=model.predict(X_test)

            training_score=r2_score(y_train,y_train_pred)
            testing_score=r2_score(y_test,y_test_pred)


            report[model_name] = testing_score

        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys) from None