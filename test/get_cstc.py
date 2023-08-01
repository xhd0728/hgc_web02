import requests
from fake_useragent import UserAgent
from lxml import etree
import time

text_ls = []
link_ls = []
sleep_time = 0.2

for page in range(8, 10):
    print(f'##### page {page} #####')
    if page == 1:
        url = 'http://cstc.hrbeu.edu.cn/3687/list.htm'
    else:
        url = f'http://cstc.hrbeu.edu.cn/3687/list{page}.htm'
    res = requests.get(url=url, headers={'user-agent': UserAgent().random})
    res.encoding = 'utf-8'
    html = res.text
    e = etree.HTML(html)
    title_ls = e.xpath('//span[@class="column-news-title"]')

    for ele in title_ls:
        ele_text = ele.xpath('string(.)')
        ele_href = ele.xpath('parent::a')[0].get('href')
        if ele_href[0] == '/':
            ele_href = 'http://cstc.hrbeu.edu.cn'+ele_href
        text_ls.append(ele_text)
        link_ls.append(ele_href)
    # for text, link in zip(text_ls, link_ls):
    #     print(f'{text} - {link}')
    time.sleep(sleep_time)

for text, link in zip(text_ls, link_ls):
    if 'weixin' in link or 'redirect' in link:
        continue
    res = requests.get(url=link, headers={'user-agent': UserAgent().random})
    res.encoding = 'utf-8'
    html = res.text
    e = etree.HTML(html)
    timer_ls = e.xpath('/html/body/div[3]/div/div[2]/div/p/span[1]')
    click_ls = e.xpath('/html/body/div[3]/div/div[2]/div/p/span[4]/span')
    try:
        click_num = click_ls[0].xpath('string(.)').strip()
        timer = timer_ls[0].xpath('string(.)')[-10:]
    except Exception as e:
        print(link)
        click_num = 0
        timer = '1970-01-01'
    print(f'{timer} - {text} - {click_num}')
    time.sleep(sleep_time)
