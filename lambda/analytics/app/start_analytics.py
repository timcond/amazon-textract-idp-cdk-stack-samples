import numpy as np
import pandas as pd
import json
import logging


#Analyze Textract Response

#Write to DynamoDB

logger = logging.getLogger(__name__)
version = "0.0.3"

def lambda_handler(event, _):
    logger.info(f"Starting Textract-Analytics version {version}")
    logger.info(f"Received event: {event}")
    
    textract_output_json_path = event.get('TextractOutputJsonPath')
    logger.info(f"TextractOutputJsonPath: {textract_output_json_path}")
    
    
    
    
    

