import os
import logging
from datetime import datetime

log_file = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(),'logs',log_file)
os.makedirs(logs_path)

log_file_path = os.path.join(logs_path,log_file)

logging.basicConfig(filename=log_file_path,format="[ %(asctime)s ] %(lineno)d - %(levelname)s - %(message)s",level=logging.INFO)