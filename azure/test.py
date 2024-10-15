from azure.ai.inference import ChatCompletionsClient # type: ignore
from azure.ai.inference.models import SystemMessage, UserMessage # type: ignore
from azure.core.credentials import AzureKeyCredential  # type: ignore
from dotenv import load_dotenv 
import os

load_dotenv()

endpoint = "https://Phi-3-mini-128k-instruct-rsnsn.eastus2.models.ai.azure.com"
api_key = os.getenv("AZURE_API_KEY")

client = ChatCompletionsClient(endpoint=endpoint, credential=AzureKeyCredential(api_key))

response = client.complete(
    messages=[
        SystemMessage(content="You are a helpful assistant."),  
        UserMessage(content="How many feet are in a mile?")      
    ]
)

print(response.choices[0].message.content)
