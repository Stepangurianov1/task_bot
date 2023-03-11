import datetime

import psycopg2
import requests
from bs4 import BeautifulSoup as BS
import time
from multiprocessing import Pool
from itertools import chain
from settings import PASSWORD, USER, HOST, DBNAME

# page = 1


def main_data(page):
    request = requests.get(f"https://codeforces.com/problemset/page/{str(page)}?order=BY_SOLVED_DESC&locale=ru")
    html = BS(request.content, 'html.parser')
    table = html.find('table', attrs={'class': 'problems'})
    data_one = []
    for row in table.find_all("tr"):
        cells = row.find_all("td")

        id, name, topic, difficult, solved = '', '', '', '', ''
        for el in cells:
            if el.find("div") is not None:
                s = el.find_all("div")[0].find('a').text
                name = " ".join(s.split())
                stings = ''
                for num, i in enumerate(el.find_all("div")[1].find_all("a")):
                    if num > 0:
                        stings += ', '
                    stings += i.string
                    topic = stings
            elif el.find("span") is not None:
                difficult = el.find("span").string
            elif el.find("a") is not None:
                if el.find("a").string is not None:
                    s = el.find("a").string
                    id = " ".join(s.split())
                else:
                    solved = str(el.find("a").contents[1])[2:]
        if difficult is not None and difficult != '':
            result = (id, name, topic, str(difficult), solved)
            data_one.append(result)
            # print(result)
    return data_one
    # data.append(result)


def main_pool():
    data_result = []
    timer = time.time()
    list_page = [el for el in range(1, 69)]
    with Pool(12) as p:
        data_result.extend(p.map(main_data, list_page))
    # print('time - ', time.time() - timer)
    return data_result


def write_data():
    data = list(chain(*main_pool()))
    conn = psycopg2.connect(dbname=DBNAME, user=USER,
                            password=PASSWORD, host=HOST)
    cursor = conn.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS tusks(id varchar(6) not null, name text not null, topic text, '
        'difficult int, solved  varchar(10))')
    args = ','.join(cursor.mogrify("(%s,%s,%s, %s, %s)", i).decode('utf-8')
                    for i in data)
    cursor.execute("INSERT INTO tusks VALUES " + args)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    write_data()
    print(datetime.datetime.now(), 'Произошла запись в бд')
