import artm
import gensim
from matplotlib import pyplot as plt
from natasha import DatesExtractor
# from nltk import bigrams
import numpy as np
import pymorphy2
import re

lc = artm.messages.ConfigureLoggingArgs()
lc.minloglevel = 3
lib = artm.wrapper.LibArtm(logging_config=lc)

stops = list(np.genfromtxt('data/bigartm.stopwords.txt', dtype='str'))
stops = set(stops + ['твой', 'кам', 'каждоить', 'как', 'когда', 'такой', 'одной', 'где', 'сколько', 'быть', 'взять', 'есть'])

dates_extractor = DatesExtractor()

topic_id2tag = {
    0: 'Внеучебные лекции', 1: 'Учебная информация',
    2: 'Объявления', 3: '',
    4: 'Научно-популярные лекции', 5: '',
    6: 'Поселение', 7: 'Билеты',
    8: 'Стипендии', 9: 'Новости',

    10: 'Сессия', 11: 'Внеучебные мероприятия',
    12: 'IT', 13: 'Квантовые технологии',
    14: 'Психология', 15: 'Олимпиады',
    16: 'Динамические системы', 17: '',
    18: 'Хакатоны', 19: '',

    20: 'Искусственный интеллект', 21: '',
    22: 'Технологические проекты', 23: 'Иностранные языки',
    24: 'Конкурсы и гранты', 25: '',
    26: 'Возможности для выпускников', 27: 'Стартапы',
    28: 'КИМ', 29: '',

    30: '', 31: 'Работа с абитуриентами',
    32: 'Музыка', 33: '',
    34: '', 35: '',
    36: 'Тренинги', 37: '',
    38: '', 39: 'Анализ данных',

    40: '', 41: 'Наука',
    42: 'Путевки', 43: 'Объявления',
    44: 'Выдача карт', 45: '',
    46: 'Спелеоклуб', 47: '',
    48: 'Волонтерство', 49: 'Матч века',

    50: '', 51: 'Театр',
    52: '', 53: 'Физика',
    54: 'Работа с выпускниками', 55: '',
    56: '', 57: '',
    58: '', 59: '',

    60: '', 61: '',
    62: '', 63: 'Учебные вопросы',
    64: 'Программирование', 65: 'Доклады',
    66: '', 67: '',
    68: 'Менторство', 69: '',

    70: '', 71: '',
    72: '', 73: 'Учебная информация',
    74: '', 75: 'Биология',
    76: '', 77: 'Спорт',
    78: '', 79: 'Биология',

    80: 'Научная деятельность', 81: 'Технологии',
    82: 'Объявления', 83: '',
    84: '', 85: '',
    86: '', 87: '',
    88: 'Культура', 89: '',

    90: '', 91: '',
    92: '', 93: '',
    94: '', 95: '',
    96: '', 97: '',
    98: '', 99: '',
}

def get_location(text):
    if re.search('[1-5]\\d\\d ГК', text):
        return re.search('[1-5]\\d\\d ГК', text).group(0)
    if re.search('[1-5]\\d\\d ЛК', text): 
        return re.search('[1-5]\\d\\d ЛК', text).group(0)        
    if re.search('[1-5]\\d\\d НК', text):
        return re.search('[1-5]\\d\\d НК', text).group(0)
    
    if re.search('\\d\\d\\d КПМ', text): 
        return re.search('\\d\\d\\d КПМ', text).group(0)
    
    if 'зале КСП' in text or 'зал КСП' in text:
        return 'конференц-зал КСП'
    if 'зале МСЦ' in text or 'зал МСЦ' in text:
        return 'конференц-зал МСЦ'

def sentence_to_words(sentence):
    morph = pymorphy2.MorphAnalyzer()
    output = []
    for token in gensim.utils.simple_preprocess(
            str(sentence.replace('\[club\\d*\\|', '').replace(']', '')),
            deacc=True
        ):  # deacc=True removes punctuations
        if token in stops:
            continue
        else:
            output.append(morph.parse(token)[0].normal_form)
    return ' '.join(output).replace('мфть', 'мфти')

def _to_vw_format(doc_index, document):
    if 0:
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

def get_date(string, date_to_replace_year):
    parsed_string = dates_extractor(string)
    if parsed_string:
        if 'month' in parsed_string[0].fact.as_json.keys() and 'day' in parsed_string[0].fact.as_json.keys():
            if 'year' in parsed_string[0].fact.as_json.keys():
                try:
                    return datetime(
                        year=parsed_string[0].fact.as_json['year'],
                        month=parsed_string[0].fact.as_json['month'],
                        day=parsed_string[0].fact.as_json['day']
                    )
                except:
                    return None
            else:
                try:
                    return datetime(
                        year=2020, month=parsed_string[0].fact.as_json['month'],
                        day=parsed_string[0].fact.as_json['day']
                    )
                except:
                    return None
        else:
            return None
    else:
        return None

