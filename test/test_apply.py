import os
import boto3
import pytest
import tftest


@pytest.fixture(scope="session")
def fixtures_dir():
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def output(fixtures_dir):
    tf = tftest.TerraformTest(".", fixtures_dir)
    tf.setup()
    tf.apply()
    yield tf.output()
    tf.destroy(**{"auto_approve": True})


def invoke_lambda(function_arn):
    client = boto3.client("lambda")
    response = client.invoke(FunctionName=function_arn)
    return response


def get_lambda_config(function_arn):
    client = boto3.client("lambda")
    response = client.get_function(FunctionName=function_arn)
    return response


def test_lambda_function_has_correct_env_vars(output):
    """Checks that deployed Lambda has the correct env var"""
    function_arn = output["function_arn"]
    assert get_lambda_config(function_arn)["Configuration"]["Environment"]["Variables"] == {"FOO": "bar"}


def test_lambda_function_returns_200(output):
    """Invokes the deployed Lambda and ensures it returns a 200 http response"""
    function_arn = output["function_arn"]
    assert invoke_lambda(function_arn)["StatusCode"] == 200
