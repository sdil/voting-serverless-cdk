
# Voting App in Serverless AWS CDK

## Introduction

## Motivation

Why am I doing this? I am learning AWS and serverless technology. This is my first time writing a fullstack serverless application. This is my playground to learn CDK and AWS services generally.

## Architecture

![Voting App Architecture](architecture.png | width=500)

Generally the application is built in [Jamstack architecture](https://jamstack.wtf). The frontend is a VueJS + NuxtJS application served from AWS CloudFront (CDN) and AWS S3 (Origin). The API Server is built in FaaS model. It consist of:

- API Gateway HTTP API
- Lambda functions for each endpoints
- AWS Cognito as identity provider
- DynamoDB tables for data persistence
- SQS Queue in the middle to theoretically withstand high number of request per second of voting endpoint so that DynamoDB will not be throttled

This architecture is intentionally made in more sophisticated way for me to touch more AWS services.

## Contributing

Start a Python virtualenv

```
$ python3 -m venv .env
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .env/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .env\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
