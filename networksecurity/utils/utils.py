import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import pandas as pd
import numpy as np
import sys
import os
import pickle


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