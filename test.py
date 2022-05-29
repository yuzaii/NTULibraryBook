import time

import requests

from Tools import identdict

# s="{data: '75bad476e35b8827e55e1fedf1bd4589',time: '1653809731312',enc: '4589C22A239522A298A61C0D41D87F82',displayName:'周良宇',userRole:'3',group1:'',mobilePhone:''}"
# d = eval(s, identdict())
# print(d)

# all_id_res=requests.get("http://office.chaoxing.com/data/apps/seat/room/list?time=&cpage=1&pageSize=100&firstLevelName=&secondLevelName=&thirdLevelName=&deptIdEnc=")
# print(all_id_res.json())
todaydate = time.strftime("%Y-%m-%d", time.localtime())
while True:

    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(nowtime)
    if nowtime == todaydate + " " + "21:06:20":
        print("okkkk")
        break
