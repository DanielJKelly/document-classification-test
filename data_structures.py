# import util
# import math
# input = 'raw-data.csv'

# # dict with keys as labels, values as array of docs
# docs_by_label = util.csv_to_dict(input)

# # dict with keys as labels, values as dicts of word counts for each doc by word
# wd_cts_by_doc = util.dict_to_counts(docs_by_label)

# # possible doc labels
# labels = util.get_labels(docs_by_label)

# # count of each distinct word in collection
# global_wd_cts = util.global_dict_counts(wd_cts_by_doc)

# # freq of each distinct word in collection
# global_wd_freq = util.global_dict_freq(global_wd_cts)

# num_wds_col = len(global_wd_cts)

# def stop_words(dic, num):
#     lst = sorted([(k,v) for k, v in dic.items()], key=lambda t: t[1], reverse=True)
#     return list(map(lambda t: t[0], lst[0:num]))

# tpls = [(k, v) for k, v in global_wd_cts.items()]

# singles = list(filter(lambda t: t[1] < 10, tpls))

