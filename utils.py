import json

import random

import requests

from redis_db import redis_db

from douban_movie.settings import USER_AGENT_LIST

PROXY = None


def get_proxies():
    proxy = redis_db.get_proxy()
    real_proxy = {
        'http': proxy,
        'https': proxy
    }
    return real_proxy


def find_max(url, headers, classify, start=0, end=10000):

    global PROXY

    middle = (start + end) // 2
    if middle % 20:
       middle += 10
    retry = True
    while retry:
        try:
            proxy = PROXY or get_proxies()
            PROXY = proxy
            response = requests.get(url=url.format(start=middle, classify=classify), headers=headers, proxies=PROXY, allow_redirects=False, timeout=2)
            if response.status_code == 200:
                retry = False
            else:
                PROXY = None
                continue
        except Exception as e:
            print(e)
            print('error')
            PROXY = None
            continue
    if json.loads(response.text).get('data'):
        retry = True
        while retry:
            try:
                proxy = PROXY or get_proxies()
                PROXY = proxy
                response = requests.get(url.format(start=middle+20, classify=classify), proxies=PROXY, headers=headers, timeout=2, allow_redirects=False)
                if response.status_code == 200:
                    retry =False
                else:
                    PROXY = None
                    continue
            except:
                PROXY = None
                continue
        if not json.loads(response.text).get('data'):
            print('%s分类 找到最大值 %s'%(classify, middle))
            return classify, middle
        else:
            print('太小 middle is %s' %middle)
            return find_max(url, headers, classify, middle, end)
    else:
        print('太大 middle is %s' %middle)
        return find_max(url, headers, classify, start, middle)


def main():
    default_url = 'https://movie.douban.com/j/new_search_subjects?sort=T&range=0,10&tags=电影&start={start}&genres={classify}'
    # headers = {
    #     'Accept-Language': 'zh-CN,zh;q=0.9',
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'
    # }
    #
    # classify_list = ["剧情", "同性", "音乐", "歌舞", "传记", "历史", "战争", "西部",
    #                 "犯罪", "喜剧", "动作", "爱情", "科幻", "悬疑", "惊悚", "恐怖",
    #                  "奇幻", "冒险", "灾难", "武侠", "情色"]
    #
    # result = []
    # for classify in classify_list:
    #     result.append(find_max(default_url, headers, classify))
    # print(result)

    result = [('剧情', 9960), ('同性', 1280), ('音乐', 1780), ('歌舞', 920),
              ('传记', 1540), ('历史', 1560), ('战争', 1840), ('西部', 400),
              ('犯罪', 4660), ('喜剧', 9960), ('动作', 6440), ('爱情', 8360),
              ('科幻', 2700), ('悬疑', 3300), ('惊悚', 6500), ('恐怖', 4400),
              ('奇幻', 2900), ('冒险', 3220), ('灾难', 160), ('武侠', 380), ('情色', 540)]

    for classify in result:
        print('开始生成 %s 分类 request url' %classify[0])
        for start in range(0, classify[1], 20):
            url = default_url.format(start=start, classify=classify[0])
            redis_db.add_movie_url(url)


if __name__ == "__main__":
    main()

