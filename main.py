from Login import LibraryBook

if __name__ == '__main__':
    user_info={
    "username" : "1930141733",  # 学号
    "password" : "19990303jy",  # 统一认证平台的密码
    "startTime" : "14:0", # 开始时间
    "endTime" : "20:00", # 结束时间
    "campus" : "启东校区", # 校区： 啬园校区 启秀校区 启东校区
    "floor" : "四楼", # 楼层： 二楼 三楼 四楼
    "room" : "403阅览室", # 房间名称： 203阅览室 303阅览室 403阅览室 四楼大厅
    "seatNum" : "068", # 座位号： 000-999 自己看
    }
    LibraryBook(user_info)

