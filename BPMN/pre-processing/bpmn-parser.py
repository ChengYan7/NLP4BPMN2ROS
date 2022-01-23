import os
import json 
from xml.dom import minidom
from xml.dom.minidom import Node
from BPMNdictionary import BPMNdict

#name of the file
filename = "UC3_inspection.bpmn"
filename1 ="UC2_sorting_freedrive_remake_v1.10.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"
filename = "UC3_inspection.bpmn"


#functions definitions 
def checkFile(filename):
    """
    Checks for file existence and readability
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
    """

    checkFile(xmlFile)
    retVal = minidom.parse(xmlFile).documentElement

    return retVal 

def replace(nreplace, str, key):
    '''
    Function to replace nth word (nreplace) in a string (str) with a given word (key)
    In our case the given word is the key from the BPMN_dictionary
    '''

    words=str.split(" ")
    words = " ".join([words[word_index] if word_index != nreplace else key for word_index in range(len(words))])
    return words

def dictionary(activitiesIDarr, BPMNdict):
    """
    Function to check if the robot activity array contains words that are the values of the dictionary,
    if yes, the given word is replaced by the generalised name of the activity i.e. the key of dictionary
    """
    control_var=0; 

    for k in activitiesIDarr:   
        words = k[0].split(' ')
        for p in sorted(BPMNdict):
            if any(word in k[0] for word in BPMNdict[p]):
                for single_dict_value in BPMNdict[p]:
                    if single_dict_value in words:
                        pos = words.index(single_dict_value)
                        str = replace(pos, k[0],p)
                        activitiesIDarr[control_var][0] = str
        control_var+=1
    return activitiesIDarr

    

#reads the XML file for the BPMN diagram specified in files.py
file = readXmlFile(filename1)
# ASK: file = readXmlFile(filename)

#definitions of tags to be extracted from the XML file
activities = file.getElementsByTagName('bpmn:serviceTask')
lane = file.getElementsByTagName('bpmn:lane')
objRef= file.getElementsByTagName('bpmn:dataObjectReference') #uses the id  attribute to find the tag and extract the name of element from it

activitiesIDarr = [] #names + ids
ObjectsArr = []


for i in lane:
    #print(i.attributes['name'].value, i.attributes['id'].value) #outputs list of lane actors and id of the actions
    if (i.attributes['name'].value.lower() == "robot"): #robot lane
        for j in activities:
            #print("activity " + j.attributes['name'].value + "  " + j.attributes['id'].value)
            activitiesIDarr.append([j.attributes['name'].value.lower(), j.attributes['id'].value])
        break


preprocessedAct = dictionary(activitiesIDarr, BPMNdict)

#looping through the array of ['activity_name', 'activity_ID' ]        
for i in preprocessedAct:
    print(i)  


#create output json file for the openAI
JSONdata ={}
JSONdata['activities'] = []
for i in preprocessedAct:
            JSONdata['activities'].append({
                'name': i[0], 
                'id':i[1]

                })

with open('..\\output\\BPMN_data.json', 'w') as outfile:
    json.dump(JSONdata, outfile)


for i in activities:
    for k in i.getElementsByTagName('bpmn:dataInputAssociation'):
        ObjectsArr.append(k.getElementsByTagName('bpmn:sourceRef')[0].firstChild.nodeValue)
        #the object array consists now of the data object references (from the sourceRef tag)

#using the data obj references and fetching them as id, we are searching for the corresponding names of the tools
for k in objRef:
    for p in ObjectsArr:
        if (k.attributes['id'].value==p):
            ObjectsArr.append([k.attributes['id'].value, k.attributes['name'].value.lower()])          

for i in ObjectsArr:
    print(i)