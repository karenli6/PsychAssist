import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
import string
import numpy as np
from nltk.corpus import stopwords

#cleaning the input
stop_words = stopwords.words('english')
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

def clean(array):
   stop_free = " ".join([i for i in array if i.lower() not in stop_words])
   punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
   normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
   return normalized.split(" ")

# returns a similarity score based on keywords and database description
def calc_similarity(keywords, description):
    sum = 0
    closest = []
    for word in keywords:
        max_similarity = 0
        closest_word = ''
        word_ss = wn.synsets(word)
        for i in description:
            i_ss = wn.synsets(i)
            for wss in word_ss:
                for iss in i_ss:
                    similarity = wss.path_similarity(iss)
                    # print('for', word, 'comparing', wss, 'and', iss, 'score:', similarity)
                    if similarity != None and similarity > max_similarity:
                            max_similarity = similarity
                            closest_word = iss
        # print(closest_word)
        closest.append(closest_word)
        sum += max_similarity
    
    
    # print(repr(closest))
    return sum/len(keywords)

# main
with open('disorders.txt', 'r+', encoding="utf-8") as f:
    line = f.readlines()
splitdescript = line[1].split()

# finding key words
# getting the user input
print("Hello! Welcome to PsychAssist.")
print("PsychAssist aids in diagnosing neurodevelopmental disorders. Please share with us all symptoms the patient is experiencing.")
print("Some questions to get you started: How does the patient feel on a general day? Have there been certain events that lead to a change in behaviour? Has the patient experienced any physical symptoms?")
user_paragraph = input("> ")

# turning input into smaller strings
all_words = user_paragraph.split()


if (calc_similarity(clean(all_words), clean(splitdescript)) >= 0.5):
    print("***It is likely the patient is experiencing a neurodevelopmental disorder.***")

    # go through specific disorders and prompt questions
    i = 0
    before=0
    beforeindex = 2;
    index = beforeindex;
    
    while i<6:
        # print("i is", i)
        bigname = line[index]
        # print(bigname)
        number = int(line[index][-2:-1])
        index+=1
        bigdescript = line[index]
        bigname = bigname[:-1]
        index +=1
        j=0
        
        while(j<number):
            # print("j is" , j)
            smallname = line[index]
            print(smallname, "\n")
            index+=1
            smalldes = line[index]
            print(smalldes, "\n")
            index+=1
            smallnumber=int(line[index])
            # print("NUMBERR ", smallnumber)
            index+=1
            if j%2 == 0:
                print("Alright,let\'s discuss", smallname)
            else:
                print("Let\'s discuss", smallname)
            #start criteria
            ask=0
            noes=0
            attention=False
            attentioncount=0
            tester = True
            value = 0
            
            while ask<smallnumber:
                #print(ask, "\n")
                if(line[index][0:1].isnumeric()==True):
                    value = int(line[index][0:1])
                    attention=True

                txt = input("Is the patient experiencing: "+line[index]+"> ")
                ask = ask+1
                index+=1
                if txt.lower() == "no":
                    noes+=1
                if txt.lower()=="no" and attention ==True:
                    attentioncount+=1
                if attention==False and noes >= smallnumber/2:
                    tester = False
                    break;
                if attention == True and attentioncount>value:
                    tester = False
                    attention = False
                    break;
                if attention == True and line[index][6:9] == "END":
                    attention = False
                    attentioncount=0
              
            index = index+(smallnumber-ask)    
            j=j+1
            if tester == False:
                print("***The patient does not have", smallname, "but we will keep checking for another", bigname + "***")
            else:
                print ("***The patient has", smallname, "***\n", "Here is the", smalldes, "\n", "This disorder is part of", bigname, "Here is the", bigdescript)
              
        i+=1

else:
    print("The patient most likely does not have a neurodevelopmental disorder.")
