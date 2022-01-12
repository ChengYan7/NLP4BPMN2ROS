from BPMNdictionary import BPMNdict

str = "your name is clasp"
words = str.split(' ')
print(words)

def replace(nreplace, str, key):
    nreplace=pos
    words=str.split(" ")
    words = " ".join([words[word_index] if word_index != nreplace else key for word_index in range(len(words))])
    return words


for p in sorted(BPMNdict):
    #print(BPMNdict[p],'returns ->', p)
    if any(word in str for word in BPMNdict[p]):
        for single_dict_value in BPMNdict[p]:
            if single_dict_value in words:
                pos = words.index(single_dict_value)
                str = replace(pos, str,p)
                print("hehehe" + str)
        




"""
a_set = {0, 1, 2}
list_of_strings = [str(s) for s in a_set]
joined_string = " ". join(list_of_strings)
print(joined_string)
"""
