# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""
import time,  socket,requests, threading, os ,urllib2
from bs4 import BeautifulSoup


import IpSpider


class TmallSpider(object):
    """
        创建爬虫类
    """

    def __init__(self, Tmall_mysql, data ,proxy=True):
        self.param = data
        self.proxy = proxy
        self.load_page(Tmall_mysql)


    def load_one(self, url, num=0):
        """
        加载网页
        :param url: 爬取地址
        :return: 爬取的网页源代码
        """

        request = requests.get(url = url,headers = self.param['headers'])
        contect = request.content
        return contect

    def load_proxy(self, url ):
        """
        加载有伪装ip的爬取页面
        :param url: 爬取地址
        :return: 爬取的网页源代码
        """
        self.proxy_set(status=True)
        proxy = urllib2.ProxyHandler(self.proxy)
        opener = urllib2.build_opener(proxy)
        urllib2.install_opener(opener)
        request = urllib2.Request(url=url, headers=self.param['headers'])
        try:
            connect = urllib2.urlopen(request)
            boday = connect.read()
        except urllib2.HTTPError:
            boday = ''
            pass

        return boday

    def load_page(self, mysql_db):
        """
        网页page分析
        :param url: 爬去网页url
        :param num: 下载的页数
        :param src: 图片
        :return:
        """
        connent = self.load_proxy(self.param['url'])
        goodsArr = self.get_goods_info(connent)
        self.insert_goods_sql(mysql_db, goodsArr)
        self.param['page_count'] = self.param['page_count'] + 1
        proxy_index = 0
        if self.param['page_num'] > 1:
            for i in range(1, self.param['page_num']):
                time.sleep(30)
                print "正在进入第", self.param['page_count'], '页'
                print self.param['url'],str(i * 60)

                while proxy_index == 0:
                    contect = self.load_proxy(self.param['url'] + str(i * 60))
                    if contect != '':
                        proxy_index = 1

                goodsArr = self.get_goods_info(contect)
                self.insert_goods_sql(mysql_db, goodsArr)
                self.param['page_count'] = self.param['page_count'] + 1

        self.stop()
        return True

    def get_goods_info(self, goodsInfoBoday):
        """
        获取商品信息
        :param goodsInfoBoday: 商品详情页面
        :return: 商品详细信息集合
        """
        soup = BeautifulSoup(goodsInfoBoday, "lxml")
        name_list = soup.select('p[class=productTitle] > a')  # 商品名称
        goodsname_list = []
        for name in name_list:
            p_name = name['title']
            goodsname_list.append(p_name)

        img_list = soup.select('div[class=productImg-wrap] > a[class=productImg] > img')  # 商品img
        goodsimg_list = []
        for img in img_list:
            # img_path = unicode("F:/python/img/白酒/",'utf-8')
            try:
                imgname = 'https:' + img['src']  # 图片名
            except KeyError:
                imgname = 'https:' + img['data-ks-lazyload']  # 图片名
            # dowpath = os.path.join(img_path, imgname)

            goodsimg_list.append(imgname)
            # load.save_img(img_path,img['src'])

        price_list = soup.select('p[class=productPrice] > em')  # 商品价格
        goodsprice_list = []
        for price in price_list:
            goodsprice_list.append(price['title'])

        sale_list = soup.select('p[class=productStatus] > span > em')  # 商品销量
        goodssale_list = []
        for sale in sale_list:
            goodssale_list.append(sale.get_text().strip())

        comment_num_list = soup.select('p[class=productStatus] > span > a')  # 商品评论
        goods_comment_num_list = []
        for comment in comment_num_list:
            goods_comment_num_list.append(comment.get_text().strip())

        url_list = soup.select('div[class=productImg-wrap] > a[class=productImg]')  # 商品img
        goodsurl_list = []
        for url in url_list:
            url_link = 'https:' + url['href']  # 图片名
            goodsurl_list.append(url_link)

        shop_list = soup.select('div[class=productShop] > a[class=productShop-name] ')  # 商品店铺
        goodsshop_list = []
        for shop in shop_list:
            goodsshop_list.append(shop.get_text().strip())

        goodsArr = {
            'goods_name': goodsname_list,
            'goods_img': goodsimg_list,
            'goods_price': goodsprice_list,
            'goods_sale': goodssale_list,
            'goods_comment_num': goods_comment_num_list,
            'goods_url': goodsurl_list,
            'goods_pcate': "浓香",
            'goods_shop': goodsshop_list,
            'goods_sql_addtime': unicode(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), "utf-8"),
        }

        return goodsArr


    def insert_goods_sql(self, Ant, goodsArr):
        """
        添加爬虫爬取的商品数据
        :param Ant: 实例化的peewee表对象
        :param goodsArr: 获取的商品集合
        :param self.param['goods_count']: 商品的个数
        :return: self.param['goods_count'] 商品的个数
        """
        print goodsArr['goods_name']
        print goodsArr['goods_img']
        print goodsArr['goods_price']
        print goodsArr['goods_sale']
        print goodsArr['goods_url']
        print goodsArr['goods_comment_num']
        print goodsArr['goods_shop']

        for (name, img, price, sale, url,comment_num,shop) in zip(goodsArr['goods_name'], goodsArr['goods_img'], goodsArr['goods_price'],
                                                 goodsArr['goods_sale'], goodsArr['goods_url'],goodsArr['goods_comment_num'],goodsArr['goods_shop']):
            print '正在获取第 ', str(self.param['goods_count']), ' 件商品的信息： 商品名称- ', name

            Ant.create(
                goods_name=name,
                goods_img=img,
                goods_price=price,
                goods_sale=sale,
                goods_url=url,
                goods_pcate=goodsArr['goods_pcate'],
                goods_comment_num=comment_num,
                goods_shop=shop,
                goods_sql_addtime=goodsArr['goods_sql_addtime']
            )
            self.param['goods_count'] = self.param['goods_count'] + 1

    def proxy_set(self, proxy={}, status=False):
        """
        设置代理IP
        :param proxy:手动代理IP
        :return: 代理IP
        """
        if status == True:
            IP = IpSpider.IPSpider()
            ip_addr = IP.ip
        elif not proxy:
            IP = IpSpider.IPSpider()
            ip_addr = IP.ip
        else:
            ip_addr = proxy
        self.proxy = ip_addr

    def stop(self):
        """
        关闭爬虫
        :return:
        """
        print "感谢您的使用："
        print "- 爬虫停止工作，请重新启动爬虫 - JdSpider"
        pass



