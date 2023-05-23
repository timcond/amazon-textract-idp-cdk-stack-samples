from constructs import Construct
import os
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_stepfunctions as sfn
import aws_cdk.aws_stepfunctions_tasks as tasks
import aws_cdk.aws_lambda as lambda_
from aws_cdk import (CfnOutput, RemovalPolicy, Stack, Duration)
import amazon_textract_idp_cdk_constructs as tcdk
    """
    PUT IN THE DECIDER AND TEST THIS WITH IT THEY SHOULD TAKE IT NO PROBLEM
    """

class S3ScaleAsyncWorkflowStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        
        # How do I tag my stack with CDK?
        # How do I run a lambda after deployment with CDK?
        
        
        super().__init__(scope, construct_id, **kwargs)

        script_location = os.path.dirname(__file__)
        s3_upload_prefix = "uploads"
        s3_output_prefix = "textract-output"
        s3_temp_output_prefix = "textract-temp-output"
        
        # aws_cdk.Tag("Cost Center", "S3ScaleAsyncWorkflowStack").visit(scope) look into tagging

        # BEWARE! This is a demo/POC setup, remove the auto_delete_objects=True and
        document_bucket = s3.Bucket(self,
                                    "S3ScaleAsyncWorkflowStack-Bucket",
                                    auto_delete_objects=True,
                                    removal_policy=RemovalPolicy.DESTROY)
        s3_output_bucket = document_bucket.bucket_name
        workflow_name = "S3ScaleAsyncWorkflowStack"

        textract_async_task = tcdk.TextractGenericAsyncSfnTask(
            self,
            "TextractAsync",
            s3_output_bucket=s3_output_bucket,
            s3_temp_output_prefix=s3_temp_output_prefix,
            integration_pattern=sfn.IntegrationPattern.WAIT_FOR_TASK_TOKEN,
            lambda_log_level="DEBUG",
            timeout=Duration.hours(24),
            input=sfn.TaskInput.from_object({
                "Token":
                sfn.JsonPath.task_token,
                "ExecutionId":
                sfn.JsonPath.string_at('$$.Execution.Id'),
                "Payload":
                sfn.JsonPath.entire_payload,
            }),
            result_path="$.textract_result")

        textract_async_to_json = tcdk.TextractAsyncToJSON(
            self,
            "AsyncToJSON",
            s3_output_prefix=s3_output_prefix,
            s3_output_bucket=s3_output_bucket)

        async_chain = sfn.Chain.start(textract_async_task).next(textract_async_to_json)

        sfn_map = sfn.Map(
            self,
            "Map State",
            items_path=sfn.JsonPath.string_at('$'),
            parameters={
                "manifest": {
                    "s3Path.$":sfn.JsonPath.string_at("States.Format($$.Map.Item.Value.fileURI)")
                }
            })

        sfn_map.iterator(async_chain)

        workflow_chain = sfn.Chain.start(sfn_map)

        state_machine = sfn.StateMachine(
            self,
            workflow_name,
            definition=workflow_chain,
            # logging_configuration=stepfunctions.CfnStateMachine.LoggingConfigurationProperty(
            #     destinations=[stepfunctions.CfnStateMachine.LogDestinationProperty(
            #         cloud_watch_logs_log_group=stepfunctions.CfnStateMachine.CloudWatchLogsLogGroupProperty(
            #             log_group_arn="logGroupArn"
            #         )
            #     )],
            #     include_execution_data=False,
            #     level="level"
            # ),
            # tags=[stepfunctions.CfnStateMachine.TagsEntryProperty(
            #     key="key",
            #     value="value"
            # )],
            # tracing_configuration=stepfunctions.CfnStateMachine.TracingConfigurationProperty(
            #     enabled=False
            # )
        )
        
        lambda_step_start_step_function = lambda_.DockerImageFunction(
            self,
            "LambdaStartS3Workflow",
            code=lambda_.DockerImageCode.from_image_asset(
                os.path.join(script_location, '../lambda/starts3workflow')),
            memory_size=128,
            architecture=lambda_.Architecture.X86_64,
            environment={
                "STATE_MACHINE_ARN": state_machine.state_machine_arn, 
                "BUCKET_NAME": "test-bench",
                "BUCKET_PREFIX": "curated_500",
                })

        lambda_step_start_step_function.add_to_role_policy(
            iam.PolicyStatement(actions=['states:StartExecution'],
                                resources=[state_machine.state_machine_arn]))

        # OUTPUT
        CfnOutput(
            self,
            "DocumentUploadLocation",
            value=f"s3://{document_bucket.bucket_name}/{s3_upload_prefix}/")
        CfnOutput(
            self,
            "StartStepFunctionLambdaLogGroup",
            value=lambda_step_start_step_function.log_group.log_group_name)
        current_region = Stack.of(self).region
        CfnOutput(
            self,
            'StepFunctionFlowLink',
            value=
            f"https://{current_region}.console.aws.amazon.com/states/home?region={current_region}#/statemachines/view/{state_machine.state_machine_arn}"
        )
