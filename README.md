# meiduo_project

美多商城

[TOC]

# 项目前准备

## 创建美多商城项目目录

~~~shell
django-admin startproject meiduo_mall
~~~

## 设置settings文件

在项目中新建settings的包，新建`dev.py`作为开发环境的settings文件。修改配置文件`manage.py`，将配置文件的位置指向`dev.py`

![image-20220723095630793](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207230956951.png)

### 修改dev.py文件

#### 配置时区

在`dev.py`配置文件中指定时区

~~~python
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'
~~~

![image-20220723095740635](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207230957701.png)

#### 配置Redis缓存

~~~python
CACHES = {
    "default": {
        "BACKEND": "django.redis.cache.RedisCache",
        "LOCATION": "redis:127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "zhouwei1997"
        }
    },
    # session
    "session": {
        "BACKEND": "django.redis.cache.RedisCache",
        "LOCATION": "redis:127.0.0.1:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "zhouwei1997"
        }
    },
    # 验证码
    "verify_code": {
        "BACKEND": "django.redis.cache.RedisCache",
        "LOCATION": "redis:127.0.0.1:6379/3",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100},
            "PASSWORD": "zhouwei1997"
        }
    },
}
# 将session保存到其他的库中
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"
~~~

![image-20220723095817774](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207230958853.png)

#### 配置mysql数据库

~~~python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'meiduo',
        'HOST': '127.0.0.1',
        'PORT': 3306,
        'USER': 'root',
        'PASSWORD': 'zhouwei1997'
    }
}
~~~

![image-20220723095855589](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207230958645.png)

#### 配置日志文件

