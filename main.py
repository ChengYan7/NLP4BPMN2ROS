import numpy as np
import re
import openai
openai.api_key = "your API"                         # enter your API for GPT-3 here
import json

"""
We will try to integrate all the functions in this one function later
"""


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
    score = re.findall(r"(?<=\"score\": )\d+", string)      # extract number after "score"
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
    score = re.findall(r"(?<=\"score\": )\d+", string)      # extract number after "score"
    max_score = None
    for num in score:
        if max_score is None or num > max_score:
            max_score = num
    text = re.findall(r'\"score\": '+max_score+',\n\"text\": (.*?)}', search_response)      # extract the text
    return text







def main():
     # upload pre-defined files on openai (only once)

    # exact the text in BPMN

    # upload the text in BPMN as the query for searching

    # get the semantic search results by GPT-3

    # Determine the skill group function corresponding to the primitive and its input parameters

    # output the robot's ROS programming codes


if __name__ == "__main__":
    main()
