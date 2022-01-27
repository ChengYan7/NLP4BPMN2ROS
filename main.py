import numpy as np
import re
import openai
import json
import os
from xml.dom import minidom

"""
We will try to integrate all the functions in this one function later
"""

# initialization
openai.api_key = "your API"                         # enter your API for GPT-3 here

# name of the file - activate the file by switching to filename1
filename = "UC3_inspection.bpmn"
filename ="UC2_sorting_freedrive_remake_v1.10.bpmn"
filename1 = "bpmnExamplewith3bubbles.bpmn"

# parameter definition
BPMNdict={
    "grasp":{"clasp", "clench", "clutch", "clutches", "grasp", "grip", "hold", "cling"},
    "reach":{"attain","reach", "arrive at", "gain", "hit", "achieve"},
    "move111111":{"move", "displace"},
    "insert":{"insert", "enclose", "put in", "put_in", "introduce","fit", "stick in"},
    "remove":{"remove", "take away", "get rid of", "transfer"},
    "stop":{"halt", "stop", "discontinue", "break off", "break", "finish", "terminate", "end"},
    "screw":{"screw", "drive in"},
    "unscrew":{"unscrew", "loosen"},
    "relocate":{"relocate", "reposition", "change positionre"},
    "release":{"release", "relinquish", "let go", "let go of"},
    "pick":{"pick up", "pick", "select", "take"},
    "return":{"return", "put back"},
    "calibrate":{"calibrate", "measure", "fine-tune", "graduate"},
    "vision":{"recognize"},
    "follow":{"mirror","follow", "observe", "watch over"},
    "record":{"register", "record"},
    "balance":{"balance", "equilibrate", "equilibrise", "equilibrize"},
    "teach":{"teach", "learn", "instruct", "demonstrate"},
    "communicate":{"information exchange", "pass on", "pass", "pass along", "put across", "transmit", "convey"},
    "time delay":{"wait", "hold", "delay", "time lag", "lag" },
    "tool":{"tool", "object", "element"},
    "movement":{"movement", "motion"},
    "position":{"position", "place","location"}
 }

# functions definitions
def checkFile(filename):
    """
    Checks for file existence and readability of the file
    Open the file for reading

    Args:
    filename: bpmn input file

    Returns:
    no return
    """

    valid = True

    if filename is None or not os.path.isfile(filename):
        valid = False

    if valid:
        try:
            with open(filename, "rb"):
                pass
        except:
            valid = False

    if not valid:
        raise Exception("unable to read file '%s'" % filename)


def readXmlFile(xmlFile):
    """
    Reads XML file content and returns its DOM representation

    Args:
    xmlFile: xml file to be preprocessed

    Returns:
    retVal: parent tag (DOM element) from the xml file e.g. <DOM Element: bpmn:definitions at 0x2ca08bbbd00>
    """

    checkFile(xmlFile)
    retVal = minidom.parse(xmlFile).documentElement
    return retVal


def replace(nreplace, str, key):
    '''
    Function to replace nth word (nreplace) in a string (str) with a given word (key)
    In our case the given word is the key from the BPMN_dictionary

    Args:
    nreplace: word to be replaced
    str: string in which the word has to be returned
    key: key from BPMN dictionary that replaces the nth word

    Returns:
    words: updated(pre-processed) string
    '''

    words = str.split(" ")
    words = " ".join([words[word_index] if word_index != nreplace else key for word_index in range(len(words))])
    return words


def dictionary(inputArr, dictionary, nreplace=1):
    """
    Function to check if the robot activity array contains words that are the values of the dictionary,
    if yes, the given word is replaced by the generalised name of the activity i.e. the key of dictionary

    Args:
    inputArr: array with act_id, act_name, obj_name, obj_id before preprocessing
    dictionary: JSON dictionary, keys are used to replace the given word
    nreplace: nth element in the row of inputArr to be pre-processed, by default it's act_name

    Returns:
    inputArr: array after preprocessing
    """
    control_var = 0

    for k in inputArr:
        words = k[nreplace].split(' ')
        for p in sorted(dictionary):
            if any(word in k[nreplace] for word in dictionary[p]):
                for single_dict_value in dictionary[p]:
                    if single_dict_value in words:
                        pos = words.index(single_dict_value)
                        str = replace(pos, k[nreplace], p)
                        inputArr[control_var][nreplace] = str
        control_var += 1
    return inputArr


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


