from xml.dom import minidom
import os

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
