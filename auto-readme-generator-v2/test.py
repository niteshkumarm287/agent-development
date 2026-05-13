from google import genai
from google.oauth2 import service_account

PROJECT_ID = "game-d8160"
LOCATION = "global"

credentials = service_account.Credentials.from_service_account_file(
    "/tmp/gcp-sa.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

client = genai.Client(
    vertexai=True,
    project=PROJECT_ID,
    location=LOCATION,
    credentials=credentials,
)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="hello",
)

print(response.text)