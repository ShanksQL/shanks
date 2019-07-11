# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/6/28 10:36 AM'

import logging
import pickle
import hashlib
import json
import redis


class RedisServer(object):

    def __init__(self):
        _redis_address = 'redis://127.0.0.1:6379'
        logging.info('init redis with {}'.format(_redis_address))
        self.r = redis.StrictRedis.from_url(_redis_address)

    def set_key(self, key, value):
        return self.r.set(key, value)

    def get_key(self, key):
        return self.r.get(key)

    def get_keys(self, key):
        return self.r.keys(key)

    def set_key_expire(self, key, seconds):
        return self.r.expire(key, seconds)

    def set_obj(self, key, obj):
        _obj_s = pickle.dumps(obj)
        return self.r.set(key, _obj_s)

    def get_obj(self, key):
        _obj_s = self.r.get(key)
        if _obj_s is None:
            return None
        else:
            try:
                return pickle.loads(_obj_s)
            except Exception as e:
                logging.error('======>>>>>error:{}'.format(e))
                return None

    def set_obj_expire(self, key, seconds):
        return self.r.expire(key, seconds)

    def set_json(self, key, _json):
        _json_s = json.dumps(_json)
        return self.r.set(key, _json_s)

    def get_json(self, key):
        _obj_s = self.r.get(key)
        if _obj_s is None:
            return None
        else:
            return json.loads(_obj_s)

    def mget_json(self, keys):
        _obj_s = self.r.mget(keys)
        return [None if _obj is None else json.loads(_obj) for _obj in _obj_s]

    def set_list(self, key, _data):
        _json_s = json.dumps({
            'list': _data
        })
        return self.r.set(key, _json_s)

    def get_list(self, key):
        _obj_s = self.r.get(key)
        if _obj_s is None:
            return None
        else:
            return json.loads(_obj_s).get('list')

    def set_json_expire(self, key, seconds):
        return self.r.expire(key, seconds)

    def get_obj_key(self, _key_obj):
        _key = str(hashlib.md5(json.dumps(_key_obj)).hexdigest())
        return self.get_key(_key)

    def set_obj_key(self, _key_obj, _obj):
        _key = str(hashlib.md5(json.dumps(_key_obj)).hexdigest())
        return self.r.set(_key, _obj)

    def set_obj_key_expire(self, _key_obj, seconds):
        _key = str(hashlib.md5(json.dumps(_key_obj)).hexdigest())
        return self.r.expire(_key, seconds)

    def del_key(self, _key):
        self.r.delete(_key)

    def del_obj_key(self, _key_obj):
        _key = str(hashlib.md5(json.dumps(_key_obj)).hexdigest())
        self.r.delete(_key)

