﻿import numpy as np
import re
import openai

openai.api_key = "API"  # enter your API for GPT-3 here
import json


def nlp_search_results(query):
    """
    use GPT-3 model online-application to get the semantic search results

    :param query: the search content, such as: query = "grasp object"
    :return: search response of GPT-3
    """
    search_response = openai.Engine("davinci").search(
        search_model="davinci",
        query=query,
        max_rerank=1,  # number of documents
        documents=["Reach", "Move", "Insert/Remove", "Screw/Unscrew", "Stop", "Relocate", "Grasp", "Release", "Pick", \
                   "Return", "Calibrate", "Vision", "Follow", "Balance", "Record", "Teach", "Communicate", "Time Delay"],
    )
    # print(search_response)
    return search_response


def best_score(search_response):
    """
    output the best score in search response

    :param search_response: search result of GPT-3
    :return: the max score of content similarity
    """
    score = re.findall(r"(?<=\"score\": )\d+", search_response)  # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    # print('best score：', max_score)
    return max_score


def corr_text(search_response):
    """
    output the pre-defined content that correspond to the query in search response

    :param search_response: search result of GPT-3
    :return: the corresponding command text in pre-defined files
    """
    string = str(search_response)
    dict = eval(string)
    for i in dict["data"]:
        data_dict = i
    text_num = data_dict["document"]
    documents = ["Reach", "Move", "Insert/Remove", "Screw/Unscrew", "Stop", "Relocate", "Grasp", "Release", "Pick",
                 "Return", "Calibrate", "Vision", "Follow", "Balance", "Record", "Teach", "Communicate", "Time Delay"]
    text = documents[text_num]
    return text


def best_command(search_response):
    """
    output the pre-defined content that get the best score in search response(some problem)

    :param search_response: search result of GPT-3
    :return: the corresponding command text in pre-defined files
    """

    score = re.findall(r"(?<=\"score\": )\d+", search_response)  # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    text = re.findall(r'\"score\": ' + max_score + ',\n\"text\": (.*?)}', search_response)  # extract the text
    return text


# open BPMN file.json
BPMN = open('..\BPMNfile.json', )

# returns JSON object as a dictionary
data = json.load(BPMN)

# get all action names
for i in data["activities"]:
    # get each search result by GPT-3
    search_response = nlp_search_results(i['act_name'])
    # get corresponding command as primitive
    dict = i
    dict["primitive"] = corr_text(search_response)

    # write the corresponding "primitive" in to BPMN file.json
    # json.dump(dict)

    # print user's input sentence
    print(i["act_name"])
    # print primitive
    print(dict["primitive"])

# Closing file
BPMN.close()
