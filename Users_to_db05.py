# -*- coding: utf-8 -*-
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import exceptions
import MySQLdb
import Credentials as k
import sys
import tweepy
import time

__author__ = 'luisangel'

# CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET
KEYS = [['1aUE01m6RTZZntyfSAJSI8NwG', 'jwggsJbyz7bJpkFAvVRNFq1eMWTEdUYBXLXP8tmCf0sH2zZIdc',
         '126471512-12bRUjQjr5bDyIoL3gA6Wq1J0byRhh1MuQzDeaC3', 'wojWtKHGHkvqVc3KSvLliWP2U4qQlweQrMcjWbQVGmhMM'],
        ['Ko7HB8uECkVvd3hsiVRukb0lg', 'tVRyWEa4J0Yw9KBLzZMp2QOCoiaahClxAPNASN4Lwl2SfhIh8w',
         '126471512-OEmy4bcwiTfrPR1LljUUNtaDs33VUnhw3NB7oxXv', 'ZMqVs24giY7T2dMB2yA4Sdn0iz1yurIND2Eh44KPyl8fx'],
        ['Mk8X14g5E7XAqw3tWcNZiMLn3', 'r0NsM8CrwlHhZqI7niNh96M5OlfGFzxwHBBoksqYKgaDlOl7HS',
         '126471512-nDp9VF09ouMcYp4HC13shKhCDxKlFP1SeWyoJGBi', 'mCW9FvQAQCdHT2imaoSl5hSZtcGQfUnQ5w5EtqUxFWSrZ'],
        ['yDyQ2r8ygIYWG0nHqccMdYdZ1', '1AmCaMtC3XprLEwE7vhmSX6J0iCIe02kODXznfsbcp62mTvFo6',
         '126471512-eNGOjOEbV1B3nzbz3oWX2S1OEvwioguEOmjiQW6I', '1aniqa6EgGLjGyvnDoyUksnHoecBgirzzxoHWnswjKhBg'],
        ['EC007SKfmmVgn1BrKNr1Yziyh', 'Te07yqZJdhnr203Pk9jQB1M8eteH1F3gy8BjOKebsZhYxpvU7L',
         '126471512-76uE3zktCRzekZXWttc8GsezUn2BKYMmYjhhVVlf', 'g6miC1CBYuILAw8Ri8jFbx1YYtTaYKKrHgIbncVd5wEgS']
        ]
ID_KEY = 0

auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
api = tweepy.API(auth)
ID_BAD = 0
REGIONS = {'03': 'antofagasta',
           '05': 'atacama',
           '07': 'coquimbo',
           '14': 'puerto montt',
           '11': 'maule',
           '02': 'aysen',
           '16': 'arica',
           '04': 'temuco',
           '17': 'valdivia',
           '10': 'magallanes',
           '15': 'tarapaca',
           '01': 'valparaiso',
           '06': 'concepcion',
           '08': 'rancagua',
           '12': 'santiago'
           }

REGIONS_INV = {'Antofagasta': '03',
               'Atacama': '05',
               'Coquimbo': '07',
               'Los Lagos': '14',
               'Maule': '11',
               'Aysen': '02',
               'Arica y Parinacota': '16',
               'Araucania': '04',
               'Los Rios': '17',
               'Magallanes': '10',
               'Tarapaca': '15',
               'Valparaiso': '01',
               'Biobio': '06',
               'O\'Higgins': '08',
               'RM Santiago': '12'
               }


def get_connection_sql():
    # Returns a connection object whom will be given to any DB Query function.

    try:
        connection = MySQLdb.connect(host=k.GEODB_HOST, port=3306, user=k.GEODB_USER,
                                     passwd=k.GEODB_KEY, db=k.GEODB_NAME)
        return connection
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        sys.exit(1)


