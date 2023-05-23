"""
kicks off Step Function executions

THIS DOES NOT WORK FOR INLINE MAP 

{
  "manifest":{    
    "bucket_name": "test-bench",
    "bucket_prefix": "TBS"
  }
}
    

"""
import json
import logging
import os
import boto3

logger = logging.getLogger(__name__)

s3_client = boto3.client(service_name='s3')
list_object_paginator = s3_client.get_paginator('list_objects_v2')

def lambda_handler(event, _):  # sourcery skip: raise-specific-error
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    logger.setLevel(log_level)
    logger.info(f"LOG_LEVEL: {log_level}")
    logger.info(json.dumps(event))
    
    manifest = event.get('manifest')
    if not manifest:
        raise Exception("no manifest")
    bucket_name = manifest.get('bucket_name')
    bucket_prefix = manifest.get('bucket_prefix')
   
    if not bucket_name:
        raise Exception("no BUCKET_NAME set")
    logger.info(f"BUCKET_NAME: {bucket_name}")
    
    if not bucket_prefix:
        raise Exception("no BUCKET_PREFIX set")
    logger.info(f"BUCKET_PREFIX: {bucket_prefix}")
    
    pages = list_object_paginator.paginate(
        Bucket=bucket_name,
        Prefix=bucket_prefix
    )
    
    profiles = []
    acceptedFiles = ['pdf', 'tif', 'tiff', 'jpg', 'png']
    for page in pages:
        for content in page.get('Contents'):
            file = content.get('Key')
            if file.split('/')[-1]:        
                fileType = file.split('.')[-1]
                if fileType.lower() in acceptedFiles:
                    profiles.append(
                        {"s3Path": f"s3://{bucket_name}/{file}"}                    
                    )
                    
    logger.info(f"Total Files: {len(profiles)}")                

    s3_client.put_object(
        Body=json.dumps(profiles),
        Bucket=bucket_name,
        Key=f"{bucket_prefix}/profile/profiles.json"
    )
    
    logger.info(f"bucket_name: {bucket_name} key: {bucket_prefix}/profile/profiles.json")
    
    return {"bucket_name": bucket_name, "key": f"{bucket_prefix}/profile/profiles.json"}