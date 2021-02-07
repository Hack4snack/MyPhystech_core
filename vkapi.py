import vk
#from settings import login, password, app_id
from time import sleep
import tqdm
import numpy as np
import database

tokenchik='de96c79e42330715c5ffa9ab3429c79b013ad488a1d56f29de83be91bee50b64ffe5e973471118949f5ba'


token ='cdf1bc50a691a9419e316bb9e47d018c497597e27c43edd7af1f66b184c2025301376c746d0ff9d9f77fb'
session2 = vk.Session(token)  #Для сообщества
vk_api2 = vk.API(session2)
print('Авторизовался')


login = '89778568689'
password = 'filomsk123'
app_id = 6741650      #6476868  #6742403            #6476868
scope = 'messages, friends, wall, groups'

session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
vk_api = vk.API(session)

print('Авторизовался как чевовек')

def message_send(id, text, att=''):
	sleep(1)
	try:
		vk_api2.messages.send(app_id=app_id, user_id=id, message=text, attachment=att, v='5.74')
		return 1
	except Exception as e:
		print(e)
		print('message_send')
		return 0



# id =466138327
# text='ПРИВЕТ ИЗ СООБЩЕСТВА'
# message_send(id, text, att='')

def get_posts(group_id, count=1, filter="all"):
    print("Get posts func %d" % group_id)
    sleep(0.3)
    posts = []
    number_posts=0
    offset=100

    # print('Начинаю парсинг постов')
    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)
    try:
        vposts = vk_api.wall.get(owner_id=group_id, count=count, offset=0, filter=filter, v='5.74')
        info = vk_api.groups.getById(group_ids=abs(group_id), v="5.126")[0]
        #numper_posts=len(vposts["items"])
        max_number_posts = vposts["count"]
        print('Начинаю парсинг', max_number_posts, 'постов')
        
        for number_posts in tqdm.tqdm(range(int(round(max_number_posts / float(offset))))):
            sleep(0.3)
            vposts = vk_api.wall.get(owner_id=group_id, count=count, offset=number_posts, filter=filter, v='5.126') # .74')
            number_posts=number_posts+offset
            if vposts["count"] > 0:
                for p in vposts["items"]:
                    # r = p["from_id"], p["text"], p["date"], p['attachments'][-1]['photo']['sizes'][-1]['url'], p['id']
                    r = dict()
                    r["text"] = p["text"]
                    r['unix_date'] = p["date"]
                    try:
                        n = len(p['attachments'])
                        if n == 1:
                            r['event_img'] = p['attachments'][-1]['photo']['sizes'][-1]['url']
                    except:
                        r['event_img'] = ''
                    r['post_id'] = p['id']
                    r['pub_name'] = info["name"]
                    r['pub_img'] = info['photo_200']
                    posts.append(r)
    except Exception as e:
        print(e)
    finally:
        return posts #Формат вывода: Кто прислал, что прислал, когда прислал


def get_comments(owner_id, post_id):
    sleep(1)
    try:
    	cmnts = vk_api.wall.getComments(owner_id=owner_id, post_id=post_id, count=30, v='5.74')['items']
    	res = []
    	for c in cmnts:
        	a = c['from_id'], c['text'], c['date']
        	res.append(a)
    	return res
    except Exception as e:
    	print(e)
    	return []


def get_likes(owner_id, item_id):
	sleep(1)
	try:
		return vk_api.likes.getList(type='post', owner_id=owner_id, item_id=item_id, v='5.74')['items']
	except Exception as e:
		print(e)
		return []


def get_FI(id):
    sleep(0.5)
    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)

    Name = vk_api.users.get(user_ids=id, name_case = 'nom', v='5.92')[0]['first_name']
    print('name is taken')
    Last_name =vk_api.users.get(user_ids=id, name_case = 'nom', v='5.92')[0]['last_name']
    print('familia is taken')
    return Name, Last_name

def get_friends(id):
    sleep(0.5)
    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)

    try:
        return vk_api.friends.get(user_id=id, v='5.84')['count']
    except Exception as e:
        print('Не получилось взять friends')
        print(e)
        return 50




def get_board_topics(group_id):
    sleep(0.5)
    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)

    topics = vk_api.board.getTopics(group_id=group_id, v='5.92')["items"]


    topics_id=[]
    #print('Принтую топики после вкапи метода')
    #print(topics)
    for topic in topics:
        topic_id=topic["id"]
        topics_id.append(topic_id)
    return topics_id

def get_board_comment(group_id, topic_id, offset=0):

    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)

    from_id = 0
    c = vk_api.board.getComments(group_id=group_id, topic_id=topic_id, offset=offset, count=100, extended=1, sort='desc', v='5.92')
    #print(c)
    offset_limit=len(c['items'])
    text = c['items'][0]['text']
    print(text+'\n')
    id = c['items'][0]['id']
    date = c['items'][0]['date']
    if len(c['profiles']) != 0:
        from_id = c['profiles'][0]['id']
    return text, from_id, id, date, offset_limit


