import kalshi_python
import yaml


class AuthedApiInstance(kalshi_python.ApiInstance):
    def __init__(
        self,
        config=kalshi_python.Configuration(),
        username_key="username",
        password_key="password",
    ):
        try:
            creds = yaml.safe_load(open("client/credentials.yaml"))
        except FileNotFoundError:
            raise Exception(
                "Please create a credentials.yaml file in the client directory. "
                + "See README.md for more info."
            )

        if username_key not in creds or password_key not in creds:
            raise Exception(
                "Please fill out the username and password fields in the "
                + "credentials.yaml file."
            )

        super().__init__(
            configuration=config,
            email=creds[username_key],
            password=creds[password_key],
        )
