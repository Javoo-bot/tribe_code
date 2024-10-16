import os
import requests
import dotenv

dotenv.load_dotenv()

deployment_name = os.environ['COMPLETIONS_MODEL']
openai_api_base = os.environ['AZURE_OPENAI_ENDPOINT']
openai_api_key = os.environ['AZURE_OPENAI_API_KEY']
openai_api_version = os.environ['OPENAI_API_VERSION']

api_url = f"https://testeo2.openai.azure.com/openai/deployments/gpt-35-turbo/completions?api-version=2024-08-01-preview"

# Example prompt for request payload
prompt = "Hello world"

json_data = {
  "prompt": prompt,
  "temperature": 0,
  "max_tokens": 30
}

# Including the api-key in HTTP headers
headers =  {"api-key": openai_api_key}

try: 
  # Request for creating a completion for the provided prompt and parameters
  response = requests.post(api_url, json=json_data, headers=headers)

  completion = response.json()
    
  # print the completion
  print(completion['choices'][0]['text'])
    
  # Here indicating if the response is filtered
  if completion['choices'][0]['finish_reason'] == "content_filter":
    print("The generated content is filtered.")

except:
    print("An exception has occurred. \n")