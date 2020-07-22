
# Voting App in Serverless AWS CDK

This is a simple voting app built using Serverless stack in AWS CDK.

<a href="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png"><img src="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png" height="600" width="470" ></a>

Generally the application is built in [Jamstack architecture](https://jamstack.wtf). The frontend is a VueJS + NuxtJS application served from **AWS CloudFront** (CDN) and **AWS S3** (Origin). The API Server is built in FaaS model. It consist of:

- **API Gateway (HTTP API)** for traffic routing
- **Lambda** functions for each endpoints
- **AWS Cognito** as identity provider
- **DynamoDB** tables for data persistence
- **DynamoDB Streams** & consumer worker to update aggregated-vote DynamoDB table
- **SQS Queue** in the middle to theoretically withstand high number of request per second of voting endpoint so that DynamoDB will not be throttled
- **X-Ray** for distributed tracing
- **Route53** for DNS routing *(TODO)*

This architecture is intentionally made in more sophisticated way for me to touch more AWS services.

## Motivation

Why am I doing this? I am learning AWS and serverless technology. This is my first time writing a fullstack serverless application. This is my playground to learn CDK and AWS services generally.

## Personal Takeways / Lesson Learned

- When deploying SSR websites on CloudFront, you cannot point the origin to S3 Bucket. Instead, you have to point the origin to S3 DNS name (eg. `<bucket>.s3-website.us-east-2.amazonaws.com`) as Custom Origin, not S3 Origin.

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
