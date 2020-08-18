
# Voting App in Serverless AWS CDK

This is a simple voting app built using Serverless stack in AWS CDK.

<a href="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png"><img src="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png" height="600" width="485" ></a>

Generally the application is built in [Jamstack architecture](https://jamstack.wtf). The frontend is a VueJS + NuxtJS application served from **AWS CloudFront** (CDN) and **AWS S3** (Origin). The API Server is built in FaaS model. It consist of:

- **API Gateway (HTTP API)** for traffic routing
- **AWS Lambda** functions for each endpoints
- **AWS Lambda Layer** to setup Python dependencies
- **AWS Cognito** as identity provider
- **DynamoDB** tables for data persistence
- **DynamoDB Streams** & consumer worker to update aggregated-vote DynamoDB table
- **SQS Queue** in the middle to theoretically withstand high number of request per second of voting endpoint so that DynamoDB will not be throttled & lost.
- **X-Ray** for distributed tracing
- **S3** for frontend static hosting
- **Cloudfront** for frontend static caching
- **AWS Certificate Manager** to manage SSL certs

This architecture is intentionally made in more sophisticated way for me to touch more AWS services.

## Motivation

Why am I doing this? I am learning AWS and serverless technology. This is my first time writing a fullstack serverless application. This is my playground to learn CDK and AWS services generally.

## Personal Takeways / Lesson Learned

- **[AWS CloudFront]** When deploying SSR websites on CloudFront, you cannot point the origin to S3 Bucket. Instead, you have to point the origin to S3 DNS name (eg. `<bucket>.s3-website.us-east-2.amazonaws.com`) as Custom Origin, not S3 Origin.
- **[AWS API Gateway]** It's almost impossible to write a API Doc for AWS API Gateway HTTP API, so use REST API if you planning to have one.
- **[AWS API Gateway]** Generally, it's better to use API Gateway REST API instead of HTTP API but remember to use all the extra you get out of it like request mapper (to SQS, DynamoDB, etc.) with Apache VTL, request/response validation, caching, API doc, API keys, request transformation, edge-optimized, AWS WAF protection, etc.
- **[AWS API Gateway HTTP API]** Refer [here](https://auth0.com/blog/securing-aws-http-apis-with-jwt-authorizers/#Add-a-JWT-Authorizer-to-Your-API) on how to secure HTTP API with JWT authorizer.
- **[AWS Lambda]** In order to setup Python deps packages, you have to use Lambda Layer where it will be mounted in `/opt/` in actual Lambda function. For Python 3.8, you have to put the files in `./python/lib/python3.8/site-packages/` so that the Lambda function can use the packages correctly.
- **[NuxtJS]** You cannot write a `<nuxt-link>` in `<b-navbar>` tag. It will cause a hydration issue. Use this instead: `<b-navbar-item tag="router-link" :to="{ path: '/' }">`.
- **[NuxtJS]** Refer [here](https://www.youtube.com/watch?v=fzcG5Oe31bo) for tutorial on how to build a AWS Cognito integration with Nuxt JS.
- **[NuxtJS]** I tried to use Amplify Auth Vue UI Component for frontend to authenticate user, however, the page is not reactive and slows down the system. The UI Component is somehow big and make the web app bloated.

## Manual Setup (out of CDK)

- Domain setup in Namecheap
- SSL cert request from AWS Cert Manager (ACM)
- AWS API Gateway HTTP API request authorizer. AWS CDK seems to be lacking on this as of now (Aug 2020). There's no method to properly set this up in apigatewayv2 class.

## Things can be improved

/* not necessarily to be done.

- Unittests on all modules
- Better error handling in NuxtJS & Python code
- Write API doc (manually)
- A more flexible way to add answers in frontend
- CI/CD setup
- E2E testing
- Tune the AWS Lambda and choose the right-size Lambda
- Optimize the DynamoDB table (read Alex Debrie's book)

## Demo

Reserved for demo

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