def getGroupINFOById(group_id):


    all=vk_api.groups.getById(group_id=group_id, fields='members_count', v='5.103')[0]
    group_name=all["name"]
    print(all)
    members_count = all['members_count']

    return group_name, members_count





def get_city(id):
	sleep(0.3)
	try:
		info = vk_api.users.get(user_ids=str(id), fields='city', v='5.84')[0]
		if 'city' in set(info.keys()):
			return info['city']['title']
		else:
			return 'non city'
	except Exception as e:
		print(e)
		return 'error city'

def get_info_about_deactivation(id):
	sleep(0.3)
	try:
		info = vk_api.users.get(user_ids=str(id), fields='city, domain', v='5.84')[0]
		if 'deactivated' in set(info.keys()):
		    return info['deactivated']

		elif  info["is_closed"] is True:  #Проверяем, закрытый ли
		    domain_str = info["domain"]
		    # Если закрытый, то оригинальный лу у него домен. За обычный домен не оставляем шансов
		    print(domain_str)
		    if 'id' in domain_str:
		        return 'privated'
		    else:
		        print('Смотрю на домен')
		        print('id' in domain_str)
		        print('Ошибка в логикеееееееееееееееееееееееееееееееееееееееееееееееееееееееееее')
		        return 'Живой'


		else:
			return 'Живой'
	except Exception as e:
		print(e)
		return 'error city'




def filterPeople(id):
    #print("FILTER")
    if int(id) > 0 and (get_friends(id) > 15):
        print('get city')
        status = get_info_about_deactivation(id)
        if status not in ['banned', 'deleted']:
            if get_city(id) != 'Сочи':
                return 1
        else:
            print('Мертвый')
    return 0


def HardFilterPeople(id):
    #print("FILTER")
    count_friends = get_friends(id)
    if int(id) > 0 and (count_friends > 15):

        if count_friends != 50:
            print('get city')
            status = get_info_about_deactivation(id)
            if status not in ['banned', 'deleted', 'privated']:
                if get_city(id) != 'Сочи':
                    return 1
            else:
                print('Мертвый или закрытый')
        else:
            print('Закрытый')
    return 0


def get_array_of_new_members(group_id):
    print('Зашел в поиск участников')
    all = np.array([])
    offset = 0
    #count = 1000

    olds = database.getAllMembers(group_id)
    if olds == None:
        olds=[1]
    else:
        #print('Старые:')
        #print(olds)
        olds=(str(olds)+' ').split()

    print(np.array(olds))
    old_len = len(olds)


    try:
        members = vk_api.groups.getMembers(group_id=group_id, offset=offset,  v='5.103')['items']
        count = len(members)
        members = [str(i) for i in members]

    except Exception as e:
        print('Не получилось достать список участников')
        print(e)
        sleep(2)
        members = [' Не получилось достать список участников']
        count = 0

    offset = len(members)
    members = np.array(members)
    all = np.hstack((all, members))




    # if mem_len > old_len:
    print('Начинаю искать новых участников группы')
    while count == 1000:
     #       print(mem_len)
        sleep(0.6)
    #        print(offset)
        members = vk_api.groups.getMembers(group_id=group_id, offset=offset,  v='5.103')['items']
        offset = offset + len(members)
        count = len(members)
        members = [str(i) for i in members]
        members = np.array(members)
        all = np.hstack((all, members))



    print('Взял длины сейчас/раньше')
    print(len(all))
    print(old_len)

    print('Вышел из цикла')
    #print(all)
    all_BD = ' '.join(all)
    database.UpdateDataMembers(group_id, all_BD)  #Записываем обновленный список людей

    print('Сейчас вот этих сравним')
    print(np.array(olds))
    print(np.array(all))

    olds = set(olds)
    members = set(all)

    membersBD=' '.join(members)
    database.UpdateDataMembers(group_id, membersBD)

    print('Вычитаю из нового старое')

    members.difference_update(olds)

    members = list(members)

    #members = ['535589045', '1']

    if ' Не получилось достать список участников' not in members:
        for member in members:
            if not HardFilterPeople(member):
                print('Мертвый или закрытый_Неоригинальный')
                members.remove(member)
                print('Удалил труп')
                print(member)
            else:
                print('Живой')

    new = members

    print('\n \n Нашел разность ' + str(np.array(new)))
    new = 'vk.com/id' + ' vk.com/id'.join(new)

    return new



def del_post(owner_id, post_id):
    post = '%s_%s' % (str(owner_id), str(post_id))
    sleep(0.5)

    # session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
    # vk_api = vk.API(session)
    try:
        if vk_api.wall.getById(posts=post, copy_history_depth=1, v='5.74'):
            vk_api.wall.delete(owner_id=owner_id, post_id=post_id, v='5.74')
            return 1
        return 0
    except Exception as e:
        print(e)
        return 0


def new_post(owner_id, text, att):
    sleep(1)
    try:
       # print('Размещаю пост')
        return vk_api.wall.post(owner_id=int(owner_id), message=text, attachments=att, v='5.74')

    except Exception as e:
        print(e)
        return 0


