# "Database code" for the DB Forum.

import datetime
import psycopg2
import bleach

DBNAME = "news"


def article():
    data = psycopg2.connect(database=DBNAME)
    cursor = data.cursor()
    cursor.execute("select articles.title, count(*) as num "
                   "from articles, log where log.path like "
                   "concat('%', articles.slug, '%') and "
                   "log.status = '200 OK' and log.method = 'GET' "
                   "group by title order by num desc limit 3")
    articles = cursor.fetchall()
    """Return most popular three articles of all time"""
    data.close()
    return articles


def g_authors():
    data = psycopg2.connect(database=DBNAME)
    cursor = data.cursor()
    cursor.execute("select authors.name, count(*) as num "
                   "from articles, authors, log where "
                   "articles.author = authors.id and "
                   "log.path like concat('%', articles.slug, '%' ) "
                   "and log.status = '200 OK' and log.method = 'GET' "
                   "group by name order by num desc")
    authors = cursor.fetchall()
    """Return most popular article authors of all time"""
    data.close()
    return authors


def g_log():
    data = psycopg2.connect(database=DBNAME)
    cursor = data.cursor()
    cursor.execute("select date, avg from (select date, round((sum(error) "
                   "/ (select count(*) from log where (time::date) "
                   "= date) * 100), 2) as avg from (select (time::date) "
                   "as date, count(*) as error from log where status "
                   "like '404 NOT FOUND' group by date) as perc group "
                   "by date order by avg  desc) as final where "
                   "avg >= 1")
    log = cursor.fetchall()
    """Return On which days did more than 1% of requests lead to errors"""
    data.close()
    return log
