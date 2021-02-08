import vk
from time import sleep
import tqdm
import numpy as np

#token ='cdf1bc50a691a9419e316bb9e47d018c497597e27c43edd7af1f66b184c2025301376c746d0ff9d9f77fb'
#session2 = vk.Session(token)
#vk_api2 = vk.API(session2)
#print('Authorized')

login = '89778568689'
password = 'filomsk123'
app_id = 6741650

session = vk.AuthSession(app_id, login, password, scope='messages, friends, wall, groups')
vk_api = vk.API(session)
print('Authorized as human')

def message_send(id, text, att=''):
	sleep(1)
	try:
		vk_api2.messages.send(app_id=app_id, user_id=id, message=text, attachment=att, v='5.74')
		return 1
	except Exception as e:
		print(e)
		print('message_send')
		return 0

def get_posts(group_id, count=1, filter="all"):
    print("Get posts func %d" % group_id)
    sleep(0.3)
    posts = []
    number_posts = 0
    offset = 100
    try:
        vposts = vk_api.wall.get(owner_id=group_id, count=count, offset=0, filter=filter, v='5.74')
        info = vk_api.groups.getById(group_ids=abs(group_id), v="5.126")[0]
        max_number_posts = vposts["count"]
        print('Begin parsing', max_number_posts, 'posts')
        
        for number_posts in tqdm.tqdm(range(int(round(max_number_posts / float(offset))))):
            sleep(0.3)
            vposts = vk_api.wall.get(owner_id=group_id, count=count, offset=number_posts, filter=filter, v='5.126') # .74')
            number_posts=number_posts+offset
            if vposts["count"] > 0:
                for p in vposts["items"]:
                    r = dict()
                    r["text"] = p["text"]
                    r['unix_date'] = p["date"]
                    try:
                        n = len(p['attachments'])
                        if n == 1:
                            r['event_img'] = p['attachments'][-1]['photo']['sizes'][-1]['url']
                        else:
                            r['event_img'] = ''
                    except:
                        r['event_img'] = ''
                    r['post_id'] = p['id']
                    r['pub_name'] = info["name"]
                    r['pub_img'] = info['photo_200']
                    posts.append(r)
    except Exception as e:
        print(e)
    finally:
        return posts

