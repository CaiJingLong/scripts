# 生成假的数据库备份文件，以便于截图使用

import os
import datetime
import random

dir = "~/backup"

os.chdir(dir)


def make_file_with_dt(date: datetime.datetime, days: int):
    dt_str = date.strftime("%Y-%m-%d")
    prefix = "fake-database-backup"
    name = "%s-%s.sql.gz" % (prefix, dt_str)
    cmd = 'dd if=/dev/zero of="%s" bs=%dM seek=%d count=0' % (name, 5, 730 + days + 1)
    print(cmd)
    os.system(cmd)

    # 文件名转换为时间戳，文件名格式都是 2021-07-01
    timeStamp = int(date.timestamp())

    # 修改文件的时间戳，随机添加 80到100分钟不等
    timeStamp += 60 * 80 + random.randint(0, 20) * 60

    os.utime(os.path.join(dir, name), (timeStamp, timeStamp))


# 日期开始时间，结束时间

start_dt = datetime.datetime(2023, 6, 1)
end_dt = datetime.datetime.now()

day = 0
while True:
    dt = start_dt + datetime.timedelta(days=day)
    if dt > end_dt:
        break
    make_file_with_dt(dt, day)
    day += 1
