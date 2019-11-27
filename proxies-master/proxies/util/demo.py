import requests


proxies = {
    'https': '1.119.148.218:9797'
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Cookie': 'ssuid=772149900; TYCID=798f4280f49f11e992fe7b09e9496f88; undefined=798f4280f49f11e992fe7b09e9496f88; _ga=GA1.2.1242727195.1571730142; jsid=SEM-BAIDU-PP-VI23xian-000873; _gid=GA1.2.964208706.1574039135; tyc-user-info=%257B%2522claimEditPoint%2522%253A%25220%2522%252C%2522myAnswerCount%2522%253A%25220%2522%252C%2522myQuestionCount%2522%253A%25220%2522%252C%2522signUp%2522%253A%25220%2522%252C%2522explainPoint%2522%253A%25220%2522%252C%2522privateMessagePointWeb%2522%253A%25220%2522%252C%2522nickname%2522%253A%2522%25E5%2585%258B%25E9%2587%258C%25E6%2596%25AF%25E8%2592%2582%25E5%25A8%259C%25C2%25B7%25E8%2589%25BE%25E4%25BC%25AF%25E7%259B%2596%25E7%2589%25B9%2522%252C%2522integrity%2522%253A%25220%2525%2522%252C%2522privateMessagePoint%2522%253A%25220%2522%252C%2522state%2522%253A%25220%2522%252C%2522announcementPoint%2522%253A%25220%2522%252C%2522isClaim%2522%253A%25220%2522%252C%2522bidSubscribe%2522%253A%2522-1%2522%252C%2522vipManager%2522%253A%25220%2522%252C%2522discussCommendCount%2522%253A%25220%2522%252C%2522monitorUnreadCount%2522%253A%2522113%2522%252C%2522onum%2522%253A%25220%2522%252C%2522claimPoint%2522%253A%25220%2522%252C%2522token%2522%253A%2522eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzg1MzI3NTA5MCIsImlhdCI6MTU3NDMxNDM3MywiZXhwIjoxNjA1ODUwMzczfQ.5-yrL0Al9cxI3sC6PmVqJUVU6gDw9pyOHIUIH6aPMDDL-v-c4m1ddDS0Ub2L2QnbmiMAmbf3T4gP_Kg1_87X8w%2522%252C%2522pleaseAnswerCount%2522%253A%25220%2522%252C%2522redPoint%2522%253A%25220%2522%252C%2522bizCardUnread%2522%253A%25220%2522%252C%2522vnum%2522%253A%25220%2522%252C%2522mobile%2522%253A%252213853275090%2522%257D; auth_token=eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiIxMzg1MzI3NTA5MCIsImlhdCI6MTU3NDMxNDM3MywiZXhwIjoxNjA1ODUwMzczfQ.5-yrL0Al9cxI3sC6PmVqJUVU6gDw9pyOHIUIH6aPMDDL-v-c4m1ddDS0Ub2L2QnbmiMAmbf3T4gP_Kg1_87X8w; __insp_wid=677961980; __insp_slim=1574317980694; __insp_nv=true; __insp_targlpu=aHR0cHM6Ly93d3cudGlhbnlhbmNoYS5jb20vY2xhaW0vZW50cnk%3D; __insp_targlpt=5LyB5Lia6K6k6K_BIC0g5aSp55y85p_l; __insp_norec_howoften=true; __insp_norec_sess=true; aliyungf_tc=AQAAAIi2qVroggkAUCVJJ5p9IUUKUQh+; csrfToken=wKOYB0zCq12CSz6jTX6l5Zpw; cloud_token=8be8529a545c4a4cb39e349ac757e229; bannerFlag=true; Hm_lvt_e92c8d65d92d534b0fc290df538b4758=1574230669,1574298246,1574385410,1574404392; RTYCID=322d26cd2ef54aa49b813b42f488e32a; cid=2352882447; ss_cidf=1; token=c5d447292137460fb018aba4f5612aed; _utm=2e3af414498c4d7397cebbcd55650539; Hm_lpvt_e92c8d65d92d534b0fc290df538b4758=1574405894; _gat_gtag_UA_123487620_1=1',
    'Host': 'www.tianyancha.com',
    'Referer': 'https://www.tianyancha.com/',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36',
}

a = requests.get('https://www.tianyancha.com/humansearch/罗永浩?pn=1', headers=headers)
print(a.text)


