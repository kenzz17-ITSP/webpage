from django.shortcuts import render
from django.http import HttpResponse

import re
import string
import numpy as np
import pickle
import json
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import nltk
from  nltk.stem import SnowballStemmer
from tensorflow.keras.models import model_from_json
import h5py

# stop_words = stopwords.words("english")
stop_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'nor', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]
stemmer =  SnowballStemmer("english")

embedding_dim = 100
max_length = 100
trunc_type='post'
padding_type='post'
oov_tok = "<OOV>"

#preprocessing functions
def strip_links(text):
    link_regex    = re.compile('((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)', re.DOTALL)
    links         = re.findall(link_regex, text)
    for link in links:
        text = text.replace(link[0], ', ')    
    return text

def strip_all_entities(text):
    entity_prefixes = ['@','#']
    for separator in  string.punctuation:
        if separator not in entity_prefixes :
            text = text.replace(separator,' ')
    words = []
    for word in text.split():
        word = word.strip()
        if word:
            if word[0] not in entity_prefixes:
                words.append(word)
    return ' '.join(words)

def preprocess(line):
    line = line.lower()
    #stopwords removal
    for word in stop_words:
      token = " " + word + " "
      line = line.replace(token, " ")
      line = line.replace("  ", " ")
    #stemming   
    tokens = []
    for token in line.split():
      tokens.append(stemmer.stem(token))
    return " ".join(tokens)


# Load Tokenizer
tokenizer= Tokenizer(oov_token=oov_tok)
tokenizer = pickle.load(open("model/tokenizer.p", "rb"))
##word_index = pickle.load(open("/content/drive/My Drive/sentiment analysis/wordindex.p", "rb"))    #these two lines can be omitted, just kept here to see word word index
##vocab_size = len(word_index)

# Load Model
json_file = open('model/model.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
# load weights into new model
model.load_weights("model.h5")
print("Loaded model from disk")


# Create your views here.
def index(request):
    return render(request,'itsp1.html')

def feedback(request):
    return render(request, 'feedback.html')

def applications(request):
    return render(request, 'applications.html')

def predict(request):
    
    # Input
    # twt = ['i like the way you smile']
    
    sentence = request.GET.get('text',None)
    twt = sentence
    # Preprocess
    twt = strip_links(twt)    #optional
    twt = strip_all_entities(twt)  #optional (it removes @username #name)
    twt = preprocess(twt)
    # print(twt)
    list_form = []        # convert to ['input']
    list_form.append(twt)

    # Tokenize
    twt = tokenizer.texts_to_sequences(list_form)

    # Padding
    twt = padded = pad_sequences(twt, maxlen=max_length, padding = padding_type, truncating=trunc_type)
    print(twt)

    # Predict
    sentiment = model.predict(twt,batch_size=1,verbose = 2)[0]
    ans = np.around(sentiment)
    
    # print(sentiment)
    if ans ==1:
        ans = 'positive'
    else:
        ans = 'negative'
    context= {'sentence': sentence, 'sentiment':ans} 
    return render(request, 'itsp1.html', context)

def store_feedback(request):
    
    sentence = request.POST.get('text',None)
    predicted = request.POST.get('predicted', 'Positive')
    actual = request.POST.get('actual','Positive')

    other_feedback = request.POST.get('feedback',None)
    
    FILE_DIR = 'model/'

    data_file_loc = FILE_DIR + 'data_ext.txt'

    if sentence:
        with open(data_file_loc,'a+') as f:
            f.write(sentence + ':' + 'predicted:' + predicted + '/' + 'actual:'+ actual + '\n')

    feedback_file_loc = FILE_DIR + 'feedback.txt'

    if other_feedback:
        with open(feedback_file_loc,'a+') as feedback:
            feedback.write(other_feedback + '\n')

    return render(request,'feedback.html')
