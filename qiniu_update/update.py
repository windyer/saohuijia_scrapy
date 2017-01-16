# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config
import urllib
import os
import time
def update(key,localfile):
    #需要填写你的 Access Key 和 Secret Key
    access_key = '-gt4mkC_zjqqWDxw3iiVp3jCqNleih5CMsBRswLZ'
    secret_key = '0F6B4TrDFa1nNe6jk2sL6TiF6LbNBhP0A22Wqhox'

    #构建鉴权对象
    q = Auth(access_key, secret_key)

    #要上传的空间
    bucket_name = 'news-hb'

    #上传到七牛后保存的文件名
    key = key

    #生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    #要上传文件的本地路径
    localfile = localfile

    ret, info = put_file(token, key, localfile)
    print info
    print ret
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
def load(image,localfile):
    try:
        os.mkdir(localfile)
    except:
        pass
    name = int(time.time())
    name_type = image.split('.')[-1]
    if len(name_type) >3 :
	name_type = "jpg"
    path = localfile+"/{0}.{1}".format(name,name_type)
    urllib.urlretrieve(image,path)
    update(path,path)
    return "http://newsimage.saohuijia.com/"+path
