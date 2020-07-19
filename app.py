#!/usr/bin/env python3

from aws_cdk import core

from voting_serverless_cdk.voting_serverless_cdk_stack import VotingServerlessCdkStack


app = core.App()
VotingServerlessCdkStack(app, "voting-serverless-cdk")

app.synth()
