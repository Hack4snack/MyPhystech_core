# WIP
import json
import re
import requests

import artm
import database
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
import time
# from nltk import bigrams
import os
from tqdm import tqdm
# from time import sleep
import vkapi
import utils

lc = artm.messages.ConfigureLoggingArgs()
lc.minloglevel = 3
lib = artm.wrapper.LibArtm(logging_config=lc)

bigramm = 0.0
bigramm_in_path = '_2gramm' if bigramm else ''
model = artm.load_artm_model('data/model100')

# bv = artm.BatchVectorizer(
#     data_path="data/initial{}.vw".format(bigramm_in_path),
#     data_format='vowpal_wabbit',
#     target_folder="data/initial_batches{}".format(bigramm_in_path)
# )

dictionary = artm.Dictionary()
dict_path = os.path.join("data/initial_batches{}".format(bigramm_in_path), 'dict.dict')
dictionary.gather(data_path=dict_path)
# dictionary.save(dictionary_path=dict_path)

num_topics = 100
num_background_topics = 10
main_topics = ['topic {}'.format(i) for i in range(num_topics - num_background_topics)]
back_topics = ['topic {}'.format(i) for i in range(num_topics - num_background_topics, num_topics)]

# model = utils.create_model(num_topics, dictionary, origin=False, bigramm=0.0, verbose=True)
# model.regularizers.add(
#     artm.DecorrelatorPhiRegularizer(
#         name='decorrelator_phi', tau=0.05, gamma=0,
#         class_ids="@raw_text", topic_names=main_topics
#     )
# )
# 
# model.fit_offline(batch_vectorizer=bv, num_collection_passes=20)
# model.dump_artm_model('data/model100')

def _to_vw_format(doc_index, document):
    if bigramm:
        raise NotImplementedError
        # return "".join(
        #     (
        #         "doc_" + str(doc_index),
        #         " |@raw_text ",
        #         " ".join(re.findall("\\w{3,}", document)),
        #         " |@2gramm ",
        #         " ".join("_".join(pair) for pair in bigrams(document.split())),
        #         "\n",
        #     )
        # )
    else:
        return "".join(
            (
                "doc_" + str(doc_index),
                " |@raw_text ",
                " ".join(re.findall("\\w{3,}", document)),
                "\n",
            )
        )

def probs2tags(probs):
    tags = []
    for i, p in enumerate(probs):
        tags.append(utils.topic_id2tags[i])
    return tags

def UnixToHumanity(date):
	return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(date))

def h_pubs():
    pubs = database.getPubs()
    print('Все пабы ап',pubs)
    # Перебираем пабы из файла
    for dpub in tqdm(pubs):
        pub = dpub.split()
        posts = vkapi.get_posts(int(pub[0]), 100)
        group = dpub.split()[1]
        print(group)
        print('Сейчас буду посты обробатывать и выдавать')
        for p in posts: # Этот цикл будет отвечать за поиск по постам
            date = UnixToHumanity(p[2])
            POST_ID = p[3]
            text=p[1]

            preprocessed_text = utils.sentence_to_words(text)
            with open('data/current{}.vw'.format(bigramm_in_path), 'w') as vw_data:
                vw_data.write(_to_vw_format(0, preprocessed_text))

            try:
                current_bv = artm.BatchVectorizer(
                    data_path="data/current{}.vw".format(bigramm_in_path),
                    data_format='vowpal_wabbit',
                    target_folder="data/current_batches{}".format(bigramm_in_path)
                )
                try:
                    topic_probs = model.transform(current_bv).values  # shape: (10, 1)
                    tags = []
                    for i, p in enumerate(topic_probs):
                        if p > 0.3:
                            tags.append(utils.topic_id2tag[i])
                    if not tags:
                        tags = ['Uncertain']
                except: # no text
                    tags = ['Uncertain']
            except: # no text
                tags = ['Uncertain']
            
            dictionary = {
                'event_id': POST_ID,
                'description': text,
                'tags': tags,
                'start_time': utils.get_date(text, date_to_replace_year=date),
                'location': utils.get_location(text),
            }
            jsoned_data = json.dumps(dictionary, cls=DjangoJSONEncoder) # , ensure_ascii=False)
            requests.post('http://rishel.pythonanywhere.com/events/add', data=jsoned_data)

        print('Закончил поиск по стенам \n')


# while True:
# for _ in range(2):
h_pubs()
    #database.add(all, text, topic_probs)
