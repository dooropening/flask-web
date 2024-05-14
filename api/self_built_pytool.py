import json
import os.path
import functools
import threading
import time


def json_write(file_path, file_name, data):

    """
    :param file_name:
    :param file_path: the path you want to store
    :param data: the data you want to store
    :return: none
    """

    path = os.path.join(file_path, file_name + '.json')
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def json_read(file_path):

    """
    :param file_path: the file you want to get
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data


def time_delay(seconds):
    """
    延迟特定秒数执行装饰器
    """
    def wrapper(func):
        @functools.wraps(func)
        def wrapper_func(*args, **kwargs):
            # 创建一个线程，在指定的延迟后执行函数
            def delayed_execution():
                time.sleep(seconds)  # 等待指定的时间
                return func(*args, **kwargs)

            # 在新线程中执行延迟函数
            threading.Thread(target=delayed_execution).start()

        return wrapper_func

    return wrapper


def check_print(s):
    print(type(s))
    print(len(s))
