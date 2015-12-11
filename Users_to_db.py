# -*- coding: utf-8 -*-
__author__ = 'luisangel'

from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import exceptions
import MySQLdb
import Credentials as k
import sys

REGIONS = {'03': 'Antofagasta',
           '05': 'Atacama',
           '07': 'Coquimbo',
           '14': 'Los Lagos',
           '11': 'Maule',
           '02': 'Aysen',
           '16': 'Arica y Parinacota',
           '04': 'Araucania',
           '17': 'Los Rios',
           '10': 'Magallanes',
           '15': 'Tarapaca',
           '01': 'Valparaiso',
           '06': 'Biobio',
           '08': 'O\'Higgins',
           '12': 'RM Santiago'
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


def get_users_sql(connection):
    query = "SELECT idLostUser FROM LostUser ;"
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data is None:
            return None
        else:
            return [x[0] for x in data]
    except MySQLdb.Error:
        print "Error: unable to fetch data"
        return -1


def insert_user_sql(connection, user):
    id_user = user.get('id')

    screen_name = user.get('screen_name')
    screen_name = unicode(screen_name).encode('utf-8') if screen_name is not None else ''

    time_zone = user.get('time_zone')
    time_zone = unicode(time_zone).encode('utf-8') if time_zone is not None else ''

    name = user.get('name')
    name = unicode(name).encode('utf-8') if name is not None else ''

    followers_count = user.get('followers_count')

    region = user.get('region')
    region = unicode(region).encode('utf-8') if region is not None else ''

    geo_enabled = user.get('geo_enabled')

    description = user.get('description')
    description = unicode(description).encode('utf-8') if description is not None else ''

    chile = user.get('chile')

    location = user.get('location')
    location = unicode().encode('utf-8') if location is not None else ''

    friends_count = user.get('friends_count')

    try:
        x = connection.cursor()
        x.execute('INSERT INTO Users_table VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (id_user,
                                                                                   screen_name,
                                                                                   time_zone,
                                                                                   name,
                                                                                   followers_count,
                                                                                   region,
                                                                                   geo_enabled,
                                                                                   description,
                                                                                   chile,
                                                                                   location,
                                                                                   friends_count))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
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


def insert_tweets_sql(connection, tweet):
    id_user = user.get('id')

    screen_name = user.get('screen_name')
    screen_name = unicode(screen_name).encode('utf-8') if screen_name is not None else ''

    time_zone = user.get('time_zone')
    time_zone = unicode(time_zone).encode('utf-8') if time_zone is not None else ''

    name = user.get('name')
    name = unicode(name).encode('utf-8') if name is not None else ''

    followers_count = user.get('followers_count')

    region = user.get('region')
    region = unicode(region).encode('utf-8') if region is not None else ''

    geo_enabled = user.get('geo_enabled')

    description = user.get('description')
    description = unicode(description).encode('utf-8') if description is not None else ''

    chile = user.get('chile')

    location = user.get('location')
    location = unicode().encode('utf-8') if location is not None else ''

    friends_count = user.get('friends_count')

    try:
        x = connection.cursor()
        x.execute('INSERT INTO Users VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ', (id_user,
                                                                                   screen_name,
                                                                                   time_zone,
                                                                                   name,
                                                                                   followers_count,
                                                                                   region,
                                                                                   geo_enabled,
                                                                                   description,
                                                                                   chile,
                                                                                   location,
                                                                                   friends_count))
        connection.commit()
    except MySQLdb.DatabaseError, e:
        print 'Error %s' % e
        connection.rollback()
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
    query = "MATCH (n:User) RETURN n skip {start} LIMIT 50000"  # Limit should same that range
    param = {'start': start}
    results = gdb.query(query, params=param, data_contents=True)
    return results.rows


def update_users():
    gdb_neo = get_connection_neo()
    gdb_sql = get_connection_sql()
    number_users = count_users_neo(gdb_neo)

    for start in range(0, number_users, 50000):
        users = get_list_users_neo(gdb_neo, start)
        for user in users:
            insert_user_sql(gdb_sql, user[0])
        print start
    pass


def update_tweets():
    gdb_sql = get_connection_sql()
    tweets = get_tweets_sql(gdb_sql)
    pass


def test():
    gdb_neo = get_connection_neo()
    p = get_list_users_neo(gdb_neo, 2)
    print p


if __name__ == '__main__':
    update_users()
