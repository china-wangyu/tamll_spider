# _*_ coding:utf-8 _*_

"""
date : 2017-6-17 14:55
auth : 青雉
version : 1.1
"""

import Tmall_spider, Tmall_mysql, Tmall_load

if __name__ == '__main__':

    Tmall_Mysql = Tmall_mysql.TmallMysql()
    Tmall_Model = Tmall_Mysql.Table()
    loads = Tmall_load.Load()
    num = int(raw_input("请输入您想爬取的页数："))
    if num == '':
        num = int(raw_input("请重新输入您想爬取的页数："))

    """茶
                # https://list.tmall.com/search_product.htm?cat=50099891&q=%B2%E8&prop=1626691:20477&sort=d&style=g&search_condition=23&industryCatId=50099956&s=    绿茶/龙井/碧螺春
                # https://list.tmall.com/search_product.htm?cat=50072599&q=%B2%E8&prop=1626691:20477&sort=d&style=g&search_condition=23&from=sn_1_prop&industryCatId=50099956&s=    普洱茶/茶饼/茶砖
                # https://list.tmall.com/search_product.htm?cat=50072577&q=%B2%E8&prop=1626691:20477&sort=d&style=g&from=sn_1_prop&industryCatId=50099956&s=    乌龙茶/铁观音/大红袍
                # https://list.tmall.com/search_product.htm?cat=50099914&q=%B2%E8&prop=1626691:20477&sort=d&style=g&search_condition=23&from=sn_1_prop&industryCatId=50099956&s=    红茶/正山小种/祁红
                # https://list.tmall.com/search_product.htm?cat=50099956&q=%B2%E8&prop=1626691:20477&sort=d&style=g&from=sn_1_cat-qp&industryCatId=50099956&s=   花茶/果茶/加工茶
                # https://list.tmall.com/search_product.htm?cat=50099926&q=%B2%E8&prop=1626691:20477&sort=d&style=g&search_condition=23&from=sn_1_prop&industryCatId=50099956&s=    黑茶/白茶/黄茶
                """

    """ 白酒
    # https://list.tmall.com/search_product.htm?cat=50105161&q=%B0%D7%BE%C6&prop=1626691:20477&sort=d&style=g&from=sn_1_cat-qp&s=   浓香
    # https://list.tmall.com/search_product.htm?cat=50105160&q=%B0%D7%BE%C6&prop=6939376:20477&sort=d&style=g&search_condition=23&from=sn_1_prop&industryCatId=50105161&s=  酱香

    """
    param = {
        "url": "https://list.tmall.com/search_product.htm?cat=50105161&q=%B0%D7%BE%C6&prop=1626691:20477&sort=d&style=g&from=sn_1_cat-qp&s=",



        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"
        },
        "page_num": num,
        "goods_count": 1,
        "page_count": 1
    }


    Tmall = Tmall_spider.TmallSpider(Tmall_Model, param)
    print "您爬取的网址是：%s" % Tmall.param['url']
    print "您设置的页数是：%s" % Tmall.param['page_num']
    print "您爬取的页数是：%s" % str(Tmall.param['page_count'] -1)
    print "您爬取的商品数是：%s" % str(Tmall.param['goods_count'] -1)
