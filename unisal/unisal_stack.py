from aws_cdk import (
    Stack,
    aws_cognito as _cognito,
    aws_apigateway as _apigateway,
    aws_lambda as _lambda,
    aws_dynamodb as _dynamodb
)
from constructs import Construct
from os import path


class UnisalStack(Stack):

    books_path = path.join("./", "books")

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        user_pool = _cognito.UserPool(self, f'{construct_id}-pool')
        user_pool.add_client("books",
                             auth_flows=_cognito.AuthFlow(user_password=True),
                             supported_identity_providers=[_cognito.UserPoolClientIdentityProvider.COGNITO])

        auth = _apigateway.CognitoUserPoolsAuthorizer(self, f'{construct_id}-auth', cognito_user_pools=[user_pool])

        backend = _lambda.Function(self, f'{construct_id}-fn-books',
                                   runtime=_lambda.Runtime.PYTHON_3_9,
                                   handler="index.handler",
                                   code=_lambda.Code.from_asset(UnisalStack.books_path))

        api = _apigateway.LambdaRestApi(self, f'{construct_id}-api', handler=backend, proxy=False)

        resource_books = api.root.add_resource("books")
        resource_books.add_method("POST", authorizer=auth, authorization_type=_apigateway.AuthorizationType.COGNITO)

        resource_book_id = resource_books.add_resource("{book_id}")
        resource_book_id.add_method("GET", authorizer=auth, authorization_type=_apigateway.AuthorizationType.COGNITO)
        resource_book_id.add_method("PUT", authorizer=auth, authorization_type=_apigateway.AuthorizationType.COGNITO)
        resource_book_id.add_method("DELETE", authorizer=auth, authorization_type=_apigateway.AuthorizationType.COGNITO)

        key = _dynamodb.Attribute(name='book_name', type=_dynamodb.AttributeType.STRING)
        table = _dynamodb.Table(self, f'{construct_id}-table', table_name='books', partition_key=key)
        table.grant_read_write_data(backend)
