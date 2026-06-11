"""
References:
- Endpoints for Microsoft Foundry Models: https://learn.microsoft.com/en-us/azure/foundry/foundry-models/concepts/endpoints?tabs=python

"""
import os

import azure.identity
import openai
from dotenv import load_dotenv

# Setup the OpenAI client to use either Azure, OpenAI.com, or Ollama API
load_dotenv(override=True)
API_HOST = os.getenv("API_HOST", "azure")

# Prequisites: SEE fdy_login_rbac.azcli FOR SETTING UP AZURE AUTHENTICATION

print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
print(f"AZURE_OPENAI_CHAT_DEPLOYMENT: {os.getenv('AZURE_OPENAI_CHAT_DEPLOYMENT')}")


if API_HOST == "azure":
    token_provider = azure.identity.get_bearer_token_provider(
        azure.identity.DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = openai.OpenAI(
        base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT'].rstrip('/')}/openai/v1/",
        api_key=token_provider,
    )
    MODEL_NAME = os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"]

elif API_HOST == "ollama":
    client = openai.OpenAI(base_url=os.environ["OLLAMA_ENDPOINT"], api_key="nokeyneeded")
    MODEL_NAME = os.environ["OLLAMA_MODEL"]

else:
    client = openai.OpenAI(api_key=os.environ["OPENAI_KEY"])
    MODEL_NAME = os.environ["OPENAI_MODEL"]


response = client.responses.create(
    model=MODEL_NAME,
    temperature=0.7,
    input=[
        {"role": "system", "content": "You are a helpful assistant that makes lots of cat references and uses emojis."},
        {"role": "user", "content": "What's the weather in SF today?"},
    ],
    store=False,
)

print(f"Response from {API_HOST}: \n")
print(response.output_text)
print("\n\nFull response object:")
print(response.model_dump_json(indent=2))
