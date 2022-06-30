from __future__ import unicode_literals
from django.shortcuts import render
from hazm import *
import convert_numbers
import re
import json
import os

path_txt_file ='txtfiles'
path_stopwords ='stop.txt'
list_txt=os.listdir(path_txt_file)

def stopwords_tokenize(path):
    f=open(path,'r')
    with open(path) as f:
        stopwords_file = f.read()
        stopwords = word_tokenize(stopwords_file)
    return stopwords

def words_lemmatizer(list_words):
    lemmatizer = Lemmatizer()
    lemmatizer_list = []
# for word,index in dic_words.items():
#   lemmatizer_wodrd=lemmatizer.lemmatize(word)
#   dic_words[lemmatizer_wodrd] = dic_words.pop(word)
    for word in list_words:
        lemmatizer_words=lemmatizer.lemmatize(word)
        lemmatizer_list.append(lemmatizer_words)
        # dic_words[lemmatizer_words] = dic_words.pop(word)
    return lemmatizer_list

def words_stopwords(stopwords_list,list_words):
    filtered_list=[]
    for word in list_words:
        if word not in stopwords_list:
            filtered_list.append(word)
    return filtered_list


def convert_number_p(txt_file):
  import re
  x=re.findall(r'(([۰-۹]+[،|٫]*)+)',txt_file)
  convert_dict ={
      "۰":"0",
      "۱":"1",
      "۲":"2",
      "۳":"3",
      "۴":"4",
      "۵":"5",
      "۶":"6",
      "۷":"7",
      "۸":"8",
      "۹":"9",
  }

  for i in range(len(x)):
    if '٫'in x[i][0]:
      s=x[i][0].replace('٫','')
    elif '،' in x[i][0]:
      s=x[i][0].replace('،','')
    else:
      s=x[i][0]
    txt_file = txt_file.replace(x[i][0],s)


  translation = txt_file.maketrans(convert_dict) 
  translation_num = txt_file.translate(translation)
  return translation_num

def files_words_indexing(sub_list_txt,path):
    dictionary={}
    # list_docID=[]
    stopwords = stopwords_tokenize(path_stopwords)
    for i in sub_list_txt:
        path_txt=os.path.join(path,i)
        f=open(path_txt,'r',encoding="utf-8", errors="ignore")
        with open(path_txt, encoding="utf-8", errors="ignore") as f:
            docID=int(i.replace(".txt",""))    
            contents = f.read()
            contents = convert_number_p(contents)
            # digit_find = contents.isdigit()
            # print(digit_find)
            words_tokenize_list = word_tokenize(contents)
            words_lemmatizer_list = words_lemmatizer(words_tokenize_list)
            words_stopwords_list = words_stopwords(stopwords,words_lemmatizer_list)

            # for j in range(len( words_stopwords_list)):
            #   dic[word_tokenize(contents)[j]]=docID
            for word in words_stopwords_list:
                if word not in dictionary:
                    dictionary[word]=[]
                    dictionary[word].append(docID)
                else:
                    if docID not in dictionary[word]:
                        dictionary[word].append(docID)
                dictionary[word].sort()
            # if word in dictionary:
            #   dictionary[word].append(docID)
    return dictionary

def serialize_index():
    dic=files_words_indexing(list_txt,path_txt_file)
    # print(dic)
    path_dict_file = 'invertrd_index.json'
    with open(path_dict_file, 'w') as outfile:
        json.dump(dic, outfile)

def create_document(document):
    docID = len(list_txt)
    docName = str(docID) + ".txt"
    path_txt = os.path.join(path_txt_file, docName)
    with open(path_txt, 'w',encoding="utf-8") as file:
        file.write(document)
    return docID

def update_inverted_index(document, docID, index_path):
    stopwords = stopwords_tokenize(path_stopwords)

    words_tokenize_list = word_tokenize(document)
    words_lemmatizer_list = words_lemmatizer(words_tokenize_list)
    words_stopwords_list = words_stopwords(stopwords,words_lemmatizer_list)
    print(words_stopwords_list)
    with open(index_path, 'r') as index_file:
        print("reading index...")
        dictionary = json.load(index_file)
    for word in words_stopwords_list:
        if word not in dictionary:
            print("adding new entry")
            dictionary[word]=[]
            dictionary[word].append(docID)
        else:
            print("updating existing entry")
            if docID not in dictionary[word]:
                dictionary[word].append(docID)
        dictionary[word].sort()
    with open(index_path, 'w') as outfile:
        json.dump(dictionary, outfile)
