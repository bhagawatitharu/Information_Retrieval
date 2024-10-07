# -*- coding: utf-8 -*-
"""Untitled11.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1OPANl9PFL9AcnmHtAfURK6QLftfmk3xA
"""

import os
import re
import string
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Load documents
def load_documents(folder_path):
    documents = {}
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
            documents[filename] = file.read()
    return documents

# Preprocessing: Tokenization, stopword removal, and stemming
def preprocess(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Tokenize
    tokens = text.split()
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(word) for word in tokens]
    return ' '.join(tokens)

# Folder containing the stories
folder_path = '/content/1'

# Load and preprocess documents
documents = load_documents(folder_path)
preprocessed_docs = {doc: preprocess(text) for doc, text in documents.items()}
preprocessed_docs

# Using TF-IDF Vectorizer to create the document-term matrix
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(preprocessed_docs.values())

# Document-term matrix
feature_names = vectorizer.get_feature_names_out()
print(f"TF-IDF Matrix Shape: {tfidf_matrix.shape}")

from sklearn.metrics.pairwise import cosine_similarity

def process_query(query):
    # Preprocess the query similar to the documents
    query = preprocess(query)
    # Transform query using the same vectorizer
    query_vec = vectorizer.transform([query])
    return query_vec

def retrieve_documents(query, top_n=5):
    query_vec = process_query(query)
    # Compute cosine similarity between query and all documents
    cosine_sim = cosine_similarity(query_vec, tfidf_matrix).flatten()
    # Get the top N results
    top_indices = cosine_sim.argsort()[-top_n:][::-1]
    top_docs = [(list(preprocessed_docs.keys())[index], cosine_sim[index]) for index in top_indices]
    return top_docs

# Test the retrieval system
query = "example search terms"
top_results = retrieve_documents(query)

print("Top Results:")
for doc, score in top_results:
    print(f"{doc}: {score}")

# Query1
query = "adventure story"
top_results = retrieve_documents(query)

print("Top Results:")
for doc, score in top_results:
    print(f"{doc}: {score}")

# Query2
query = "hard work"
top_results = retrieve_documents(query)

print("Top Results:")
for doc, score in top_results:
    print(f"{doc}: {score}")

