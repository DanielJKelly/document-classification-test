import numpy as np
DOC_LABELS = {
    'DELETION OF INTEREST': 1, 
    'RETURNED CHECK': 2, 
    'BILL': 3,
    'POLICY CHANGE': 4, 
    'CANCELLATION NOTICE': 5, 
    'DECLARATION': 6, 
    'CHANGE ENDORSEMENT': 7, 
    'NON-RENEWAL NOTICE': 8,
    'BINDER': 9, 
    'REINSTATEMENT NOTICE': 10, 
    'EXPIRATION NOTICE': 11, 
    'INTENT TO CANCEL NOTICE': 12, 
    'APPLICATION': 13,
    'BILL BINDER': 14
}

from copy import deepcopy

def labels_data(file):
    data = open(file, 'r')
    wds = []
    lines= []
    labels = []
    for line in data:
        lines.append(line.strip())
    
    for line in lines:
        comma = line.find(',')
        if comma != -1: 
            label = line[0:comma]
            words = line[comma + 1:].split(' ')
            wds.append(words)
            labels.append(DOC_LABELS[label])
    
    return [wds, labels]

# take file and return dict where classification type is key, and value is array of arrays of words
def csv_to_dict(file): 
    raw_data = open(file, 'r')
    lines = []
    results = {}

    for line in raw_data: 
        lines.append(line.strip())
    
    for line in lines: 
        comma = line.find(',')
        if comma != -1: 
            item = line[0:comma]
            words = line[comma + 1:].split(' ')
            if item not in results: 
                results[item] = []
                results[item].append(words)
            else:
                results[item].append(words)
    return results


def get_labels(dic):
    results = {}
    i = 0
    for label in dic:
        i +=1
        results[label.upper()] = i
    return results

# take wordDict and return dict where keys are classification types and value is a dict with keys being words and values being the word counts
def dict_to_counts(dic):
    results = {}
    for label in dic: 
        groups = dic[label]
        results[label] = {}
    
        for group in groups:
            for word in group:
                if word not in results[label]:
                    results[label][word] = 1
                else:
                    results[label][word] += 1
    return results

def global_dict_counts(dic): 
    results = {}
    for cat in dic: 
        words = dic[cat]
        for word in words: 
            if word not in results:
                results[word] = words[word]
            else:
                results[word] += words[word]
    return results

def ct_wds_by_doc(doc_dic):
    results = {}
    for label in doc_dic: 
        for doc in doc_dic[label]:
            uq = np.unique(doc)
            for w in uq: 
                if w not in results: 
                    results[w] = 1
                else: 
                    results[w] += 1
    return results

def global_dict_freq(dic): 
    return {k: v / len(dic) for k, v in dic.items()}

def ct_word_groups(dic, gp_size):
    results = {}
    for label in dic:
        results[label] = {}
        docs = dic[label]
        for doc in docs:
            for i in range(0,len(doc) - gp_size):
                gp = ','.join(doc[i: i+ gp_size])
                if gp not in results[label]:
                    results[label][gp] = 1
                else:
                    results[label][gp] += 1
    return results


def get_unique_words(counts):
    uniques = {}
    for key in counts: 
        uniques[key] = len(counts[key])
    return uniques

def word_sets_by_cat(counts):
    sets = []
    for key in counts:
        sets.append((key, set(counts[key].keys())))
    return sets

def global_uniques(counts):
    sets = map(lambda tuple: tuple[1], word_sets_by_cat(counts))

    return len(set.union(*sets))

def avg_length_by_cat(dic):
    results = {}
    for cat in dic: 
        num_docs = len(dic[cat])
        total = 0
        for doc in dic[cat]:
            total += len(doc)
        results[cat] = int(total / num_docs)
    return results

def uniques_by_cat(cat, sets):
    copy = sets[:]

    for i in range(0, len(copy)):
        if sets[i][0] == cat:
            cat_set = copy.pop(i)[1]
    
    copy_sets = map(lambda tpl: tpl[1], copy)
    return cat_set.difference(*copy_sets)

def dict_doc_lens(dic):
    c = deepcopy(dic)
    # map each array of docs to just the len of each doc 
    for label in c: 
        c[label] = list(map(lambda doc: len(doc), c[label]))
    return c

def list_doc_len_tpls(dic, labels):
    results = []
    for label in dic:
        for len in dic[label]:
            results.append((len, labels[label]))
    return results

def word_set_label_tps(dic, labels, word_lists):
    results = []
    for label in dic: 
        for doc in dic[label]:
            r = []
            l = len(doc)
            for lst in word_lists:
                if is_sub_list(lst, doc):
                    r.append(1)
                else:
                    r.append(0)
            r.append(DOC_LABELS[label])
            r.insert(0, l)
            results.append(tuple(r))
    return results

def gp_tuples(doc_dic, gp_dic, num):
    results = {}
    
    for cat in gp_dic: 
        gps = gp_dic[cat]
        results[cat] = sorted([(k, v / len(doc_dic[cat])) for k, v in gps.items()], key=lambda t: t[1], reverse=True)[0:num]
    
    return results

def is_sub_list(l1, l2):
    # does l2 contain l1 in correct order, contiguous
    if len(l2) < len(l1) or not l1 or not l2: 
        return False
    
    for i in range(0, len(l2) - len(l1) + 1):
        if l1 == l2[i: i+ len(l1)]:
            return True
    
    return False



