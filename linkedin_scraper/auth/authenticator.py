import os

import yaml


def authenticate(item: object) -> bool:
    """
    Authenticates a user by validating their API key against a list of valid keys
    stored in a secret YAML file.
    Args:
        item (object): An object containing the attribute `x_api_key`,
                       which represents the user's API key.
    Returns:
        bool: Returns `True` if the provided API key is valid, otherwise `False`.
    """

    # Extracting user's API Key
    x_api_key = item.x_api_key

    # Setting up the Path to the secret file
    BASEPATH = os.path.dirname(__file__)
    path_secretfile = os.path.join(BASEPATH, "secret.yaml")

    # Opening all valid API keys
    with open(path_secretfile, "r") as file:
        valid_api_keys = yaml.safe_load(file)["secret_keys"]

    # Validating with valid x_api_keys
    if x_api_key in valid_api_keys:
        return True
    return False
