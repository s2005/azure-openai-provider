import json
import os
import sys
from dataclasses import dataclass

from openai import AzureOpenAI

DEFAULT_API_VERSION = '2024-02-01'

endpoint: str
api_key: str
deployment_name: str
api_version: str

@dataclass
class AzureConfig:
    endpoint: str
    deployment_name: str
    api_key: str
    api_version: str

    def to_json(self):
        return json.dumps(
            self,
            default=lambda o: o.__dict__,
            sort_keys=True)


async def get_azure_config(model_name: str | None = None) -> AzureConfig | None:
    global endpoint
    global api_key
    global deployment_name
    global api_version

    if 'GPTSCRIPT_AZURE_ENDPOINT' in os.environ and 'GPTSCRIPT_AZURE_API_KEY' in os.environ:
        endpoint = os.environ['GPTSCRIPT_AZURE_ENDPOINT']
        api_key = os.environ['GPTSCRIPT_AZURE_API_KEY']
    if 'GPTSCRIPT_AZURE_DEPLOYMENT_NAME' in os.environ:
        deployment_name = os.environ['GPTSCRIPT_AZURE_DEPLOYMENT_NAME']
    elif model_name is not None:
        deployment_name = model_name
    if 'GPTSCRIPT_AZURE_API_VERSION' in os.environ:
        api_version = os.environ['GPTSCRIPT_AZURE_API_VERSION']
    else:
        api_version = DEFAULT_API_VERSION

    if 'endpoint' in globals() and 'api_key' in globals() and 'deployment_name' in globals() and 'api_version' in globals():
        return AzureConfig(
            endpoint=endpoint,
            api_key=api_key,
            deployment_name=deployment_name,
            api_version=api_version
        )

    return None


def client(endpoint: str, deployment_name: str, api_key: str, api_version: str) -> AzureOpenAI:
    return AzureOpenAI(
        azure_endpoint=endpoint,
        azure_deployment=deployment_name,
        api_key=api_key,
        api_version=api_version
    )


if __name__ == "__main__":
    import asyncio

    config = asyncio.run(get_azure_config())

    if config is None:
        print("Azure config not found. Please ensure you have configured the environment variables correctly.")
        sys.exit(1)

    env = {
        "env": {
            "GPTSCRIPT_AZURE_API_KEY": config.api_key,
            "GPTSCRIPT_AZURE_ENDPOINT": config.endpoint,
            "GPTSCRIPT_AZURE_DEPLOYMENT_NAME": config.deployment_name,
            "GPTSCRIPT_AZURE_API_VERSION": config.api_version
        }
    }
    print(json.dumps(env))
