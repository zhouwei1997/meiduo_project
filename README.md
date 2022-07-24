# meiduo_project

美多商城

[TOC]

# 项目前准备

## 创建美多商城项目目录

~~~shell
django-admin startproject meiduo_mall
~~~

## 新建templates目录并将其作为模板文件

![image-20220723100131406](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231001501.png)

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

在`dev.py`文件中配置数据库的连接信息

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

同时还是需要在过程的`__init__.py`文件中引入数据库的配置信息

~~~python
# 配置mysql数据库
import pymysql

pymysql.install_as_MySQLdb()
~~~

![image-20220723100445741](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231004842.png)

#### 引入jinja2的模板

~~~python
TEMPLATES = [
    # 引入jinja2的模板
    {
        'BACKEND': 'django.template.backends.jinja2.Jinja2',
        # 配置模板文件的加载路径
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            # 补充jinja2模板引擎环境
            'environmemt': 'meiduo_mall.utils.jinja2_env.jinja2_environment'
        },
    },

]
~~~

![image-20220723100304817](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231003941.png)

在项目中新建utils的包，配置jinja2的模板信息`jinja2_env.py`

~~~python 
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def jinja2_environment(**options):
    # 创建环境对象
    env = Environment(**options)
    # 自定义语法：{{ static('静态文件相对路径') }} {{ url('路由的命名空间')}}
    env.globals.update({
        'static': staticfiles_storage.url,  # 获取静态文件的前缀
        'url': reverse  # 反向解析
    })
    # 返回对象
    return env
~~~

![image-20220723100644907](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231006003.png)

#### 配置日志文件

~~~python
# 配置工程日志
current_path = os.path.dirname(os.path.realpath(__file__))  # 当前目录的绝对路径
log_path = os.path.join(os.path.dirname(current_path), '../logs')  # 日志存放目录
if not os.path.exists(log_path): os.mkdir(log_path)  # 若目录不存在则创建
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(os.path.dirname(BASE_DIR), 'logs/meiduo.log'),  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}
~~~

#### 配置静态文件

~~~python
# 指定加载静态文件的路由前缀
STATIC_URL = '/static/'
# 配置静态文件加载路径
STATICFILE_DIRS = [os.path.join(BASE_DIR, 'static')]
~~~

![image-20220723175958894](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231759168.png)

#  用户注册模块

~~~python
# 创建子应用
python manage.py startapp users
~~~

![image-20220723180557034](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231805094.png)

注册用户模块，在`dev.py`中注册

![image-20220723180740585](https://raw.githubusercontent.com/zhouwei1997/Image/master/202207231807669.png)
