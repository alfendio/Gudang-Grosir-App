import psycopg2
import psycopg2.extras
import os
import re
import globalvar
import datetime

#wkt1 = datetime.datetime.now().strftime('%d_%m_%Y %H:%M:%S')

def getConnection():
    dict_connection = dict()
    port = globalvar.port
    db = globalvar.db
    user = globalvar.user
    pswd = globalvar.pswd
    if os.environ.get('GAE_ENV') == 'standard':
        host = '/cloudsql/%s' % (globalvar.instance_name)
    else:
        host = '127.0.0.1'
    string_params = (host, port, db, user, pswd)
    dict_connection['ksb-2022'] = """
        host='%s' port=%s dbname='%s' user='%s' password='%s'
        """ % string_params

    return dict_connection

class Database():
    def __init__(self, param, autocommit=True):
        self._dict_connection = getConnection()
        self._connection_det = self._dict_connection.get(param)
        self.autocommit = autocommit
        try:
            self._conn = psycopg2.connect(self._connection_det)
            self._curs = self._conn.cursor()
            self._curs.execute("SET TIMEZONE='Asia/Jakarta'")
        except psycopg2.Error as error:
            raise Exception('%s, Database : %s' % (error, 'Tidak Ditemukan'))

    def select(self, text_query):
        '''
            Fungsi ini digunakan untuk select query tanpa parameter
            @param select_stringL Merupakan statement query yang dipakai
            @return: status =
        '''
     
        try:
            self._curs.execute(text_query)
            data = self._curs.fetchall()
        except psycopg2.Error as error:
            data = "Error : {} - {}".format(text_query, error)
            #parameter_text = (wkt1, data, text_query)
        result = data
        return result

    def execute(self, text_query, value):
        '''
            Fungsi ini digunakan untuk insert, update, dan delete
        '''
        status = False
        try:
            self._curs.execute(text_query,value)
            self._conn.commit()
            data = self._curs.rowcount
            status = True
        except psycopg2.Error as error:
            data = "Error {} - {}".format(text_query, error)
        result = str(data) + "Berhasil"
        return status, result
