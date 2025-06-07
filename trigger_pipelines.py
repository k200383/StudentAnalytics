import requests
import json
import os
from azure.identity import ClientSecretCredential
from dotenv import load_dotenv

load_dotenv()


tenant_id = "a1e3cc4f-47e2-4e32-a7a1-5b14136b160b"
client_id = "4d116976-162f-4038-996e-06379e28940d"
client_secret = os.getenv("FABRIC_CLIENT_SECRET")
workspace_id = "4b128012-36fa-4785-9f9b-bf62d6e5a3bb"
pipeline_id = "332993a1-6150-4cc3-96ff-d2ccd2dd6094"

# Get token
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
token = credential.get_token("https://api.fabric.microsoft.com/.default").token

# Pipeline URL
url = f"https://api.fabric.microsoft.com/v1/workspaces/{workspace_id}/pipelines/{pipeline_id}/run"

# Define parameter(s) passed to notebook in the pipeline
payload = {
    "parameters": {
        "files_path": "abfss://TechTest@onelake.dfs.fabric.microsoft.com/BronzeLakehouse.Lakehouse/Files/Raw data"
    }
}

# Trigger pipeline
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
print(response.status_code)
print(json.dumps(response.json(), indent=2))
