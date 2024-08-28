import os

from dotenv import load_dotenv
from typing import Optional


def load_environment() -> None:
    """Load environment variables from .env files based on the project stage."""
    # Load common variables from .env
    load_dotenv()
    project_stage = os.getenv('PROJECT_STAGE', 'local')
    env_file = f'.env.{project_stage}'
    # Load environment-specific variables
    load_dotenv(env_file)


def get_env_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    """Retrieve an environment variable or raise an error if it is missing.

    Args:
        name (str): The name of the environment variable.
        default (Optional[str]): The default value if the environment variable is not set.

    Returns:
        Optional[str]: The value of the environment variable.

    Raises:
        EnvironmentError: If the environment variable is not set and no default is provided.
    """
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


load_environment()

MONGO_URI = get_env_variable('MONGO_URI')
MONGO_DB = get_env_variable('MONGO_DB')
MONGO_COLLECTION = get_env_variable('MONGO_COLLECTION')

REDIS_HOST = get_env_variable('REDIS_HOST')
REDIS_PORT = get_env_variable('REDIS_PORT')
REDIS_DB = get_env_variable('REDIS_DB')

VK_BOT_TOKEN = get_env_variable('VK_BOT_TOKEN')
