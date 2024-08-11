import flask
import functions_framework

@functions_framework.http
def main(request: flask.Request) -> flask.typing.ResponseReturnValue:
    return "Hello world!"
