import os,sys
import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler,OrdinalEncoder
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from sklearn.pipeline import Pipeline
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_file_path:object = os.path.join('artifacts','preprocessor.pkl')


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig

    def get_preprocessor_object(self):
        try:

            numerical_columns = ['carat', 'depth', 'table', 'x', 'y', 'z']
            categorical_columns = ['cut', 'color', 'clarity']

            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']

            logging.info('getting preprocessor object')

            numerical_pipeline = Pipeline(steps=[
                ('simple_imputer',SimpleImputer(strategy='median')),
                ('scaling',StandardScaler())
            ])

            categorical_pipeline = Pipeline(steps=[
                ('simple_imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinal_encoding',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaling',StandardScaler())
            ])

            preprocessor = ColumnTransformer([
                ('numerical_pipeline',numerical_pipeline,numerical_columns),
                ('categorical_pipeline',categorical_pipeline,categorical_columns)
            ])

            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)


    def initiate_data_transformation(self, train_path, test_path):
        try:
            logging.info('data transformation started!!')

            preprocessor = self.get_preprocessor_object()
            target_column = 'price'
            drop_columns = ['id','price']

            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            train_x = train_df.drop(columns=drop_columns,axis=1)
            train_target = train_df[target_column]

            test_x = test_df.drop(columns=drop_columns,axis=1)
            test_target = test_df[target_column]

            train_arr = preprocessor.fit_transform(train_x)
            test_arr = preprocessor.transform(test_x)

            train_final = np.c_[train_arr,np.array(train_target)]
            test_final = np.c_[test_arr,np.array(test_target)]


            save_object(self.data_transformation_config.preprocessor_file_path,preprocessor)

            return (
                train_final,
                test_final,
                self.data_transformation_config.preprocessor_file_path
            )
        except Exception as e:
            raise CustomException(e,sys)
        

if __name__=='__main__':
    obj = DataTransformation()
    pros = obj.get_preprocessor_object()
    train,test,pro = obj.initiate_data_transformation('/Users/jatin/Desktop/Diamond_price_prediction/artifacts/train.csv','/Users/jatin/Desktop/Diamond_price_prediction/artifacts/test.csv')
    print(pro)
    