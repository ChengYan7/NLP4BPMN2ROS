import numpy as np
import re
import openai
openai.api_key = "your API"                         # enter your API for GPT-3 here
import json


def nlp_search_results(query, file_ID):
    """
    use GPT-3 model online-application to get the semantic search results

    :param query: the search content, such as: query = "grasp object"
    :param file_ID: pre-defined file library () "file-aVmfougPtrAX3RA40qSufHqQ"
    :return: search response of GPT-3
    """
    search_response = openai.Engine("davinci").search(
        search_model="davinci",
        query=query,
        max_rerank=5,                                   # number of documents
        file=file_ID
    )
    # print(search_response)
    return search_response


def best_score(search_response):
    """
    output the best score in search response

    :param search_response: search result of GPT-3
    :return: the max score of content similarity
    """
    score = re.findall(r"(?<=\"score\": )\d+", search_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    # print('best score：', max_score)
    return max_score


def best_command(search_response):
    """
    output the pre-defined content that get the best score in search response

    :param search_response: search result of GPT-3
    :return: the corresponding command text in pre-defined files
    """
    score = re.findall(r"(?<=\"score\": )\d+", search_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    text = re.findall(r'\"score\": '+max_score+',\n\"text\": (.*?)}', search_response)      # extract the text
    return text


# open BPMN file.json
BPMN = open('data.json', )

# returns JSON object as a dictionary
data = json.load(BPMN)

# Iterating through the json
# list
for i in data['emp_details']:
    print(i)

# get the semantic search results by GPT-3

# write the corresponding "primitive" in to BPMN file.json


# Closing file
BPMN.close()

