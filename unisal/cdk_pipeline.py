from aws_cdk import (
    Stack,
    Stage,
    aws_codecommit as _codecommit,
    pipelines as _pipelines,
)
from constructs import Construct
from unisal.unisal_stack import UnisalStack


class AppStage(Stage):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        UnisalStack(self, "UnisalStack")


class PipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        repo = _codecommit.Repository(self, f'{construct_id}-repo',
            repository_name = 'books',
            description = 'Repository for books system')

        synth_step = _pipelines.ShellStep("Synth",
                               input=_pipelines.CodePipelineSource.code_commit(repo, "main"),
                               commands=[
                                    "npm install -g aws-cdk",
                                    "python -m pip install -r requirements.txt",
                                    "cdk synth"])

        pipeline = _pipelines.CodePipeline(self, f'{construct_id}-pipeline', pipeline_name="books", synth=synth_step)
        pipeline.add_stage(AppStage(self, "app-stage"))
