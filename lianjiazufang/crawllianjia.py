import csv
import pymysql
import warnings
import re
import requests
import random
import time


class Zufang(object):

    def __init__(self):
        self.p = re.compile(
            r'<li calss="clear LOGCLICKDATA">.*?class="info clear">.*?data-sl>(.*?)</a>.*?data-el="region">(.*?)</a>\s*(.*?)\s*</div>.*?class="totalPrice"><span>(.*?)</span>.*?data-price="(.*?)">',re.S
        )
        self.User_Agent = [{"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"},
                           {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"},
                           {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"}]
        self.headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image /webp, image / apng, * / *;q=0.8',
            'Accept - Language': 'zh - CN, zh;q = 0.9',
            'Connection': 'keep - alive',
            'Host': 'sz.lianjia.com',
            'User-Agent': random.choice(self.User_Agent)['User-Agent']
        }
        self.baseurl = 'https://sz.lianjia.com/ershoufang/pg'
        self.db = pymysql.Connect('localhost', 'root', '123qwe', 'lianjia', charset='utf8')
        self.cur = self.db.cursor()

    def getpage(self):
        startpn = int(input('请输入爬取起始页：'))
        stoppn = int(input('请输入爬取终止页：'))
        with open('链家.csv', 'a', encoding='gb18030', newline='') as f:
            self.write = csv.writer(f)
            for i in range(startpn, stoppn+1):
                print('正在爬取第%d页' % i)
                time.sleep(2)
                nurl = str(i-1)
                url = self.baseurl + nurl + '/'
                res = requests.get(url, headers=self.headers)
                res.encoding = 'utf-8'
                html = res.text
                print(html)
                self.parsepage(html, i)
            self.db.close()

    def parsepage(self, html, i):
        rlist = self.p.findall(html)
        print(rlist)
        self.writepage(rlist, i)

    def writepage(self, rlist, i):
        for t in rlist:
            l = list(t)
            self.write.writerow(l)
            ins = 'insert into lianjia(title,area,des,value,price) value("%s","%s","%s","%s","%s");' % (l[0], l[1], l[2], l[3], l[4])
            self.cur.execute(ins)
        self.db.commit()
        print('保存完成第%d页' % i)

    def main(self):
        self.getpage()


if __name__ == '__main__':
    Zufang().main()
