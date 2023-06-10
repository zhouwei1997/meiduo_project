# -*- coding: utf-8 -*- 
# @Time : 2023/6/10 10:41 
# @Author : 世间无事人
# @File : tests.py 
# @description :

from fdfs_client.client import Fdfs_client, get_tracker_conf

tracker_conf = get_tracker_conf('client.conf')
print(tracker_conf)
client = Fdfs_client(tracker_conf)

# 文件上传
result = client.upload_by_filename('C:/Users/Administor/Desktop/微信截图_20230610103246.png')
print(result)
