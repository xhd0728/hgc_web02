import requests
import time
from fake_useragent import UserAgent
from lxml import etree

text_ls = []
link_ls = []
sleep_time = 0.1

for page in range(8, 10):
    print(f'##### page {page} #####')
    if page == 1:
        url = 'http://qihang.hrbeu.edu.cn/958/list.htm'
    else:
        url = f'http://qihang.hrbeu.edu.cn/958/list{page}.htm'
    res = requests.get(url=url, headers={'user-agent': UserAgent().random})
    res.encoding = 'utf-8'
    html = res.text
    e = etree.HTML(html)
    ele_link_ls = e.xpath('//span[@class="Article_Title"]/a/@href')
    ele_text_ls = e.xpath('//span[@class="Article_Title"]/a/@title')

    for link, title in zip(ele_link_ls, ele_text_ls):
        _link = 'http://qihang.hrbeu.edu.cn'+link
        link_ls.append(_link)
        text_ls.append(title)
    time.sleep(sleep_time)

    # for link, title in zip(link_ls, title_ls):
    #     print(f'{link} - {title}')

for text, link in zip(text_ls, link_ls):
    res = requests.get(url=link, headers={'user-agent': UserAgent().random})
    res.encoding = 'utf-8'
    html = res.text
    e = etree.HTML(html)
    timer_ls = e.xpath('//*[@id="container"]/div/div/p/span[3]')
    click_ls = e.xpath('//*[@id="container"]/div/div/p/span[4]/span')
    try:
        click_num = click_ls[0].xpath('string(.)').strip()
        timer = timer_ls[0].xpath('string(.)')
    except Exception as e:
        print(str(e))
        click_num = 0
        timer = '1970-01-01'
    print(f'{timer} - {text} - {click_num}')
    time.sleep(sleep_time)
