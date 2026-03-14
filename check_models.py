from google import genai

client = genai.Client(api_key="AIzaSyC3X5scueLSZlzoWuA8aihFNECUYChC2-c")

for m in client.models.list():
    print(m.name)