def substitute(act_name, act_id, obj_name, obj_id, primitive, my_file):
    if (obj_name == "2 finger gripper"):
        finger_gripper = True;
        act_module = False;
    elif (obj_name == "vacuum gripper"):
        finger_gripper = False;
        act_module = True;
    else:
        # default values
        finger_gripper = False;
        act_module = False;

        # MOVE/REACH with screw object
    if ((primitive == "move" or primitive == "reach") and obj_name == "screw"):
        print("move/reach + screw")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":
    rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.") #useful info for the debugger
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x={obj_name}.x, 
        position_y={obj_name}.y, 
        position_z={obj_name}.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID {act_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")        
        """)

        # GRASP
        # If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
        # if it is something else the parameter to be changed is "activatemodule"
    if (primitive == "grasp"):
        print("grasp")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":  
        rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.")
        # Here goes the action calling for the precise task definition
        gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp={finger_gripper}, speed=20, force=1, distance=40, activatemodule={act_module}, modulestrenght=255)
        Activity_name = taskDefinition["object"][-16:]
        Activity = activity(Activity_name)
        # Sends the goal to the action server.
        self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
            done_cb = Activity._resultCB)
        self.activeActivity = Activity
        rospy.loginfo("Task {act_name} with the ID {act_id} has been executed.")
        taskStatus["value"] = "inProgress"
        taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        """)

        # UNGRASP
        # If the object connected is a 2 finger gripper the parameter to be changes is "grasp"
        # if it is something else the parameter to be changed is "activatemodule"
    if (primitive == "ungrasp"):
        print("ungrasp")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":  
    rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.")
    # Here goes the action calling for the precise task definition
    gripperGraspGoal = fmp_gripper_action.msg.gripperGoal(grasp={finger_gripper}, speed=20, force=1, distance=40, activatemodule={act_module}, modulestrenght=255)
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.gripperActuation.send_goal(gripperGraspGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID: {act_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
            """)

        # MOVE/REACH with nut object
    if ((primitive == "move" or primitive == "reach") and obj_name == "nut"):
        print("move/reach + nut")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":
    rospy.loginfo("Task {act_name} with the ID: {act_id} and nut object: {obj_id} in progress.")
    # Here goes the action calling for the precise task definition
    moveTrajGoal = fmp_move_traj.msg.ExecuteMotionPlannerGoal(execute_motion = True, change_planner = True, planner = "fmpur10withgripper_s",
        position_x={obj_name}.x, 
        position_y={obj_name}.y, 
        position_z={obj_name}.z,
        change_orientation= False)  
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.moveTrajClient.send_goal(moveTrajGoal, feedback_cb = Activity._feedbackCB, 
        done_cb = Activity._resultCB)
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID: {act_id} and nut object: {obj_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
                """)

    if (primitive != "move" and primitive != "reach" and primitive != "grasp" and primitive != "ungrasp"):
        print("none of above 4")
        my_file.write(f"""
if taskDefinition["object"] == "urn:ngsi-ld:TaskDefinition:siemens:Activity{act_id}":  
    rospy.loginfo("Task {act_name} with the ID: {act_id} in progress.")
    # Here goes the action calling for the precise task definition
    Activity_name = taskDefinition["object"][-16:]
    Activity = activity(Activity_name)
    # Sends the goal to the action server.
    self.activeActivity = Activity
    rospy.loginfo("Task {act_name} with the ID {act_id} has been executed.")
    taskStatus["value"] = "inProgress"
    taskStatus["observedAt"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ") 
    """)



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
    activities = file.getElementsByTagName('bpmn:serviceTask')
    lane = file.getElementsByTagName('bpmn:lane')
    objRef = file.getElementsByTagName(
        'bpmn:dataObjectReference')  # uses the id  attribute to find the tag and extract the name of element from it

    actRefArr = []
    actObjArr = []

    for i in lane:
        if (i.attributes['name'].value.lower() == "robot"):  # robot lane
            if activities:
                for activity in activities:
                    association = activity.getElementsByTagName("bpmn:dataInputAssociation")
                    if association:
                        for sourceRef in association:
                            actRefArr.append(
                                [activity.attributes['id'].value.lower(), activity.attributes['name'].value.lower(),
                                 sourceRef.getElementsByTagName("bpmn:sourceRef")[0].firstChild.nodeValue,
                                 'obj_placeholder'])
                    else:
                        actRefArr.append(
                            [activity.attributes['id'].value.lower(), activity.attributes['name'].value.lower(), 'None',
                             'None'])

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
        JSONdata['activities'].append({
            'act_id': i[0],
            'act_name': i[1],
            'obj_id': i[2],
            'obj_name': i[3]})
        # get each classification result by GPT-3
        classification_results = nlp_classification_results(i[1], "file-I2XzSpsdqtEDxe4sMOcH87UH")
        # get corresponding command as primitive
        primitive = corr_label(classification_results)
        JSONdata['activities'].append({
            'primitive': primitive})

    # create a file (input to GPT-3)
    with open(filename1.replace('.bpmn', '.json'), 'w') as outfile:
        json.dump(JSONdata, outfile, indent=4)

    # 3. output robot's programming code in ROS
    input_file = filename1.replace('.bpmn', '.json')

    my_file = open(input_file.replace('.json', '.py'), "w")
    f = open(input_file)
    data = json.load(f)

    for i in data['activities']:
        substitute(i['act_name'], i['act_id'], i['obj_name'], i['obj_id'], i['primitive'], my_file)
        #substitute(act_name, act_id, obj_name, obj_id, primitive):


    # my_file = open("ROSready.py")
    # content = my_file.read()
    # my_file.close()



if __name__ == "__main__":
    main()
