import os
import json 
from xml.dom import minidom
from xml.dom.minidom import Node
from BPMNdictionary import BPMNdict
from files import file_name


"""
TODO:
enhance the extraction from BPMN diagram i.e. tools
ASK: how it should be activities and tools together? 
files to be specified in BPMN_files
create the ROS parser
multiple activities using the same tool, get only distinct?
"""



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
    Functions to replace nth word (nreplace) in a string (str) with a given word (key)
    In our case the given word is the key from the BPMN_dictionary
    '''

    words=str.split(" ")
    words = " ".join([words[word_index] if word_index != nreplace else key for word_index in range(len(words))])
    return words

def dictionary(activitiesIDarr, BPMNdict):
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

#parrent tag - node:
flowNodes= file.getElementsByTagName('bpmn:flowNodeRef')

#initialize array consisting of activities (name+id)
activitiesIDarr = []
#print attributes name i.e. in this case the executables in the flow written by a human
for i in lane:
    #print(i.attributes['name'].value, i.attributes['id'].value) #outputs list of lane actors and id of the actions
    if (i.attributes['name'].value.lower() == "robot"): #robot lane
        for j in activities:
            #print("activity " + j.attributes['name'].value + "  " + j.attributes['id'].value)
            activitiesIDarr.append([j.attributes['name'].value.lower(), j.attributes['id'].value])
        break

# dictionary implementation
preprocessedAct = dictionary(activitiesIDarr, BPMNdict)

#looping through the array of ['activity_name', 'activity_ID' ]        
for i in preprocessedAct:
    print(i)  


##################################
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
##################################


#extraction of elements/objects
activities = file.getElementsByTagName('bpmn:serviceTask')
objRef= file.getElementsByTagName('bpmn:dataObjectReference') #by id ---> extract name

ObjectsArr = []

for i in activities:
    for k in i.getElementsByTagName('bpmn:dataInputAssociation'):
        ObjectsArr.append(k.getElementsByTagName('bpmn:sourceRef')[0].firstChild.nodeValue)

for k in objRef:
    for p in ObjectsArr:
        if (k.attributes['id'].value==p):
            ObjectsArr.append([k.attributes['id'].value, k.attributes['name'].value.lower()])          




