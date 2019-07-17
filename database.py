import sqlite3
from sqlite3 import OperationalError
from datetime import datetime

local_storage: dict = {}


def save_to_bd(original_url, short_url, period):
    creation_d = datetime.now()
    if period == '':
        new_month = creation_d.month + 1
    else:
        new_month = creation_d.month + int(period)

    if new_month > 12:
        delta = abs(12-new_month)
        expire_d = datetime(creation_d.year+1, delta, creation_d.day)
    else:
        expire_d = datetime(creation_d.year, new_month, creation_d.day)

    insert_row = """insert into web_url (long_url, short_url, creation_d, expired_d, count_use) values (
    '%s', '%s', '%s', '%s', %d)""" % (original_url, short_url, creation_d, expire_d, 1)
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute(insert_row)


def get_original_url(short_url):
    redirect_url = ''
    select_row = """select long_url from web_url where short_url='%s'""" % short_url
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res_cursor = cursor.execute(select_row)
        redirect_url = res_cursor.fetchone()[0]
    return redirect_url


def create_db():
    create_table = """create table if not exists web_url(
    long_url text primary key not null,
    short_url text not null,
    creation_d text not null,
    expired_d text not null,
    count_use int)"""
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(create_table)
        except OperationalError:
            pass


def check_dates():
    # method that deletes dates with overdue expire date
    check_date = """delete from web_url where expired_d < '%s'""" % datetime.now()
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        cursor.execute(check_date)


def update_local_storage():
    # method should update local storage of most popular urls requests
    popular_urls = """select long_url, short_url from web_url 
    group by long_url having count_use >= (select avg(count_use) 
    from web_url)"""
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        for row in cursor.execute(popular_urls):
            local_storage[row[0]] = row[1]
        # print(local_storage)


def is_exist(url):
    if local_storage.get(url) is None:
        return False
    return True


def update_url_count(url):
    select_row = """select long_url from web_url where long_url='%s'""" % url
    take_count = """select count_use from web_url where long_url = '%s'""" % url
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute(select_row).fetchone()
        if res is None:
            return False
        new_count = cursor.execute(take_count).fetchone()[0]+1
        update_row = """update web_url set count_use=? where long_url=?"""
        cursor.execute(update_row, (new_count, str(url)))
    return True


def get_short_url(url):
    select_row = """select short_url from web_url where long_url='%s'""" % url
    with sqlite3.connect('urls.db') as conn:
        cursor = conn.cursor()
        res = cursor.execute(select_row).fetchone()[0]
    return res
