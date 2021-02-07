import vkapi
import database
import time
from time import sleep

import numpy as np
from tqdm import tqdm

def filterPunc(str):
	punct = "?.,!-()\/\n"
	for p in punct:
		str = str.replace(p, ' ')
	return str.split()



def UnixToHumanity(date):
	return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(date))


def filterPeople(id):
    print("FILTER")
    if int(id) > 0 and (vkapi.get_friends(id) > 15):
        print('get city')
        status = vkapi.get_info_about_deactivation(id)
        if status not in ['banned', 'deleted']:
            if vkapi.get_city(id) != 'Сочи':
                return 1
        else:
            print('Мертвый')
    return 0


def h_post(group_id, post, city, place):
    print('Берем вот этот пост:')
    print(post[1])
    id = post[0]
    date = UnixToHumanity(post[2])
    DATE=date.split()
    if int(DATE[3]) in [2019,2020]:
        print('Отфильтровал по дате этого года')
        keys = set(database.getKeys())
        badKeys = set(database.getBadKeys())
        text = set(filterPunc(post[1].lower()))
        print("Вытащил инфу про пост")

        if not (text & badKeys):
        #if text & keys and not (text & badKeys):
            print("Есть ключевые слова")
            if (not database.getById(id)) and filterPeople(id):
                print("Отфильтровали. Нет в бд. Друзей > 30")
                #database.add(id, post[1], city, date)
                print('Добавил в бд')
                name, Last_name = vkapi.get_FI(id)
                Name = str(name) + ' '+ str(Last_name)
                #'[id'+str(id)+"|Новый участник!!!!]
                #msg = "vk.com/id" + str(id) + "\n" + post[1] + '\n'+date#+'\n'+'vk.com/group'+str(pub)
                #msg = '[id'+str(id)+'|'+str(Name)+']' + "\n" + post[1] + '\n'+date#+'\n'+'vk.com/group'+str(pub)

                group_name, number_count = vkapi.getGroupINFOById(group_id)

                msg_up = '[id'+str(id)+'|'+str(Name)+']' + "\n" + post[1] + '\n'+date+'\n'+'Источник: ' +str(place) +'\n'+'[public'+str(group_id)+ '|' + str(group_name) + ']'

                msg = '[id'+str(id)+'|'+str(Name)+']' + "\n" + post[1] + '\n'+date+'\n'+'Источник: '+str(place)
                #vkapi.message_send(466138327, msg_up)
                #vkapi.message_send(421464245, msg_up)
                #vkapi.message_send(553620033, msg)    # Эдгард. Если что делитнуть
                #vkapi.message_send(128836091, msg) # Милюкин
                #vkapi.message_send(78037600,  msg_up) # Камчаткин
                #vkapi.message_send(123962593, msg) # Арсен Медоян
                #vkapi.message_send(176654286, msg_up)  # Миленькин
                #vkapi.message_send(97581396, msg)  # Напсо
                #vkapi.message_send(150821903, msg) # Альбина Терещенко
                #vkapi.message_send(176654286, msg)
                #vkapi.message_send(389608010, msg)
                #vkapi.message_send(555249697, msg)
                #vkapi.message_send(440164728, msg)
                database.add(id, post[1], city, date)
                print('Заснул')
                sleep(0.31)
                return 0
            print('Этот пост уже есть в БД \n')
            return 0   # Уже есть в базе. Значит уже был тут, нет смысла искать дальше
        return 0
    return 0

def h_cmnts(pub, post):
    print('Идет поиск по постам с комментами')
    cmnts = vkapi.get_comments(int(pub[0]), post)
    for cmnt in cmnts:
        h_post(pub[0][1:], cmnt, pub[1], 'Комментарии')


def h_likes(pub, post, city, date, text):
	badKeys = set(database.getBadLikesKeys())
	likes = vkapi.get_likes(pub, post)
	msg = 'Лайкнул пост: %d в группе vk.com/club%d\n%s' % (post, -pub, date)
	for l in likes:
	    if not database.getById(l) and not text & badKeys:
	   # if not database.getById(l) and filterPeople(l) and not text & badKeys:
		    database.add(l, msg, city, date)
		    #vkapi.message_send(421464245, 'vk.com/id' + str(l) + '\n' + msg)
		    #vkapi.message_send(466138327, 'vk.com/id' + str(l) + '\n' + msg)
		    #466138327  Анатолий
		    #176654286   Саша
		    #421464245  Татьяна
            #database.add(l, msg, city, date)

