import openai

# enter your API
openai.api_key = "API"

# upload your train dataset
response = openai.File.create(file=open("labeled examples 3.jsonl"), purpose="classifications")

# get your file ID as response
print(response)

# then your can use this ID in the main.py

#  only definition of primitive
#  "filename": "labeled examples.jsonl",
#  "id": "file-PovQSNq6cQozNGRdH8IYCowu",

# primitive and definition
#  "filename": "labeled examples 2.jsonl",
#  "id": "file-C0qj8kQWTheFwcZvUbIQ0UKJ",

# primitive and its synonyms and definition
#   "filename": "labeled examples 3.jsonl",
#   "id": "file-I2XzSpsdqtEDxe4sMOcH87UH",