def get_id_lost_users_sql(connection, id_lost):
    query = "SELECT idLostUser FROM LostUser WHERE idLostUser = %s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_lost,))
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [x[0] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def get_id_user_sql(connection, id_user):
    query = "SELECT idUser FROM Users_table WHERE idUser = %s;"
    try:
        cursor = connection.cursor()
        cursor.execute(query, (id_user,))
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [x[0] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def insert_lost_user(connection, id_user):
    try:
        x = connection.cursor()
        x.execute('INSERT INTO LostUser VALUES (%s) ', (
            id_user,))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()


def get_new_api():
    global ID_KEY
    ID_KEY = 0 if ID_KEY >= 4 else ID_KEY + 1
    global auth
    auth = tweepy.OAuthHandler(KEYS[ID_KEY][0], KEYS[ID_KEY][1])
    auth.set_access_token(KEYS[ID_KEY][2], KEYS[ID_KEY][3])
    global api
    api = tweepy.API(auth)


def insert_user_sql(connection, user):
    id_user = user.get('id')
    while True:
        try:
            u = api.get_user(id_user)
            break
        except tweepy.TweepError, e:
            print "Primero: " + e.reason + " Termina."
            if e.reason == 'Failed to send request: (\'Connection aborted.\', ' \
                           'gaierror(-2, \'Name or service not known\'))':
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.reason == 'Failed to send request: HTTPSConnectionPool(host=\'api.twitter.com\', port=443): ' \
                           'Read timed out. (read timeout=60)':
                print 'Internet. Dormir durante 1 minuto. ' + e.message
                time.sleep(60)
                continue
            if e.message[0]['code'] == 34:
                print "Not found ApiTwitter id: " + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                return
            if e.message[0]['code'] == 63:
                print 'Usuario suspendido:' + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                return
            if e.message[0]['code'] == 50:
                print 'User not found:' + str(id_user)
                cn = get_connection_sql()
                insert_lost_user(cn, id_user)
                cn.close()
                return
            else:
                global ID_BAD
                if ID_BAD == id_user:
                    print "Id: %d durmio dos veces." % id_user
                    return
                ID_BAD = id_user
                # hit rate limit, sleep for 15 minutes
                print 'Rate limited. Dormir durante 15 minutos. code: ' + ' id: ' + str(id_user)
                get_new_api()
                continue
        except StopIteration:
            break

    if u.protected is True:
        cn = get_connection_sql()
        insert_lost_user(cn, id_user)
        cn.close()
        return
    try:
        screen_name = u.screen_name
    except AttributeError:
        screen_name = None
    screen_name = unicode(screen_name).encode('utf-8') if screen_name is not None else ''

    try:
        time_zone = u.time_zone
    except AttributeError:
        time_zone = None
    time_zone = unicode(time_zone).encode('utf-8') if time_zone is not None else ''

    try:
        name = u.name
    except AttributeError:
        name = None
    name = unicode(name).encode('utf-8') if name is not None else ''

    followers_count = u.followers_count

    geo_enabled = u.geo_enabled

    try:
        description = u.description
    except AttributeError:
        description = None
    description = unicode(description).encode('utf-8') if description is not None else ''

    tweet_chile = 0

    try:
        location = u.location
    except AttributeError:
        location = None
    location = unicode().encode('utf-8') if location is not None else ''

    friends_count = u.friends_count

    verified = u.verified

    try:
        entities = u.entities
    except AttributeError:
        entities = None
    entities = unicode().encode('utf-8') if entities is not None else ''

    try:
        utc_offset = u.utc_offset
    except AttributeError:
        utc_offset = None
    utc_offset = unicode().encode('utf-8') if utc_offset is not None else ''

    statuses_count = u.statuses_count

    try:
        lang = u.lang
    except AttributeError:
        lang = None
    lang = unicode().encode('utf-8') if lang is not None else ''

    try:
        url = user.url
    except AttributeError:
        url = None
    url = unicode().encode('utf-8') if url is not None else ''

    created_at = u.created_at

    listed_count = u.listed_count

    try:
        x = connection.cursor()
        x.execute('INSERT INTO Users_table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ',
                  (id_user,
                   screen_name,
                   time_zone,
                   name,
                   followers_count,
                   geo_enabled,
                   description,
                   tweet_chile,
                   location,
                   friends_count,
                   verified,
                   entities,
                   utc_offset,
                   statuses_count,
                   lang,
                   url,
                   created_at,
                   listed_count))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
        return

    region = user.get('region')
    region = unicode(region).encode('utf-8') if region is not None else ''

    if region == '':
        return

    if region == 'Chile':
        user_location = get_user_location(connection, 'santiago')
        user_location[0][1] = '00'
    else:
        city_name = REGIONS[REGIONS_INV[region]]
        user_location = get_user_location(connection, city_name)

    try:
        x = connection.cursor()
        x.execute('INSERT INTO User_location VALUES (%s,%s,%s,%s,%s) ', (id_user,
                                                                                  user_location[0][0],
                                                                                  user_location[0][1],
                                                                                  user_location[0][2],
                                                                                  user_location[0][3]
                                                                                  ))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
        return


def get_user_location(gdb_sql, city_name):
    query = "select country_code, region_code, longitude, latitude " \
            "from cities " \
            "where city_name = %s and country_code = 'cl';"
    try:
        cursor = gdb_sql.cursor()
        cursor.execute(query, (city_name,))
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [[x[0], x[1], x[2], x[3]]
                    for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1
    pass


def get_tweets_sql(gdb_sql):
    query = "SELECT * FROM Tweet ;"
    try:
        cursor = gdb_sql.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [[x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9], x[10], x[11], x[12], x[13]]
                    for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1
    pass


def get_connection_neo():
    try:
        gdb = GraphDatabase("http://neo4j:123456@localhost:7474/db/data/")
        return gdb
    except exceptions.StatusException as ex:
        print "Connection error with Neo4J: " + ex.result
        sys.exit(1)


def count_users_neo(gdb_neo):
    query = "MATCH (n:User) RETURN count(n)"
    results = gdb_neo.query(query, data_contents=True)
    return results.rows[0][0]


def get_list_users_neo(gdb, start):
    query = "MATCH (n:User) RETURN n skip {start} LIMIT 54000"  # Limit should same that range
    param = {'start': start}
    results = gdb.query(query, params=param, data_contents=True)
    return results.rows


def update_users():
    gdb_neo = get_connection_neo()
    gdb_sql = get_connection_sql()
    for start in [1080000, 1134000, 1188000, 1242000, 1296000]:
        users = get_list_users_neo(gdb_neo, start)
        for user in users:
            lost = len(get_id_lost_users_sql(gdb_sql, int(user[0].get('id'))))
            user_exist = len(get_id_user_sql(gdb_sql, int(user[0].get('id'))))
            if lost == 1 or user_exist == 1:
                continue
            insert_user_sql(gdb_sql, user[0])
            print "Processed " + str(user[0].get('id'))
    gdb_sql.close()
    pass


def update_tweets():
    gdb_sql = get_connection_sql()
    tweets = get_tweets_sql(gdb_sql)
    pass


def test():
    con = get_connection_sql()
    p = get_id_lost_users_sql(con, 43748620)
    print len(p)


if __name__ == '__main__':
    update_users()
