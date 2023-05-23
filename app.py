#!/usr/bin/env python3
import aws_cdk as cdk

from textract_cdk_stack_samples.paystub_w2_comprehend_classification import PaystubAndW2Comprehend
from textract_cdk_stack_samples.demo_with_queries_stack import DemoQueries
from textract_cdk_stack_samples.analyze_expense import AnalyzeExpenseStack
from textract_cdk_stack_samples.analyze_id import AnalyzeIDStack
from textract_cdk_stack_samples.insurance import InsuranceStack
from textract_cdk_stack_samples.paystub_w2_spacy import PaystubAndW2Spacy
from textract_cdk_stack_samples.simple_async_workflow import SimpleAsyncWorkflow
from textract_cdk_stack_samples.simple_sync_workflow import SimpleSyncWorkflow
from textract_cdk_stack_samples.simple_async_and_sync_workflow import SimpleSyncAndAsyncWorkflow
from textract_cdk_stack_samples.document_split_workflow import DocumentSplitterWorkflow
from textract_cdk_stack_samples.lending_workflow import LendingWorkflow
from textract_cdk_stack_samples.generate_csv_workflow import GenerateCSVWorkflow
from textract_cdk_stack_samples.simple_searchPDF import SimpleSearchPDF
from textract_cdk_stack_samples.s3_scale_async_workflow import S3ScaleAsyncWorkflowStack

app = cdk.App()

PaystubAndW2Comprehend(
    app,
    "PaystubAndW2Comprehend",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */
    # env=cdk.Environment(account='<account_id>', region='<region-name>'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
)

DemoQueries(app, "DemoQueries")
AnalyzeExpenseStack(app, "AnalyzeExpense")
AnalyzeIDStack(app, "AnalyzeID")
InsuranceStack(app, "InsuranceStack")
PaystubAndW2Spacy(app, "PaystubAndW2Spacy")
SimpleAsyncWorkflow(app, "SimpleAsyncWorkflow")
SimpleSyncWorkflow(app, "SimpleSyncWorkflow")
SimpleSyncAndAsyncWorkflow(app, "SimpleSyncAndAsyncWorkflow")
DocumentSplitterWorkflow(app, "DocumentSplitterWorkflow")
LendingWorkflow(app, "LendingWorkflow")
GenerateCSVWorkflow(app, "GenerateCSVWorkflow")
SimpleSearchPDF(app, "SimpleSearchPDF")
S3ScaleAsyncWorkflowStack(app, "S3ScaleAsyncWorkflowStack")

app.synth()
