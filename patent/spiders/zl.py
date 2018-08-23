# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashFormRequest

from patent.items import ZlItem


class ZlSpider(scrapy.Spider):
    name = 'zl'

    def start_requests(self):
        start_url = 'http://epub.sipo.gov.cn/patentoutline.action'

        for pn in range(1,4):
            fd = self.formdata(pn)
        # fd = {
        #     "strWhere":"OPD=BETWEEN['1985.01.01','2018.07.20']",
        #     'pageNow':'2' #这个地方不能用int类型
        # }
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Cookie': '_gscu_7281245=32008863jy5s3b13; WEB=20111130; JSESSIONID=EF9ADE3F72584F01DC4F98126CAE6C7E; Hm_lvt_06635991e58cd892f536626ef17b3348=1532008864,1532065540; _gscbrs_7281245=1; TY_SESSION_ID=ae948647-7750-4648-8425-6b1b93f844af; Hm_lpvt_06635991e58cd892f536626ef17b3348=1532065585; _gscs_7281245=32065539bdqdkx10|pv:3'
        }

            yield scrapy.FormRequest(url=start_url,formdata=fd,headers=headers,callback=self.parse)

    def formdata(self,pageNum):
        return {
            "strWhere": "OPD=BETWEEN['1985.01.01','2018.07.20']",
            'pageNow': '{}'.format(pageNum)  # 这个地方不能用int类型
        }

    def parse(self, response):
        #专利名称
        title = response.xpath("//h1")
        #申请公布号
        openNo = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[1]')
        #申请公布日
        openDate = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[2]')
        #申请号
        applyNo = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[3]')
        #申请日
        applyDate= response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[4]')
        #申请人
        applyPeople = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[5]')
        #发明人
        inventor = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[6]')
        #地址
        address = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[8]')
        #分类号
        classifyNo = response.xpath('//div[@class="cp_box"]/div[@class="cp_linr"]/ul/li[9]')
        #摘要
        summery = response.xpath('//div[@class="cp_box"]/div/div[@class="cp_jsh"]')
        #二维码
        qrcodeurls = response.xpath('//div[@class="cp_box"]/a/img/@src')
        #缩略图
        thumb = response.xpath('//div[@class="cp_box"]/div[@class="cp_img"]/img/@src')

        baseUrl = 'http://epub.sipo.gov.cn/'
        for ti,on,od,an,ad,ap,inv,add,cf,su,qr,th in zip(title,openNo,openDate,applyNo,applyDate,applyPeople,inventor,address,classifyNo,summery,qrcodeurls,thumb):
            item = ZlItem()
            item['title'] = ti.xpath("string(.)").extract_first().strip().split()[1]
            item['openNo']= on.xpath("string(.)").extract_first()[6:]
            item['openDate']=od.xpath("string(.)").extract_first()[6:]
            item['applyNo']=an.xpath("string(.)").extract_first()[5:]
            item['applyDate']=ad.xpath("string(.)").extract_first()[4:]
            item['applyPeople']=ap.xpath("string(.)").extract_first()[4:]
            item['inventor']=''.join(inv.xpath("string(.)").extract_first()[4:].strip().split())
            item['address']=add.xpath("string(.)").extract_first()[3:]
            item['classifyNo']=cf.xpath("string(.)").extract_first().split()[0][4:]
            item['summery']=su.xpath("string(.)").extract_first().split()[1]
            item['qrcodeurls']=baseUrl + qr.extract()
            item['thumb']=baseUrl + th.extract()

            yield item

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            }
            yield SplashFormRequest(url='http://epub.sipo.gov.cn/pam.action',callback=self.downparse,method='POST',args={
                'wait':5},formdata={
                "strWhere":"PN='"+"{}".format(on.xpath("string(.)").extract_first()[6:])+"'",
                "strSources":"pip"
            },headers=headers)

    def downparse(self,response):
        item = DownurlItem()
        item['downurl'] = response.xpath('//div[@class="main"]//ul/li[last()]/a/@href').extract_first()
        item['applyNo'] = response.xpath('//title/text()').extract_first()[4:]

        yield item