def add_standard_scores(model, dictionary, modalities=("@raw_text", '@origin')):
    model.scores.add(
        artm.scores.SparsityThetaScore(name='theta_sparsity')
    )

    for modality in modalities:
        model.scores.add(
            artm.scores.SparsityPhiScore(name='phi_{}_sparsity'.format(modality),
            class_id=modality), overwrite=True
        )
        model.scores.add(
            artm.scores.TopTokensScore(name='top_tokens_{}'.format(modality),
            class_id=modality, num_tokens=15), overwrite=True
        )
        model.scores.add(artm.scores.PerplexityScore(
            name='perplexity_{}'.format(modality), dictionary=dictionary,
            class_ids=[modality]), overwrite=True
        )
        model.scores.add(
            artm.TopicKernelScore(name='topic_kernel_{}'.format(modality),
            probability_mass_threshold=0.3, class_id=modality), overwrite=True
        )

def create_model(num_topics, dictionary, origin=100000, bigramm=5, verbose=True, seed=16):
    if bigramm:
        if origin:
            class_ids = {'@raw_text': 1.0, '@origin': origin, '@2gramm':bigramm}
            modalities=('@raw_text', '@2gramm', '@origin')
        else:
            class_ids = {'@raw_text': 1.0, '@2gramm':bigramm}
            modalities=('@raw_text', '@2gramm')
    else:
        if origin:
            class_ids = {'@raw_text': 1.0, '@origin': origin}
            modalities=('@raw_text', '@origin')
        else:
            class_ids = {'@raw_text': 1.0}
            modalities=['@raw_text']

    model = artm.ARTM(
        # num_processors=12,
        topic_names=['topic {}'.format(i) for i in range(num_topics)],
        theta_columns_naming = 'title',
        show_progress_bars=verbose,
        num_document_passes = 5,
        class_ids=class_ids,
        seed=seed
    )
#     if origin:
    add_standard_scores(model, dictionary, modalities)
#     else:
#         add_standard_scores(model, dictionary, modalities=["@raw_text"])
    model.initialize(dictionary)

    return model

def plot_perp_and_sparsity(model, modality='@raw_text', use_first_perp=False):
    # TODO: add purity and contrast
    # https://matplotlib.org/gallery/api/two_scales.html

    f = plt.figure(figsize=(12,5))
    ax1 = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    if use_first_perp:
        ax1.plot(model.score_tracker["perplexity_{}".format(modality)].value)
    else:
        ax1.plot(range(1, model.num_phi_updates),
                 model.score_tracker["perplexity_{}".format(modality)].value[1:])
    ax1.set_title('perplexity')
    ax1.grid()
    ax2.plot(model.score_tracker["theta_sparsity"].value, label='$\\Theta$')
    ax2.plot(model.score_tracker["phi_{}_sparsity".format(modality)].value, label='$\\Phi$')
    ax2.set_title('$\\Phi$ and $\\Theta$ sparsity')
    ax2.legend()
    ax2.grid()

def plot_metrics(model, modality='@raw_text', use_first_perp=False):
    f = plt.figure(figsize=(12,5))
    ax1 = f.add_subplot(121)
    ax2 = f.add_subplot(122)
    if use_first_perp:
        ax1.plot(model.score_tracker["perplexity_{}".format(modality)].value)
    else:
        ax1.plot(range(1, model.num_phi_updates),
                 model.score_tracker["perplexity_{}".format(modality)].value[1:])
    ax1.set_title('perplexity')
    ax1.grid()
    ax2.plot(model.score_tracker["theta_sparsity"].value, label='$\\Theta$')
    ax2.plot(model.score_tracker["phi_{}_sparsity".format(modality)].value, label='$\\Phi$')

    ax1_1 = ax1.twinx()
    ax1_1.plot(model.score_tracker["topic_kernel_@raw_text"].average_purity, 'g')
    ax1_1.set_ylabel('Purity', color='tab:green')
    ax1_1.tick_params(axis='y', labelcolor='tab:green')

    ax2_2 = ax2.twinx()
    ax2_2.plot(model.score_tracker["topic_kernel_@raw_text"].average_contrast, 'r')
    ax2_2.set_ylabel('Contrast', color='tab:red')
    ax2_2.tick_params(axis='y', labelcolor='tab:red')

    f.tight_layout()  # otherwise the right y-label is slightly clipped
    ax2.set_title('$\\Phi$ and $\\Theta$ sparsity')
    ax2.legend()
    ax2.grid()

def print_top_terms(model, modality='@raw_text', indexes=False):
    if not indexes:
        indexes = model.score_tracker["top_tokens_{}".format(modality)].last_tokens.keys()
    else:
        indexes = list(map(lambda x: 'topic ' + str(x), indexes))
    for topic_name in indexes:
        tokens = model.score_tracker["top_tokens_{}".format(modality)].last_tokens
        res_str = topic_name + ': ' + ', '.join(tokens[topic_name])
        print(res_str)

