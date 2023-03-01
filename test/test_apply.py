import os
import json
import boto3
import pytest
import tftest

tf_dir = os.path.dirname(os.path.abspath(__file__))


class TestLambdaIntegration:
    @pytest.fixture
    def output(self):
        tf = tftest.TerraformTest(tfdir=tf_dir)
        tf.setup()
        tf.apply()
        yield tf.output()
        tf.destroy(**{"auto_approve": True})

    def invoke_lambda(self, function_arn):
        client = boto3.client("lambda")
        return client.invoke(FunctionName=function_arn)

    def get_lambda_config(self, function_arn):
        client = boto3.client("lambda")
        return client.get_function(FunctionName=function_arn)

    def test_lambda_function_has_correct_env_vars(self, output):
        """Checks that deployed Lambda has the correct env var"""
        function_arn = output["function_arn"]
        assert self.get_lambda_config(function_arn)["Configuration"]["Environment"]["Variables"] == {"FOO": "bar"}

    def test_lambda_function_invocation(self, output):
        """Invokes the deployed Lambda and ensures it returns the expected response"""
        function_arn = output["function_arn"]
        lambda_response = self.invoke_lambda(function_arn)
        assert lambda_response["StatusCode"] == 200
        response_body = json.loads(lambda_response["Payload"].read().decode("utf-8"))
        assert response_body["body"]["Arn"] == "arn:aws:sts::854268402788:assumed-role/app_role/terraform_test"
