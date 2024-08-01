import os
from dotenv import load_dotenv
from typing import Optional


def load_environment() -> None:
    load_dotenv()  # Загружаем общие переменные из .env
    project_stage = os.getenv('PROJECT_STAGE', 'local')
    env_file = f'.env.{project_stage}'
    load_dotenv(env_file)  # Загружаем переменные для конкретной среды


def get_env_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name, default)
    if value is None:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


# Загрузка файла .env
load_environment()

# Получаем значения переменных окружения
MONGO_URI = get_env_variable('MONGO_URI')
MONGO_DB = get_env_variable('MONGO_DB', )
MONGO_COLLECTION = get_env_variable('MONGO_COLLECTION')

REDIS_HOST = get_env_variable('REDIS_HOST')
REDIS_PORT = get_env_variable('REDIS_PORT')
REDIS_DB = get_env_variable('REDIS_DB')

VK_BOT_TOKEN = get_env_variable('VK_BOT_TOKEN')

print(f"MONGO_URI: {MONGO_URI}")
print(f"MONGO_DB: {MONGO_DB}")
print(f"MONGO_COLLECTION: {MONGO_COLLECTION}")
print(f"REDIS_HOST: {REDIS_HOST}")
print(f"REDIS_PORT: {REDIS_PORT}")
print(f"REDIS_DB: {REDIS_DB}")
print(f"VK_BOT_TOKEN: {VK_BOT_TOKEN}")