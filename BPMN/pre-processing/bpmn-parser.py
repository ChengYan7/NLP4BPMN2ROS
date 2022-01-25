import os
import json 
from xml.dom import minidom
from xml.dom.minidom import Node
from BPMNdictionary import BPMNdict

#name of the file - activate the file by switching to filename1
filename = "UC3_inspection.bpmn"
filename ="UC2_sorting_freedrive_remake_v1.10.bpmn"
filename1 = "bpmnExamplewith3bubbles.bpmn"

#functions definitions 
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
        raise SqlmapSystemException("unable to read file '%s'" % filename)

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

    words=str.split(" ")
    words = " ".join([words[word_index] if word_index != nreplace else key for word_index in range(len(words))])
    return words

def dictionary(inputArr, dictionary, nreplace = 1):
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
    control_var=0; 

    for k in inputArr:   
        words = k[nreplace].split(' ')
        for p in sorted(dictionary):
            if any(word in k[nreplace] for word in dictionary[p]):
                for single_dict_value in dictionary[p]:
                    if single_dict_value in words:
                        pos = words.index(single_dict_value)
                        str = replace(pos, k[nreplace],p)
                        inputArr[control_var][nreplace] = str
        control_var+=1
    return inputArr

    

#reads the XML file for the BPMN diagram specified in files.py
file = readXmlFile(filename1)

#definitions of tags to be extracted from the XML file
activities = file.getElementsByTagName('bpmn:task')
lane = file.getElementsByTagName('bpmn:lane')
objRef= file.getElementsByTagName('bpmn:dataObjectReference') #uses the id  attribute to find the tag and extract the name of element from it

actRefArr = []
actObjArr = []

for i in lane:
    if (i.attributes['name'].value.lower() == "robot"): #robot lane
        if activities: 
            for activity in activities:
                association = activity.getElementsByTagName("bpmn:dataInputAssociation")
                if association:
                    for sourceRef in association:
                        actRefArr.append([activity.attributes['id'].value.lower(), activity.attributes['name'].value.lower(), sourceRef.getElementsByTagName("bpmn:sourceRef")[0].firstChild.nodeValue, 'obj_placeholder'])
                else:
                    actRefArr.append([activity.attributes['id'].value.lower(), activity.attributes['name'].value.lower(), 'None', 'None'])



objNameIdPairs = { k.attributes['id'].value : k.attributes['name'].value.lower() for k in objRef}
actObjFullArr = []
for p in actRefArr:
    if p[2] in objNameIdPairs.keys():
        p[3] = objNameIdPairs[p[2]]
    actObjFullArr.append(p)

preprocessedAct = dictionary(actObjFullArr, BPMNdict)

# create JSON object with the preprocessed data 
JSONdata ={}
JSONdata['activities'] = []
for i in preprocessedAct:
            JSONdata['activities'].append({
                'act_id': i[0], 
                'act_name':i[1],
                'obj_id':i[2], 
                'obj_name':i[3]
                })

#create a file (input to GPT-3)
with open(filename1.replace('.bpmn', '.json'), 'w') as outfile:
    json.dump(JSONdata, outfile, indent = 4)
