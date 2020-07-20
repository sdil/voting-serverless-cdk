import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="voting_serverless_cdk",
    version="0.0.1",
    description="An empty CDK Python app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="author",
    package_dir={"": "voting_serverless_cdk"},
    packages=setuptools.find_packages(where="voting_serverless_cdk"),
    install_requires=[
        "aws-cdk.core==1.52.0",
        "aws-cdk.aws_lambda",
        "aws-cdk.aws_apigatewayv2",
        "aws-cdk.aws_dynamodb",
        "aws_cdk.aws_lambda_event_sources",
        "aws_cdk.aws_sqs",
        "aws_cdk.aws_cognito",
        "aws_cdk.aws_cloudfront",
        "aws_cdk.aws_s3",
        "aws_cdk.aws_s3_deployment",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
