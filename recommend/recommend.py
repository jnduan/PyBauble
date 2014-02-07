#!/usr/bin/env python
import sys
import re
import codecs
import math

from operator import itemgetter 

DATA_PATH = "."
TRAIN_FILE = DATA_PATH + "/trainingset.csv"
TEST_FILE = DATA_PATH + "/test1.csv"
VALIDATE_FILE1 = DATA_PATH + "/validation1.csv"
VALIDATE_FILE2 = DATA_PATH + "/validation2.csv"

def read_csv(path, cols = [], primary=0):
    data = {}
    try: 
        f = codecs.open(path, 'r', 'utf-16')
        lines = f.readlines()
    except UnicodeError, e:
        f = codecs.open(path, 'r', 'utf-8')
        lines = f.readlines()
    
    for line in lines:
        items = line.split("\t")
        data.setdefault(items[primary],set([]))
        #print pair[0], pair[1], type(pair[0]), type(items[pair[0]])
        if cols: 
            data[items[primary]].update([items[i] for i in cols])
        else:
            data[items[primary]].update(items)
    return data


class Recommender(object):
    
    def __init__(self):
        self.weight = {}

    def train(self, data):
        pass

    def recommend(self, id, topN):
        pass 

    def precision(self, test_data, vali_data):
        hit = 0
        total = 0
        for id, items in test_data.items():
            result_items = self.recommend(items, 9)
            vali_items = vali_data[id] if vali_data.has_key(id) else set([])
            for item, weight in result_items:
                if item in vali_items:
                    hit += 1
            total += 9
        return hit / (1.0 * total)

    def recall(self, test_data, vali_data):
        hit = 0
        total = 0
        for id, items in test_data.items():
            result_items = self.recommend(items, 9)
            vali_items = vali_data[id] if vali_data.has_key(id) else set([])
            for item, weight in result_items:
                if item in vali_items:
                    hit += 1
            total += len(vali_items)
        return hit / (1.0 * total) 

    def coverage(self, train_data, test_data):
        recommend_items = set()
        all_items = set()
        for id, items in train_data.items():
            all_items.update(items)
        for id, items in test_data.items():
            result_items = self.recommend(items, 9)
            for item, weight in result_items:
                recommend_items.add(item)
        return len(recommend_items) / (len(all_items) * 1.0)

    def popularity(self, train_data, test_data):
        item_popularity = {}
        popularity = 0
        n = 0
        for id, items in train_data.items():
            for item in items:
                item_popularity.setdefault(item, 0)
                item_popularity[item] += 1
        for id, items in test_data.items():
            result_items = self.recommend(items, 9)
            for item, weight in result_items:
                popularity += math.log(1 + item_popularity[item])
                n += 1
        popularity /= n * 1.0
        return popularity

    def score(self, train, test, vali):
        p = self.precision(test, vali)
        r = self.recall(test, vali)
        f = 2 * p * r / (p + r)
        c = self.coverage(train, test)
        o = self.popularity(train, test)
        return {'precision':p, 'recall':r, 'fmeasure':f, 'coverage':c, 'popularity':o}

class ItemCFRecommender(Recommender):
   
    def train(self, data):
        self.data = data
        self.weight = self._item_similarity_(data)    

    def recommend(self, user_items, topN):
        W = self.weight
        rank = {}
        for i in list(user_items):
            if not W.has_key(i):
                continue
            else:
                pass
                #print W[i]
            for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:topN]:
                if j in user_items:
                    continue
                rank.setdefault(j, 0)
                rank[j] += 1 * wj
        return sorted(rank.items(), key=lambda d: -d[1])[0:topN]

    def _item_similarity_(self, data):
        alpha = 0.01
        C = {}
        N = {}
        for id, items in data.items():
            for i in items:
                N.setdefault(i, 0)
                C.setdefault(i, {})
                N[i] += 1
                for j in items:
                    if i == j:
                        continue
                    C[i].setdefault(j, 0)
                    C[i][j] += 1 / math.log(1 + len(items) * 1.0)
        W = {}
        for i, related_items in C.items():
            W.setdefault(i, {})
            for j, cij in related_items.items():
                W[i].setdefault(j, 0)
                W[i][j] = cij / math.sqrt(N[i] ** (1 - alpha) * N[j] ** alpha)
        return W
       

class UserCFRecommender(Recommender):
    
    def train(self, data):
        self.weight = self._user_similarity_(data)

    def recommend(self, user_id, topN):
        rank = {}
        return rank


    def _user_similarity_(self, data):

        item_users = {}
        for id, items in data.items():
            for i in items:
                if i not in item_users:
                    item_users[i] = set()
                item_users[i].add(id)
        C = {}
        N = {}
        W = {}
        return W


class TopicRecommender(Recommender):
    pass

class CombineRecommender(Recommender):

    def train(self, data):
        pass

    def recommend(self, data, topN):
        pass

if __name__ == "__main__":
    print
    print "starting.."
    train_data = read_csv(TRAIN_FILE, primary=2, cols=[3])
    #test_data = read_csv(DATA_PATH + "/t1.submit", 1)
    test_data = read_csv(VALIDATE_FILE1, primary=0, cols=[3])
    vali_data = read_csv(VALIDATE_FILE2, primary=0, cols=[3])
    
    recommender = ItemCFRecommender()
    recommender.train(train_data)
    #rank = recommender.recommend(train_data['10449872'], 9)
    print recommender.score(train_data, test_data, vali_data)
    #recommender = UserCFRecommender()
    #recommender.train(train_data)
    #print recommender.recommend('11948349', 9)
    #print recommender.score(train_data, test_data, vali_data)
   
    

