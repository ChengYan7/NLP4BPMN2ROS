import openai

# enter your API
openai.api_key = "your API"

# upload your file library
response = openai.File.create(file=open("predefined.jsonl"), purpose="search")

# get your file ID as response
print(response)

# then your can use this ID in the main.py

# "file-aVmfougPtrAX3RA40qSufHqQ"