def h_board(group_id):
    print('Начинаю поиск по обсуждениям \n')
    #group_id='78172201'
    print('новая группа \n'+str(group_id)+'\n')
    city = 'laza'
    topics = vkapi.get_board_topics(group_id)
    new_db = []
    print('Смотрим темы')
    print(topics)
    for topic in topics:
        print('Выбрал новую тему обсуждения')
        offset = 0
        p = vkapi.get_board_comment(group_id, topic, offset)
        offset_supremum=p[4]
        print('Смещение первое:')
        print(str(offset))
        print(offset_supremum)

        for offset in range(0, int(offset_supremum)):
            sleep(0.33)
            print('Смещение второе')
            #sleep(0.2)
            print(str(offset))
            c = vkapi.get_board_comment(group_id, topic, offset)
            from_id=c[1]
   #         id=c[2]
            date = UnixToHumanity(c[3])
            DATE=date.split()
            keys = set(database.getKey_board())
            badKeys = set(database.getBadKeys())
            text = set(filterPunc(c[0].lower()))
            offset = offset + 1

            if int(DATE[3]) in [2020, 2021] : #Проверели этого ли года.
                print('Подошел по дате')
                #if text & keys and not (text & badKeys): #Есть ли ключевые слова.
                if not (text & badKeys): #Есть ли ключевые слова.
                    print('Есть маркеры')

                    if (not database.getById(from_id)) and filterPeople(from_id):
                        print('Нет в бд и пройден фильтр')
                        print('Вот такой текст')
                        print(c[0])
                        database.add(from_id, c[0], city, date)
                        print('Добавил в бд')

                        name, Last_name = vkapi.get_FI(from_id)
                        Name = str(name) + ' '+ str(Last_name)
                        group_name, number_count = vkapi.getGroupINFOById(group_id)

                        msg = '[id'+str(from_id)+'|'+str(Name)+']' + "\n" + c[0] + '\n'+date+'\nИсточник: обсуждения' +'\n'+'[public'+str(group_id)+ '|' + str(group_name) + ']'

                        #vkapi.message_send(176654286, msg)
                        #vkapi.message_send(466138327, msg) #Анатолий
                        #vkapi.message_send(421464245, msg)
                        #vkapi.message_send(78037600,  msg) # Камчаткин

                    break    # Можно выходить из цикла, потому что дальнейшие сообщения этого сообщения уже проверялись
            else:
                break
    #vkapi.set_topics(new_db)


def get_array_of_new_members():

    mass=[]
    all = np.array(mass)




def h_pubs():
    pubs = database.getPubs()
    print('Все пабы ап')
    print(pubs)
    # Перебираем пабы из файла
    i=1
    for dpub in pubs:
        print(i)
        i=i+1
        pub = dpub.split()
        print('Новый паблик пошел \n')
        #print(dpub)
        posts = vkapi.get_posts(int(pub[0]), 100)

        #print(posts[0])
        group = dpub.split()[1]
        print(group)
        print('Сейчас буду посты вставляdddть')
        #print(posts[0])



        print('Теперь начинаем чекать стены и комментарии к постам на этих стенах.')
        for p in tqdm(posts): # Этот цикл будет отвечать за поиск по постам
            print(p)

            date = UnixToHumanity(p[2])

            #finish=h_post(pub[0][1:], p, pub[1], "Стена")
            #print(group)
            #print('группа')

            database.add(p[3], p[1], group, date)

            # if finish==1:
            #     break
        print('Закончил поиск по стенам \n')

#         for p in posts: # Этот цикл будет отвечать за поиск по коментам постов
#             h_cmnts(pub, int(p[3]))
# 		#	h_likes(int(pub[0]), int(p[3]), pub[1], UnixToHumanity(p[2]), p[1])

#         try:
#             h_board(pub[0][1:])  # Обсуждения
#         except Exception as e:
#             sleep(2)
#             print('Проверь вот тут!!!!!!!!!!!!')
#             print(e)

#         sleep(0.2)
#         group_name, number_count = vkapi.getGroupINFOById(pub[0][1:])
#         database.addV(pub[0][1:], number_count)



#         if int(number_count)%5 == 0:          # fix it 1
#             number_count_old=database.getAllidAnyWhe(pub[0][1:])
#             print('Было: '+ str(number_count_old))
#             print('Стало: '+ str(number_count))
#             if  int(number_count) > int(number_count_old):
#                 database.UpdateData(pub[0][1:], number_count)
#                 msg_up = '[public'+str(pub[0][1:])+ '|' + str(group_name) + ']' + '\n' + 'Участников было/стало: ' + str(number_count_old) +'/'+str(number_count) + '\nНовые участники:\n'

#                 group_id=pub[0][1:]
#                 people = vkapi.get_array_of_new_members(group_id)

#                 #print(people)
#                 msg_up = msg_up + people


#                 print('отправил результаты')
#                 vkapi.message_send(176654286, msg_up)  # Миленькин

def h_spam(messange):
	pubs = database.getSpamPubs()
	for pub in pubs:
		id, t = pub.split()
		posts = vkapi.get_posts(int(id), 100, 'others')
		i = 0
		print('start:')
		for post in posts:
			print('i = %d' % i)
			print(post[0])
			if post[0] == 466138327 and i < 5:
				break
			elif post[0] == 466138327:
					vkapi.del_post(id, post[3])
					vkapi.new_post(id, messange, '')
					break
			else:
				i += 1
		if i == 20:
			vkapi.new_post(id, messange, '')
