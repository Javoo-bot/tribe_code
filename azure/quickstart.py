import os
import requests
import dotenv

# Load environment variables from .env file
dotenv.load_dotenv()

# Extracting environment variables for API configuration
deployment_name = os.environ.get('COMPLETIONS_MODEL')
openai_api_base = os.environ.get('AZURE_OPENAI_ENDPOINT')
openai_api_key = os.environ.get('AZURE_OPENAI_API_KEY')
openai_api_version = os.environ.get('OPENAI_API_VERSION')

# Construct the API URL using environment variables
api_url = f"{openai_api_base}/openai/deployments/{deployment_name}/chat/completions?api-version={openai_api_version}"

# Example prompt for the request payload
json_data = {
 "messages": [
  {
   "role": "system",
   "content": "you're a helpful assistant that talks like a pirate"
  },
  {
   "role": "user",
   "content": "can you tell me how to care for a parrot?"
  }
 ]
}

# Including the api-key in HTTP headers
headers = {
    "api-key": openai_api_key,
    "Content-Type": "application/json"
}

try: 
    # Request for creating a completion for the provided prompt and parameters
    response = requests.post(api_url, json=json_data, headers=headers)
    response.raise_for_status()  # Raise an error for bad HTTP status codes

    completion = response.json()
    
    # Print the completion text
    print(completion['choices'][0]['message']['content'])
    
    # Check if the response was filtered
    if completion['choices'][0].get('finish_reason') == "content_filter":
        print("The generated content is filtered.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
