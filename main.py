import numpy as np
import openai
openai.api_key = "your API"                         # enter your API for GPT-3 here


# nlp_search_results: use GPT-3 model online-application to get the semantic search results
def nlp_search_results(query, file_ID):                      # input must be as the format "input"
    search_response = openai.Engine("davinci").search(
        search_model="davinci",
        query=query,                                # such as: query="grasp object"
        max_rerank=5,                               # number of documents
        file=file_ID                                # your pre-defined file library "file-aVmfougPtrAX3RA40qSufHqQ"
    )
    # print(search_response)
    return search_response


# best_score: output the pre-defined content that get the best score in search response
def best_score(search_response):

    return


#


def main():
     # upload pre-defined files on openai (only once)

    # exact the text in BPMN

    # upload the text in BPMN as the query for searching

    # get the semantic search results by GPT-3

    # Determine the skill group function corresponding to the primitive and its input parameters

    # output the robot's ROS programming codes


if __name__ == "__main__":
    main()
