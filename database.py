import sqlite3


conn = sqlite3.connect("data.db")
cursor = conn.cursor()


def create_table():
	cursor.execute("""CREATE TABLE mipt
		(u_id integer, m_text text, city text, date text)
		""")
	return 0


def add(id, text,topic_probs, city, date):
#	print("Add function")
	cursor.execute("INSERT INTO mipt VALUES (?,?,?,?,?)", (id, text,topic_probs, city, date))
	conn.commit()
	return id


def getmipt(city):
	sql = "SELECT * FROM mipt WHERE city=%s" % city
	cursor.execute(sql)
	return cursor.fetchall()


def getById(id):
    print('Get by ID')
    sql = "SELECT * FROM mipt WHERE u_id=%d" % id
    cursor.execute(sql)
    return cursor.fetchall()


def readFile(name):
	file = open(name, "r")
	data = file.read().split("\n")
	file.close()
	return data


def getAllidAnyWhe(group_id):
    print('Достал информацию из БД')
    #group_id = int(group_id)
    conn = sqlite3.connect("/home/Aleron751/Destroyer2.0/data_group.db")   #  /home/Aleron751/Destroyer2.0/
    cursor = conn.cursor()
    sql = "SELECT count FROM mipt WHERE group_id=%d" % int(group_id)   #number_count
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()[0][0]


def getAllMembers(group_id):
    print('Достал информацию из БД')
    #group_id = int(group_id)
    conn = sqlite3.connect("/home/Aleron751/Destroyer2.0/data_group.db")   #  /home/Aleron751/Destroyer2.0/
    cursor = conn.cursor()
    sql = "SELECT members FROM mipt WHERE group_id=%d" % int(group_id)   #number_count
    cursor.execute(sql)
    conn.commit()
    return cursor.fetchall()[0][0]


def addV(user_id, number):
    conn = sqlite3.connect("/home/Aleron751/Destroyer2.0/data_group.db")   #/home/Aleron751/Destroyer2.0/
    cursor = conn.cursor()
    req = "INSERT INTO mipt VALUES (?,?,?)"
    cursor.execute(req, (user_id, number, 0))
    conn.commit()
    print('Добавил в бд информацию')
    return user_id

def UpdateData(group_id, i):                     # Добавляем балл
    conn = sqlite3.connect("/home/Aleron751/Destroyer2.0/data_group.db")   #  /home/Aleron751/Destroyer2.0/
    cursor = conn.cursor()
    req ="UPDATE mipt SET count=? WHERE group_id=?;"
    cursor.execute(req, (i, group_id))
    conn.commit()
    print('Изменил состояние в UpdateData на '+str(i))

    print('Успех, число измененно')

def UpdateDataMembers(group_id, i):                     # Добавляем балл
    conn = sqlite3.connect("/home/Aleron751/Destroyer2.0/data_group.db")   #  /home/Aleron751/Destroyer2.0/
    cursor = conn.cursor()
    req ="UPDATE mipt SET members=? WHERE group_id=?;"
    if i ==None:
        i = ' '
    cursor.execute(req, (str(i), group_id))
    conn.commit()
    print('Изменил состояние в UpdateData на список учасников')

    print('Успех, число измененно')

def getPubs():
	return readFile("pubs.txt")


def getKeys():
	return readFile("keys.txt")

def getKey_board():
	return readFile("key_board.txt")

def getBadKeys():
	return readFile("badKeys.txt")


def getSpamPubs():
	return readFile('spam.txt')


def getBadLikesKeys():
	return readFile('likesbadkeys.txt')
