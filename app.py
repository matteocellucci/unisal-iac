#!/usr/bin/env python3
import os

import aws_cdk as cdk

from unisal.cdk_pipeline import PipelineStack


app = cdk.App()
PipelineStack(app, "PipelineStack")

app.synth()
