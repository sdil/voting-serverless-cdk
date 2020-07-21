#!/usr/bin/env python3

from aws_cdk import core

from voting_serverless_cdk.voting_serverless_cdk_stack import (
    VotingServerlessCdkStack,
    VotingFrontendCdkStack,
)


app = core.App()
VotingServerlessCdkStack(app, "voting-serverless-cdk")
VotingFrontendCdkStack(app, "voting-frontend-cdk")

app.synth()
