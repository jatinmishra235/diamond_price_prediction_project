import os,sys
import pandas as pd
from src.logger import logging
from src.exception import CustomException
from sklearn.model_selection import train_test_split
from dataclasses import dataclass


@dataclass
class DataIngestionConfig:
    train_file_path:str = os.path.join('artifacts','train.csv')
    test_file_path:str = os.path.join('artifacts','test.csv')
    raw_file_path:str = os.path.join('artifacts','raw.csv')

class DataIngestion:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig

    def initiate_data_ingestion(self):
        try:
            logging.info('data ingestion has started')

            df = pd.read_csv(os.path.join(os.getcwd(),'notebooks','data','diamond.csv'))
            os.makedirs(os.path.dirname(self.data_ingestion_config.raw_file_path),exist_ok=True)
            df.to_csv(self.data_ingestion_config.raw_file_path,index=False,header=True)

            train_df,test_df = train_test_split(df, test_size=0.2)

            train_df.to_csv(self.data_ingestion_config.train_file_path,index=False,header=True)
            test_df.to_csv(self.data_ingestion_config.test_file_path,index=False,header=True)

            logging.info('data ingestion completed!')

            return (
                self.data_ingestion_config.train_file_path,
                self.data_ingestion_config.test_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
    

if __name__=='__main__':
    obj = DataIngestion()
    train, test = obj.initiate_data_ingestion()
    print(train)