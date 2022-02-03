from xml.dom import minidom
import os
import re

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
        raise Exception(f"unable to read file {filename}")


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

def checkLanes(lane):
    """
    Function to check the actors of all the lanes

    Args:
    lane - Tag Name of the xml tree element to check

    Output: 
    arr - arr with actors' names
    
    """
    arr = []
    for k in lane:
        arr.append(k.attributes['name'].value.lower()) 
    return arr


def getActivities(lane, actRefArr, file):
    """
    Function to control the flow of information extraction from BPMN, 3 possible scenarios:
    1. Robot lane exists and contains activities 
    2. Robot lane exists and is empty in such case we check for the operator lane:
        2.1 Operator lane exists and the extraction of information will focus on the operator lane
        2.2 Operator lane exists and no information --> raise Exception
    3. Robot lane doesn't exist --> raise Exception
        3.1 Operator lane exists and the extraction of information will focus on the operator lane
        3.2 Operator lane exists and no information --> raise Exception
        
    Inputs:
    - lane: xml element from which the items are extracted
    - actRefArr - empty array to store information on act and references
    - file - input file to parse

    Returns:
    - actRefArr - filled array with activity data, object reference (id) and placeholder for obj_name
    """
    
    lanesArr = checkLanes(lane)
    if "robot" in lanesArr:
       activities = file.getElementsByTagName('bpmn:serviceTask')
       if not activities: #if the robot lane is empty 
           if "operator" in lanesArr: #check the operator lane
               activities = file.getElementsByTagName('bpmn:userTask')
               if not activities:
                   raise Exception("Both robot and operator lane are empty, exiting the program.")
    elif ("operator" not in lanesArr and "robot" not in lanesArr):
        raise Exception("Both robot and operator lane do not exist, exiting the program.")

    for i in lane:
        if (i.attributes['name'].value.lower() == "robot"):  # robot lane
            for activity in activities:
                association = activity.getElementsByTagName("bpmn:dataInputAssociation")
                if association:
                    
                    for sourceRef in association:
                        
                        #add spacing between uppercase words if no spacing provided
                        activity_modified =re.sub(r'(?P<end>[a-z])(?P<start>[A-Z])', '\g<end> \g<start>', 
                        activity.attributes['name'].value)
                        
                        #create array containing act_id, act_name, obj_id and placeholder for obj_name
                        actRefArr.append(
                            [activity.attributes['id'].value.lower(), activity_modified.lower(),
                            sourceRef.getElementsByTagName("bpmn:sourceRef")[0].firstChild.nodeValue,
                            'obj_placeholder']) 
                else:
                    
                    actRefArr.append(
                        [activity.attributes['id'].value.lower(), activity.attributes['name'].value.lower(), 'None',
                        'None'])
    if actRefArr:
        print("Activities array - success")                    
    return actRefArr
