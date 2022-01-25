import openai

# enter your API
openai.api_key = "API"

# upload your train dataset
response = openai.File.create(file=open("labeled examples 2.jsonl"), purpose="classifications")

# get your file ID as response
print(response)

# then your can use this ID in the main.py

#  "filename": "labeled examples.jsonl",
#  "id": "file-PovQSNq6cQozNGRdH8IYCowu",

#  "filename": "labeled examples 2.jsonl",
#  "id": "file-C0qj8kQWTheFwcZvUbIQ0UKJ",
