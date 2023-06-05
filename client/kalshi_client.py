import kalshi_python
import yaml


class AuthedApiInstance(kalshi_python.ApiInstance):
    def __init__(self, config=kalshi_python.Configuration()):
        try:
            creds = yaml.safe_load(open("client/credentials.yaml"))
        except FileNotFoundError:
            raise Exception(
                "Please create a credentials.yaml file in the client directory. See README.md for more info."
            )

        if "username" not in creds or "password" not in creds:
            raise Exception(
                "Please fill out the username and password fields in the credentials.yaml file."
            )

        super().__init__(configuration=config)

        loginResponse = self.login(
            kalshi_python.LoginRequest(
                email=creds["username"], password=creds["password"]
            )
        )
        self.set_api_token(loginResponse.token)
