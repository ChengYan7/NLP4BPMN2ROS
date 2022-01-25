import openai

# enter your API
openai.api_key = "API"

# upload your train dataset
response = openai.File.create(file=open("labeled examples.jsonl"), purpose="classifications")

# get your file ID as response
print(response)

# then your can use this ID in the main.py

#  "filename": "labeled examples.jsonl",
#  "id": "file-PovQSNq6cQozNGRdH8IYCowu",
