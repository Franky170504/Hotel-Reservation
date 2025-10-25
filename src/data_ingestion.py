import os 
import sys
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.path_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_test_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR, exist_ok=True)
    
        logger.info(f"Data ingestion started with {self.bucket_name} and {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            # 1. Hard-coded the correct project ID
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            os.makedirs(os.path.dirname(RAW_FILE_PATH), exist_ok=True)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"File successfully saved in {RAW_FILE_PATH}")

        except Exception as e:
            logger.error("failed to download data from gcp")
            # 2. Added logging for the *original* error
            logger.error(f"Original error: {e}") 
            # 3. Changed 'return' to 'raise'
            raise CustomException("failed to download data", sys.exc_info())
        
    def split_data(self):
        try:
            logger.info("Started with train test split")
            data = pd.read_csv(RAW_FILE_PATH)
            train_data, test_data = train_test_split(data, test_size=1-self.train_test_ratio, random_state=40)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"data saved in {RAW_DIR}")

        except Exception as e:
            logger.error("Error while splitting the data")
            # 4. Added original error logging for consistency
            logger.error(f"Original error: {e}")
            # 5. Changed 'return' to 'raise'
            raise CustomException("Failed to split data", sys.exc_info())
        
    def run(self):
        try:
            logger.info("Starting data ingestion")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data ingestion done")
        
        # 6. This 'except' block now correctly catches the 'raise'
        # from either of the functions above.
        except CustomException as ce: 
            logger.error(f"CustomException : {str(ce)}")

        finally:
            logger.info("Data ingestion Completed")

if __name__ == "__main__":
    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()