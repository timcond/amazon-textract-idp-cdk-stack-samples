import boto3

def split_s3_path_to_bucket_and_key(s3_path: str) -> Tuple[str, str]:
    if len(s3_path) <= 7 or not s3_path.lower().startswith("s3://"):
        raise ValueError(
            f"s3_path: {s3_path} is no s3_path in the form of s3://bucket/key."
        )
    s3_bucket, s3_key = s3_path.replace("s3://", "").split("/", 1)
    return (s3_bucket, s3_key)
    

# Read json file from S3 and parse with Textract Response Parser
class ReadJsonFromS3():        
    
    def __init__(self, s3_path):
        self.s3_client = boto3.client('s3')
        self.s3_bucket, self.s3_key = split_s3_path_to_bucket_and_key(s3_path)                
        self.obj = self.s3_client.get_object(self.bucket, self.key)
        self.json = self.obj.get()['Body'].read().decode('utf-8')
        
        
    

    