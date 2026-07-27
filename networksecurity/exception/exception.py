import sys
from networksecurity.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_details:sys):
        self.error_message=error_message

        _,_,ex_tb = error_details.exc_info()
        self.lineno = ex_tb.tb_lineno
        self.file_name = ex_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error Occured in File name = {self.file_name} and Line Number = {self.lineno} Message = {str(self.error_message)}"

