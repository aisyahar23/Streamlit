import pandas as pd
import numpy as np
import json
import nltk
from nltk.stem import snowball
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.tree import DecisionTreeClassifier
import random
from datetime import datetime

intent_list = []
train_data = []
train_label = []
responses = {}
list_of_words = []

nltk.download('punkt_tab')
snowballStemmer = snowball.SnowballStemmer("english")

def text_preprocessing(sentence):
    # tokenize the sentences
    tokens = nltk.word_tokenize(sentence)
    # check the word is alphabet or number
    for token in tokens:
        if not token.isalnum():
            tokens.remove(token)
    stem_tokens = []
    for token in tokens:
        stem_tokens.append(snowballStemmer.stem(token.lower()))
    return " ".join(stem_tokens)

# Feature Extraction
vectorizer = CountVectorizer()

# Build NLP Model
from sklearn.naive_bayes import MultinomialNB

clf_nb = MultinomialNB()
clf_dt = DecisionTreeClassifier(random_state=33)

def bot_respond(user_query):  # what user say
    user_query = text_preprocessing(user_query)
    user_query_bow = vectorizer.transform([user_query])
    clf = clf_dt
    predicted = clf.predict(user_query_bow)  # predict the intents
    # When model don't know the intent
    max_proba = max(clf.predict_proba(user_query_bow)[0])
    if max_proba < 0.08 and clf == clf_nb:
        predicted = ['noanswer']
    elif max_proba < 0.3 and not clf == clf_nb:
        predicted = ['noanswer']
    bot_response = ""
    numOfResponses = len(responses[predicted[0]])
    chosenResponse = random.randint(0, numOfResponses-1)
    if predicted[0] == "TimeQuery":
        bot_response = eval(responses[predicted[0]][chosenResponse])
    else:
        bot_response = responses[predicted[0]][chosenResponse]
    return bot_response

def load_model():
    # import training data
    with open("intents.json") as f:
        data = json.load(f)

    # load training data
    for intent in data['intents']:
        for text in intent['text']:
            # Save the data sentences
            preprocessed_text = text_preprocessing(text)
            train_data.append(preprocessed_text)
            # Save the data intent
            train_label.append(intent['intent'])
        intent_list.append(intent['intent'])
        responses[intent['intent']] = intent["responses"]

    # Feature Extraction
    vectorizer.fit(train_data)
    list_of_words = vectorizer.get_feature_names_out()
    train_data_bow = vectorizer.transform(train_data)

    # Train the model
    clf_dt.fit(train_data_bow, train_label)
