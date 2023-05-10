import aws_cdk as core
import aws_cdk.assertions as assertions

from unisal.unisal_stack import UnisalStack

# example tests. To run these tests, uncomment this file along with the example
# resource in unisal/unisal_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = UnisalStack(app, "unisal")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
