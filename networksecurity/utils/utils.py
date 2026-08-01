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
    


