import re
import requests,sys
#用于执行统一身份认证用来加密明文密码的js脚本
import execjs
#用来进行xpath定位网页的部分内容
from lxml import etree

from Tools import identdict


def loing_authserver_ntu(username,password):     #利用统一身份认证，返回票据
    session=requests.session()
    login_url='https://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas/ntu/index'
    #利用get取网页中的stal，lt,execution,
    thpage_text=session.get(login_url).text
    staltree = etree.HTML(thpage_text)
    thstal=staltree.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')
    thlt=staltree.xpath('//*[@id="casLoginForm"]/input[1]/@value')
    thexecution=staltree.xpath('//*[@id="casLoginForm"]/input[3]/@value')
    encrypt_script_url = 'http://authserver.ntu.edu.cn/authserver/custom/js/encrypt.js'
    js = requests.get(encrypt_script_url).text
    ctx = execjs.compile(js)
    password = ctx.call('_ep', repassword, thstal[0])
    # print(thstal[0])
    # print(thlt[0])
    # print(thexecution[0])
    # print(password)
    # print('------p2------')
    longin_data={
        'username':reusername,
        'password':password,
        'lt':thlt[0],
        'dllt':'userNamePasswordLogin',
        'execution':thexecution[0],
        '_eventId':'submit',
        'rmShown':'1'
    }
    login_res=session.post(login_url,longin_data,allow_redirects=False)
    # print(login_res)
    # print('--------------------')
    try:
        Location_url=login_res.headers['Location']
    except KeyError:
        print('账号密码错误或被要求需要验证码！')
        # LL.log(1,"账号密码错误或被要求需要验证码")
        sys.exit(0)
    # print(backhead)
    print("南通大学统一认证成功，正在跳转超星平台。。。")
    # print(Location_url)
    # 对重定向的地址也就是超星的地址进行请求
    res=session.get(Location_url)

    # 获取js里的data信息
    js_info = re.findall(r'{data: {?.*}', res.text)
    # print(js_info[0])

    # 转js中的信息成字典 留着放入请求头
    params=eval(js_info[0], identdict())
    # print(params)

    res1=session.get(url="http://cv-p.chaoxing.com/login_auth/cas/ntu/login",params=params)
    # print(res1.json())

    res2=session.get(url="https://i.chaoxing.com",allow_redirects=False)
    # print(res2)
    if res2.status_code==302:
        print("超星平台跳转成功")
    # 这里显示302 则表示已经成功 获取超星重定向url
    CX_Location_url = res2.headers['Location']
    print(CX_Location_url)

    # 请求超星重定向url
    res3=session.get(CX_Location_url)
    # print(res3.text)

    res4=session.get("http://office.chaoxing.com/front/third/apps/seat/index")
    print(res4.text)
    return Location_url

###1.超星图书馆登录接口
# https://passport2.chaoxing.com/login?newversion=true&refer=http://office.chaoxing.com/front/third/apps/seat/index

### 2.跳转认证平台（好像可以直接跳转）抓包试试
# https://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas/ntu/index

### 3.登录成功预约接口
# http://office.chaoxing.com/front/third/apps/seat/index

username="" # 学号
password="" #统一认证平台的密码
loing_authserver_ntu(username,password)