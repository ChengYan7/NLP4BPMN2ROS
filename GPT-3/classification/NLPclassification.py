import numpy as np
import re
import openai
openai.api_key = "API"      # enter your API for GPT-3 here
import json


def nlp_classification_results(query, file_ID):
    """
    use GPT-3 model online-application "classification" to get the semantic search results

    :param query: the search content, such as: query = "grasp object"
    :param file_ID: pre-uploaded labeled examples
    :return: classification response of GPT-3
    """
    classification_response = openai.Classification.create(
        file=file_ID,
        query=query,
        search_model = "ada",
        model="curie",
        max_examples=1,                                   # number of documents

    )
    # print(classification_response)
    return classification_response


def best_score(classification_response):
    """
    output the best score in search response

    :param classification_response: classification result of GPT-3
    :return: the max score of content similarity
    """
    score = re.findall(r"(?<=\"score\": )\d+", classification_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    # print('best score：', max_score)
    return max_score


def corr_label(classification_response):
    """
    output the pre-defined content that correspond to the query in search response

    :param classification_response: search result of GPT-3
    :return: the corresponding command label as primitive
    """
    string = str(classification_response)
    dict = eval(string)
    for i in dict["selected_examples"]:
        data_dict = i
    label = data_dict["label"]
    return label


def best_command(classification_response):
    """
    output the pre-defined content that get the best score in search response(some problem)

    :param classification_response: search result of GPT-3
    :return: the corresponding command text in pre-defined files
    """

    score = re.findall(r"(?<=\"score\": )\d+", classification_response)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    text = re.findall(r'\"score\": '+max_score+',\n\"text\": (.*?)}', classification_response)      # extract the text
    return text


# open BPMN file.json
BPMN = open("..\BPMNfile.json", )

# returns JSON object as a dictionary
data = json.load(BPMN)

# get all action names
for i in data["activities"]:
    # get each search result by GPT-3
    classification_results = nlp_classification_results(i['act_name'], "file-C0qj8kQWTheFwcZvUbIQ0UKJ")
    # get corresponding command as primitive
    dict = i
    dict["primitive"] = corr_label(classification_results)

    # write the corresponding "primitive" in to BPMN file.json
    # json.dump(dict)

    # print user's input sentence
    print(i["act_name"])
    # print primitive
    print(dict["primitive"])

# Closing file
BPMN.close()

