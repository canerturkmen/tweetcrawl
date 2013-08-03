"""
Analysis for CSV data dumped out of mongodb
"""
import copy

import csv
import random
import re
import sys

# ['created_at', 'entities.hashtags', 'favorite_count', 'text', 'retweet_count', 'user.id', 'user.screen_name']



def revise_norm_1():
    with open('/Users/Caner/Desktop/norm.csv') as read:
        with open('/Users/Caner/Desktop/norm2.csv', 'wb') as out:
            reader = csv.reader(read, delimiter=',', quotechar='"')
            writer = csv.writer(out,delimiter=',', quoting=csv.QUOTE_MINIMAL )
            for r in reader:
                pass

def generate_norm_1():
    users = {}
    sw = []
    with open('/Users/Caner/Downloads/stop-words/stop-words-turkish.txt') as words:
        reader = csv.reader(words)
        for r in reader:
            sw.append(r[0])

    results = []
    vocab = {}

    print sw

    with open("/Users/Caner/Scrapes/tweet/tweets.csv") as file:
        with open('/Users/Caner/Desktop/norm_sample8.csv', 'wb') as out:
            reader = csv.reader(file, delimiter=",", quotechar='"')
            writer = csv.writer(out , delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for r in reader:
                if not users.get(r[5]):
                    users[r[5]] = []
                    users[r[5]].append(r[3])
                else:
                    users[r[5]].append(r[3])

            user_sample = random.sample(users.keys(), 1000)

            i = 0
            for key in user_sample:

                for a in users.get(key):
                    txt = re.sub(r'(http\S*)', '', a) # take out links
                    txt = re.sub("\n", " ", txt)
                    txt = re.sub("\t", " ", txt)
                    rex = re.compile(r'[,|.|!|\?| |;|\||\'|\"|\)|\(|:]')
                    wordlist = rex.split(txt)
                    wordlist2 = []
                    for w in wordlist:
                        if w not in sw and len(w) > 2 and w[0] != "@": # take out stopwords
                            wordlist2.append(w.lower())

                    for w in wordlist2:
                        a = [key, i, w]
                        results.append(a)
                        writer.writerow(a)

                i+=1

            total_vocab = {}
            for r in results:
                total_vocab[r[2]] = 0

            matrix = {}
            for r in results:
                if not matrix.get(r[0]):
                    matrix[r[0]] = copy.copy(total_vocab)
                matrix[r[0]][r[2]] = 1

            with open('/Users/Caner/Desktop/mx_out4.csv', 'wb') as outmatrix:
                matrixwriter = csv.writer(outmatrix, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for m in matrix:
                    row = []
                    for i in sorted(total_vocab.keys()):
                        row.append(matrix.get(m).get(i))
                    matrixwriter.writerow(row)







def learn_dates():
    """
    Get unique dates in the csv dump
    """
    ls = {}
    with open("/Users/Caner/Scrapes/tweet/tweets.csv") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for r in reader:
            # Mon Jul 22 19:59:01 +0000 2013
            ls[r[0][4:10]] = ""

    print ls.keys()

def get_unique_users():
    """
    Number of unique users who tweeted
    """
    ls = {}
    with open("/Users/Caner/Scrapes/tweet/tweets.csv") as file:
        reader = csv.reader(file, delimiter=",", quotechar='"')
        for r in reader:
            # Mon Jul 22 19:59:01 +0000 2013
            #ls[r[0][4:10]] = ""
            ls[r[0]] = ""

    print len(reader)

generate_norm_1()
print "Done"