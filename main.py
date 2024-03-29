# WIP
import json
import re
import requests
import time
from time import sleep

import artm
from datetime import datetime
import demoji
from django.core.serializers.json import DjangoJSONEncoder
# from nltk import bigrams
import os
from tqdm import tqdm
import vkapi
import utils
from IPython.core.debugger import set_trace

lc = artm.messages.ConfigureLoggingArgs()
lc.minloglevel = 3
lib = artm.wrapper.LibArtm(logging_config=lc)
tqdm._instances.clear()

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
dictionary.gather(data_path=dict_path) # dictionary.save(dictionary_path=dict_path)

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
# model.fit_offline(batch_vectorizer=bv, num_collection_passes=20)
# model.dump_artm_model('data/model100')

def h_pubs():
    pubs = utils.get_pubs() # ['id public name']
    print('Все пабы: ', pubs)
    for dpub in tqdm(pubs, position=0, leave=True):
    #for dpub in pubs:
        pub_id = dpub.split()[0]
        posts = vkapi.get_posts(int(pub_id), 100)
        pub_title = ' '.join(dpub.split()[1:])
        print('pub: ', pub_title)
        for i, post in enumerate(posts):
            raw_text = demoji.replace(post['text'])
            if len(raw_text.split()) <= 7:
                continue
            date = utils.UnixToHumanity(post['unix_date'])
            preprocessed_text = utils.sentence_to_words(raw_text)
            with open('data/current{}.vw'.format(bigramm_in_path), 'w') as vw_data:
                vw_data.write(utils._to_vw_format(0, preprocessed_text, bigramm))
            try:
                current_bv = artm.BatchVectorizer(
                    data_path="data/current{}.vw".format(bigramm_in_path),
                    data_format='vowpal_wabbit',
                    target_folder="data/current_batches{}".format(bigramm_in_path)
                )
                try:
                    topic_probs = model.transform(current_bv).values  # shape: (10, 1)
                    tags = []
                    for j, prob in enumerate(topic_probs):
                        if prob > 0.25:
                            tags.append(utils.topic_id2tag[j])
                    if not tags:
                        tags = ['Uncertain']
                except:
                    # no text
                    tags = ['Uncertain']
            except: # no text
                tags = ['Uncertain']
            
            dictionary = {
                # 'title': ,
                'description': raw_text,
                'location': utils.get_location(raw_text),
                'start_time': utils.get_date(raw_text, date_to_replace_year=date),
                'event_img_url': post['event_img'],
                'source_url': 'https://vk.com/wall-' + pub_id + '_' + str(post['post_id']),
                'tags': tags,
                'post_id': post['post_id'],
                'pub_time': date,
                'channel_data': {
                    'title': post["pub_name"],
                    'img_url': post['pub_img'],
                    'source_url': 'https://vk.com/club' + pub_id,
                    'pub_id': pub_id,
                },
            }
            #print(dictionary)
            #print('-' * 10, end='\n')
            #if i > 10:
            #    break
            #break
            jsoned_data = json.dumps(dictionary, cls=DjangoJSONEncoder) # .encode('utf-8') # , ensure_ascii=False).encode('utf-8')
            r = requests.post('http://rishel.pythonanywhere.com/events/add', data=jsoned_data)
            #print(type(r), r)

        print('Finished wall search.\n')

while True:
    h_pubs()
    sleep(3600 * 6)

