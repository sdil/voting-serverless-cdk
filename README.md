
# Voting App in Serverless AWS CDK

This is a simple voting app built using Serverless stack in AWS CDK.

See me building this app in public in this [Twitter thread](https://twitter.com/sdil/status/1284816892301959168).

<a href="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png"><img src="https://raw.githubusercontent.com/sdil/voting-serverless-cdk/master/architecture.png" height="600" width="485" ></a>

Generally the application is built in [Jamstack architecture](https://jamstack.wtf). The frontend is a VueJS + NuxtJS application served from **AWS CloudFront** (CDN) and **AWS S3** (Origin). The API Server is built in FaaS model. It consist of:

- **API Gateway (HTTP API)** for traffic routing
- **AWS Lambda** functions for each endpoint
- **AWS Lambda Layer** to setup Python dependencies
- **AWS Cognito** as an identity provider
- **DynamoDB** tables for data persistence
- **DynamoDB Streams** & consumer worker to update aggregated-vote DynamoDB table
- **SQS Queue** in the middle to withstand high number of request per second of voting endpoint so that DynamoDB will not be throttled & lost.
- **X-Ray** for distributed tracing
- **S3** for frontend static hosting
- **Cloudfront** for frontend static caching
- **AWS Certificate Manager** to manage SSL certs

This architecture is intentionally made in a more sophisticated way for me to touch more AWS services.

# Table of Contents

- [Motivation](#motivation)
- [Demo](#demo)
- [Benchmark](#benchmakr)
- [Manual Setup (out of CDK)](#manual-setup-out-of-cdk)
- [Things can be improved](#things-can-be-improved)
- [Personal Takeaways / Lesson Learned](#personal-takeaways--lesson-learned)
- [Deploy on Your AWS Account](#deploy-on-your-aws)
- [References](#references)

## Motivation

Why am I doing this? I am learning AWS and serverless technology. This is my first time writing a fullstack serverless application. This is my playground to learn CDK and AWS services generally.

## Demo

Reserved for demo

## Benchmark

Reserved for benchmark

## Manual Setup (out of CDK)

- Domain setup in Namecheap
- SSL cert request from AWS Cert Manager (ACM). It require manual CNAME setup for domain verification from ACM.
- AWS API Gateway HTTP API request authorizer. AWS CDK seems to be lacking on this as of now (Aug 2020). There's no method to properly set this up in apigatewayv2 class.
- X-Ray setup

## Things can be improved

\* not necessarily to be done.

- Write unit tests on all modules
- Local testing to test the API & integration with AWS services
- Benchmark the API performance
- Better error handling in NuxtJS & Python code
- Write API doc (manually)
- Support multiple answer choices when creating poll
- CI/CD setup. Currently I'm pushing to prod from CDK CLI
- E2E testing
- Support all CRUD operations
- Support pagination on polls listing on the main page
- Tune the AWS Lambda and choose the right-size Lambda
- Optimize the DynamoDB table (read [Alex Debrie's book](https://www.dynamodbbook.com/))
- Add monitoring & alerting (refer [this article](https://lumigo.io/blog/what-alerts-should-you-have-for-serverless-applications/) by Yan Chui)
- Use [AWS Lambda Powertools](https://github.com/awslabs/aws-lambda-powertools-python) for logging, tracing & metrics

## Personal Takeaways / Lesson Learned

- **[AWS CloudFront]** When deploying SSR websites on CloudFront, you cannot point the origin to S3 Bucket. Instead, you have to point the origin to S3 DNS name (eg. `<bucket>.s3-website.us-east-2.amazonaws.com`) as Custom Origin, not S3 Origin.
- **[AWS API Gateway]** It's almost impossible to write an API Doc for AWS API Gateway HTTP API, so use REST API if you planning to have one.
- **[AWS API Gateway]** Generally, it's better to use API Gateway REST API instead of HTTP API but remember to use all the extra you get out of it like request mapper (to SQS, DynamoDB, etc.) with Apache VTL, request/response validation, caching, API doc, API keys, request transformation, edge-optimized, throttling, AWS WAF protection, etc.
- **[AWS API Gateway HTTP API]** 
- **[AWS Lambda]** In order to setup Python deps packages, you have to use Lambda Layer where it will be mounted in `/opt/` in an actual Lambda function. For Python 3.8, you have to put the files in `./python/lib/python3.8/site-packages/` so that the Lambda function can use the packages correctly.
- **[AWS Lambda & AWS API Gateway]** The `event` payload from API Gateway contains a lot more data than I expected. Always test E2E by invoking the Lambda function from API Gateway to see the full data.
- **[NuxtJS]** You cannot write a `<nuxt-link>` in `<b-navbar>` tag. It will cause a hydration issue. Use this instead: `<b-navbar-item tag="router-link" :to="{ path: '/' }">`.
- **[NuxtJS]** I tried to use Amplify Auth Vue UI Component for frontend to authenticate user, however, the page is not reactive and slows down the system. The UI Component is somehow big and make the web app bloated.

## Deploy on Your AWS Account

```
# Start a Python virtualenv
$ python3 -m venv .env

# Activate the virtualenv
$ source .env/bin/activate

# Once the virtualenv is activated, you can install the required dependencies.
$ pip install -r requirements.txt

# At this point you can now synthesize the CloudFormation template for this code.
$ cdk synth

# Install Python dependencies for Lambda Layer
$ make install-python-deps

# Move .env.sample file to .env
$ mv ./frontend/.env.sample ./frontend/.env
```

Replace the variables in `./frontend/.env`

Deploy the CDK

```
$ cdk deploy *
```

Refer [Manual Setup](#manual-setup-out-of-cdk) section to setup on your services outside of CDK.

Enjoy!

## References

Thanks to these articles that helped me to make this project reality.

- [How to add authentication using AWS Amplify's Auth Class in a Nuxt app (Auth Part 1)](https://www.youtube.com/watch?v=fzcG5Oe31bo) by jagr.co. How to use a AWS Amplify Auth (Cognito) in Nuxt JS.
- [User management in Vue.js with AWS Cognito](https://medium.com/js-dojo/user-management-in-vue-js-with-aws-cognito-1905511b93b) by Christopher Bartling. How to fetch AWS Cognito signed in user token & refresh it when it's expiring.
- [How to secure HTTP API with JWT authorizer](https://auth0.com/blog/securing-aws-http-apis-with-jwt-authorizers/#Add-a-JWT-Authorizer-to-Your-API) by Auth0.
