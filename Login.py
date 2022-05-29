import re
import time

import requests,sys
#用于执行统一身份认证用来加密明文密码的js脚本
import execjs
#用来进行xpath定位网页的部分内容
from lxml import etree

from Tools import identdict


def LibraryBook(user_info):     #利用统一身份认证，返回票据
    # 先获取用户信息和
    print(user_info)
    todaydate=time.strftime("%Y-%m-%d", time.localtime())
    print("当前日期:"+todaydate)
    startTime=user_info['startTime']
    endTime=user_info['endTime']


    session=requests.session()
    login_url='https://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas/ntu/index'

    #利用get取网页中的stal，lt,execution,
    thpage_text=session.get(login_url).text
    staltree = etree.HTML(thpage_text)
    print("正在登陆统一认证平台。。。")
    thstal=staltree.xpath('//*[@id="pwdDefaultEncryptSalt"]/@value')
    thlt=staltree.xpath('//*[@id="casLoginForm"]/input[1]/@value')
    thexecution=staltree.xpath('//*[@id="casLoginForm"]/input[3]/@value')
    encrypt_script_url = 'http://authserver.ntu.edu.cn/authserver/custom/js/encrypt.js'
    js = requests.get(encrypt_script_url).text
    ctx = execjs.compile(js)
    password = ctx.call('_ep', user_info['password'], thstal[0])
    # print(thstal[0])
    # print(thlt[0])
    # print(thexecution[0])
    # print(password)
    # print('------p2------')
    longin_data={
        'username':user_info['username'],
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

    # 到预约界面
    # res4=session.get("http://office.chaoxing.com/front/third/apps/seat/index")
    # # print(res4.text)

    # 获取pagetoken 这个玩意下面需要的
    get_pagetoken_res=session.get("http://office.chaoxing.com/front/third/apps/seat/list?deptIdEnc= ")
    # print(get_pagetoken_res.text)
    pagetoken=re.findall(r"&pageToken='?.*'", get_pagetoken_res.text)[0][16:-14]
    print("pagetoken:"+pagetoken)
    # print(pagetoken[0][16:-14])

    # 获取角色信息 不知道有没有用
    role_res=session.get("http://office.chaoxing.com/data/apps/seat/person/role")
    # print(role_res.text)
    #
    # 获取南通大学所有图书馆的所有能预约的房间列表id信息 并且根据用户所填的寻找相对应的信息   roomid
    all_id_res=session.get("http://office.chaoxing.com/data/apps/seat/room/list?time=&cpage=1&pageSize=100&firstLevelName=&secondLevelName=&thirdLevelName=&deptIdEnc= ")
    # print(all_id_res.json())
    all_id=all_id_res.json()
    for i in all_id['data']['seatRoomList']:
        # print(i['firstLevelName'])
        if i['firstLevelName']==user_info['campus']:
            if i['secondLevelName']==user_info['floor']:
                if i['thirdLevelName']==user_info['room']:
                    room_id=str(i['id'])



    #获取最后一步的token
    get_token_res=session.get("http://office.chaoxing.com/front/third/apps/seat/select?id="+room_id+"&day="+todaydate+"&backLevel=2&pageToken="+pagetoken+"&fidEnc=")
    # print(get_token_res.text)
    token = re.findall(r"token: '?.*", get_token_res.text)[0][8:-2]
    print("token:"+token)

    # 获取座位信息？
    # res6=session.get("http://office.chaoxing.com/data/apps/seat/room/info?id=6867&toDay=2022-05-29")
    res6=session.get("http://office.chaoxing.com/data/apps/seat/seatgrid/roomid?roomId="+room_id)
    # print(res6.text)
    #
    #获取在用户所预约时间段这个房间已经被选的座位
    res7=session.get("http://office.chaoxing.com/data/apps/seat/getusedseatnums?roomId="+room_id+"&startTime="+startTime+"&endTime="+endTime+"&day="+todaydate)
    print(res7.text)


    # # 最终的提交
    # submit_res = session.get(
    #     "http://office.chaoxing.com/data/apps/seat/submit?roomId=" + room_id + "&startTime=" + startTime + "&endTime=" + endTime + "&day=" + todaydate + "&seatNum=" +
    #     user_info['seatNum'] + "&captcha=&token=" + token)
    #
    # submit_info = submit_res.json()
    # # print(submit_info)
    # # print(submit_info['success'])
    # if submit_info['success'] == True:
    #     print("恭喜你，预约成功")
    # else:
    #     print(submit_info)
    #
    # print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))



    ##这里要等待当到达早上8：00的时候发生下面的请求
    while True:

        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(nowtime)
        if nowtime == todaydate +" "+"07:00:00":
            # 最终的提交
            submit_res = session.get(
                "http://office.chaoxing.com/data/apps/seat/submit?roomId=" + room_id + "&startTime=" + startTime + "&endTime=" + endTime + "&day=" + todaydate + "&seatNum=" +
                user_info['seatNum'] + "&captcha=&token=" + token)

            submit_info = submit_res.json()
            # print(submit_info)
            if submit_info['success'] == True:
                print("恭喜你，预约成功")
            else:
                print(submit_info)

            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            break








    # # res6=session.get("http://office.chaoxing.com/data/apps/seat/submit?roomId=6867&startTime=16%3A30&endTime=17%3A00&day=2022-05-29")
    # # print(res6.text)
    # return Location_url

###1.超星图书馆登录接口
# https://passport2.chaoxing.com/login?newversion=true&refer=http://office.chaoxing.com/front/third/apps/seat/index

### 2.跳转认证平台（好像可以直接跳转）抓包试试
# https://authserver.ntu.edu.cn/authserver/login?service=http://cv-p.chaoxing.com/login_auth/cas/ntu/index

### 3.登录成功预约接口
# http://office.chaoxing.com/front/third/apps/seat/index

