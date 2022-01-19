import openai

# enter your API
openai.api_key = "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"

# upload your file library
response = openai.File.create(file=open("predefined skill.jsonl"), purpose="search")

# get your file ID as response
print(response)

# then your can use this ID in the main.py

# "filename": "predefined primitive.jsonl"
# "id": "file-kH1toOuo8l1SEfVR1mda5ZTP"

# "filename": "predefined skill.jsonl"
# "id": "file-azrvWHleyJ83Dov3GcC2pKrp"
