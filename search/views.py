from __future__ import unicode_literals
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from hazm import *
import json
from pathlib import Path
from invertedIndex.views import words_lemmatizer, serialize_index, create_document, update_inverted_index

path_dict_file = 'invertrd_index.json'

def searchingSingleWord(input_list,dic):
  input_word = input_list[0]
  print(input_word)
  if input_word in dic.keys():
    return dic[input_word]
  else:
    return "not found"

def searchingAnd(input_list,dic):
  input_list.remove('و')
  word_1 = input_list[0]
  word_2 = input_list[1]
  result_list = []
  counter_post_list_1 = 0
  counter_post_list_2 = 0

  if word_1 in dic.keys():
    posting_list_1 = dic[word_1]
  if word_2 in dic.keys():
    posting_list_2 = dic[word_2]
  
  len_posting_list_1 = len(posting_list_1)
  len_posting_list_2 = len(posting_list_2)

  while counter_post_list_1 < len_posting_list_1 and counter_post_list_2 < len_posting_list_2:
    if posting_list_1[counter_post_list_1] == posting_list_2[counter_post_list_2]:
      result_list.append(posting_list_1[counter_post_list_1])
      counter_post_list_1 +=1
      counter_post_list_2 +=1
    elif posting_list_1[counter_post_list_1] > posting_list_2[counter_post_list_2]:
      counter_post_list_2 +=1
    else:
      counter_post_list_1 +=1

  return result_list

def searchingOr(input_list,dic):
  input_list.remove('یا')
  word_1 = input_list[0]
  word_2 = input_list[1]
  result_list = []
  counter_post_list_1 = 0
  counter_post_list_2 = 0

  if word_1 in dic.keys():
    posting_list_1 = dic[word_1]
  if word_2 in dic.keys():
    posting_list_2 = dic[word_2]
  
  len_posting_list_1 = len(posting_list_1)
  len_posting_list_2 = len(posting_list_2)

  while counter_post_list_1 < len_posting_list_1 and counter_post_list_2 < len_posting_list_2:
    if posting_list_1[counter_post_list_1] > posting_list_2[counter_post_list_2]:
      result_list.append(posting_list_2[counter_post_list_2])
      counter_post_list_2 +=1
    elif posting_list_1[counter_post_list_1] < posting_list_2[counter_post_list_2]:
      result_list.append(posting_list_1[counter_post_list_1])
      counter_post_list_1 +=1
    elif posting_list_1[counter_post_list_1] == posting_list_2[counter_post_list_2]:
      result_list.append(posting_list_1[counter_post_list_1])
      counter_post_list_1 +=1
      counter_post_list_2 +=1

  while counter_post_list_1 < len_posting_list_1:
    result_list.append(posting_list_1[counter_post_list_1])
    counter_post_list_1 +=1

  while counter_post_list_2 < len_posting_list_2:
    result_list.append(posting_list_2[counter_post_list_2])
    counter_post_list_2 +=1

  return result_list

def searching (input_word,dic):
  words_tokenize_list = word_tokenize(input_word)
  words_lemmatizer_list = words_lemmatizer(words_tokenize_list)
  #word1 and word2
  if 'و' in words_lemmatizer_list:
    word_and_word =  searchingAnd(words_lemmatizer_list,dic)
    return word_and_word
  #word1 or word2
  elif 'یا' in words_lemmatizer_list:
    word_or_word = searchingOr(words_lemmatizer_list,dic)
    return word_or_word
  #single word
  else:
    single_word = searchingSingleWord(words_lemmatizer_list,dic)
    return single_word

def search(request):
    input = request.POST.get('query')
    path = Path(path_dict_file)
    if not(path.is_file()):
      print ("generating index...")
      serialize_index()
    with open(path_dict_file, 'r') as index_file:
        print("reading index...")
        dic = json.load(index_file)
    x = searching(input, dic)
    return JsonResponse(x, safe=False)

def add(request):
  document = request.POST.get('document')
  print(document)
  docID = create_document(document)
  update_inverted_index(document, docID, path_dict_file)
  return HttpResponse(document)

def index(request):
  return render(request, 'index.html')