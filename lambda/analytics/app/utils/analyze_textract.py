import numpy as np
import pandas as pd
import json

#Read file from S3
from utils.read_from_s3 import ReadJsonFromS3


def sum_list(num_list):
    a = np.array(num_list)
    return np.sum(a)

def get_res_byte_size(textractRes):
    json_string = json.dumps(textractRes)
    bytes_ = json_string.encode("utf-8")
    return len(bytes_)

class AnalyzeTextract:
    def __init__(self, document):
        self.document = ReadJsonFromS3("s3://test-bench/curated_500/W2_XL_input_noisy_1268.jpg")
        self.t_document = t2.TDocumentSchema().load(document)
        self.trp_doc = trp.Document(t2.TDocumentSchema().dump(self.t_document))
        self.num_lines = []
        self.num_tables = []
        self.num_words = []
        self.num_char = []
        self.num_blocks = []
        self.num_form_fields = []

    def analyze(self):
        for page in self.trp_doc.pages:
            lines = list(page.lines)
            words = [word for line in lines for word in line.words]
            char = [char for word in words for char in word.text]

            self.num_lines.append(len(lines))
            self.num_words.append(len(words))
            self.num_char.append(len(char))
            self.num_blocks.append(len(page.blocks))

            if hasattr(page, "tables"):
                self.num_tables.append(len(page.tables))
            else:
                self.num_tables = [0]
            if hasattr(page, "form"):
                self.num_form_fields.append(len(page.form.fields))
            else:
                self.num_form_fields = [0]trp_doc.pages:

#Analyze Textract Response


#Write to DynamoDB
