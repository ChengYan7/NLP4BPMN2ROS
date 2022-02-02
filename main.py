import re
import openai
import json
from config import key 
from BPMN.BPMN_dict import BPMNdict
from BPMN.pre_functions import dictionary, readXmlFile, getActivities
from GPT3.NLP_functions import nlp_classification_results, corr_label 
from ROS.writeROS_function import substitute
"""
We will try to integrate all the functions in this one function later
"""

# initialization
openai.api_key = key  # enter your API for GPT-3 in the config file 


# name of the file - activate the file by switching to filename1
filename1 = "UC1_CS_Clip_Lightbarrier2LightbarrierHolder.bpmn"
filename1 ="UC1_CS_Clip_BasePlate2MotorAssembly2.bpmn" #works fine
filename1= "UC1_CS_Clip_Motor2MotorAssembly0.bpmn" #works fine
filename1 = "UC1_CS_Clip_MotorGear2MotorAssembly1.bpmn" #works fine
filename1="UC1_CS_PickAndPlace_Baseplate.bpmn" #works fine
filename1 = "UC1_CS_Clip_Lightbarrier2LightbarrierHolder.bpmn" #parsing ok, not ok - clip #only operator lane
filename = "UC1_CS_Clip_TransmissionGear2MotorHolder.bpmn" #not ok - clip 


def main():

    """
    1. exact the text in BPMN
    2. get the primitive command by GPT-3 classification
    3. output robot's programming code in ROS
    """
    # 1. exact the text in BPMN
    # reads the XML file for the BPMN diagram specified in files.py
    file = readXmlFile(filename1)

    # definitions of tags to be extracted from the XML file
    lane = file.getElementsByTagName('bpmn:lane')
    objRef = file.getElementsByTagName('bpmn:dataObjectReference')  # uses the id  attribute to find the tag and extract the name of element from it
    
    actRefArr = []

    actRefArr = getActivities(lane, actRefArr, file)
    for k in actRefArr:
        print(k)
    objNameIdPairs = {k.attributes['id'].value: k.attributes['name'].value.lower() for k in objRef}
    
    actObjFullArr = []
    for p in actRefArr:
        if p[2] in objNameIdPairs.keys():
            p[3] = objNameIdPairs[p[2]]
        actObjFullArr.append(p)

    preprocessedAct = dictionary(actObjFullArr, BPMNdict)

    # 2. get the primitive command by GPT-3 classification
    # create JSON object with the preprocessed data
    JSONdata = {}
    JSONdata['activities'] = []
    for i in preprocessedAct:

        try:
            # get each classification result by GPT-3
            classification_results = nlp_classification_results(i[1], "file-I2XzSpsdqtEDxe4sMOcH87UH")
            # get corresponding command as primitive
            primitive = corr_label(classification_results)
        except:
            primitive = "No corresponding primitive"

        JSONdata['activities'].append(
            {
            'act_id': i[0],
            'act_name': i[1],
            'obj_id': i[2],
            'obj_name': i[3].replace(" ", "_"),
            'primitive': primitive
            })

    # create a file (input to GPT-3)
    with open("Output\\" + filename1.replace('.bpmn', '.json'), 'w') as outfile:
        json.dump(JSONdata, outfile, indent=4)

    # 3. output robot's programming code in ROS
    input_file = "Output\\" +filename1.replace('.bpmn', '.json')

    my_file = open(input_file.replace('.json', '.py'), "w")
    f = open(input_file)
    data = json.load(f)

    # generate ROS script and save to a file in the output folder 
    for i in data['activities']:
        substitute(i['act_name'], i['act_id'], i['obj_name'], i['obj_id'], i['primitive'], my_file)


if __name__ == "__main__":
    main()
