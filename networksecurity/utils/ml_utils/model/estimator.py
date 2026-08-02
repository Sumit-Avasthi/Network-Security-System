from networksecurity.constant.training_pipeline import SAVED_MODEL_DIR,SAVED_MODEL_FILE_NAME

import os
import sys

from networksecurity.exception.exception import NetworkSecurityException


class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.model=model
            self.preprocessor=preprocessor
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None

    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_pred=self.model.predict(x_transform)
            return y_pred
        except Exception as e:
            raise NetworkSecurityException(e,sys) from None