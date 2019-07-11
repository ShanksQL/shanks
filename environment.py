# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/6/11 9:31 AM'

import threading
import importlib
import inspect
import pkgutil
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool
from sqlalchemy.ext.horizontal_shard import ShardedSession
from sqlalchemy.orm import sessionmaker, scoped_session
import re

mu = threading.Lock()


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        def create_new(*new_args, **new_kwargs):
            if mu.acquire():
                if cls not in instances:
                    instances[cls] = cls(*new_args, **new_kwargs)
                mu.release()
                return instances[cls]

        if cls not in instances:
            return create_new(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class Environment(object):
    def initialize(self, args=None):
        if self.__is_inited__:
            return
        self._init_config_(args)
        self._init_db_()
        self._init_redis_()
        self.import_all_models()
        self._add_event()
        self.db.remove()

    def _init_db_(self):

        def _get_session(path):
            path = clean_db_path(path)
            return create_engine(
                path, convert_unicode=True,
                echo=False, poolclass=QueuePool, pool_size=200,
                pool_recycle=100
            )

        _db_path = self.conf.get_conf('db', 'path')
        logging.info('init default db with {}'.format(_db_path))
        self._shards = {
            'default': _get_session(_db_path)
        }
        _shard_list = self.conf.get_conf('db', 'shard_list')
        self._shard_regex = []
        if _shard_list and _shard_list != '':
            for _s in _shard_list.split(','):
                _path = self.conf.get_conf('shard_{}'.format(_s), 'path') or _db_path
                if _path:
                    logging.info('init {} db with {}'.format(_s, _path))
                    self._shards[_s] = _get_session(_path)
                _regex = self.conf.get_conf('shard_{}'.format(_s), 'regex')
                if _regex and _regex != '':
                    self._shard_regex.append(
                        (re.compile('|'.join(map(lambda x: '^{}$'.format(x), _regex.split(',')))), _s))

        _session = sessionmaker(class_=ShardedSession, expire_on_commit=False)
        _session.configure(
            shards=self._shards,
            shard_chooser=_shard_chooser,
            id_chooser=_id_chooser,
            query_chooser=_query_chooser
        )
        self.d = scoped_session(_session)
        self.e = self._shards['default']

    def import_all_models(self):
        _classes = []
        apps = self.get_conf('core_apps')
        for key, value in apps:
            # print "import"+value
            _classes += self.import_models_by_app(value)

    @staticmethod
    def import_models_by_app(app_name):
        _classes = []
        _app = importlib.import_module(app_name)
        _modules = [importlib.import_module(app_name + "." + _m_name) for _m_name in
                    iter_all_modules(_app.__path__[0]) if
                    _m_name.split(".")[len(_m_name.split(".")) - 1].startswith("model")]
        for _module in _modules:
            _classes += [_cls for _n, _cls in inspect.getmembers(_module, inspect.isclass)]
        return _classes


def _shard_chooser(mapper, instance, clause=None):
    _tablename = ''
    if instance:
        _tablename = instance.__tablename__
    if mapper:
        _tablename = mapper.class_.__tablename__

    if _tablename == '' and clause is not None:
        if hasattr(clause, 'table'):
            _tablename = clause.table.name
        else:
            import core.ds.sharding.SqlUtil
            _tablename = core.ds.sharding.SqlUtil.getTabNameShortName(clause.text)

    return environment.get_shard_from_table(_tablename)


def _id_chooser(query):
    return _query_chooser(query)


def _query_chooser(query):
    mappers = query._mapper_adapter_map.values()
    _table_name = mappers[0][0].class_.__tablename__
    return [environment.get_shard_from_table(_table_name)]


def clean_db_path(_db_path):
    return _db_path if "charset" in _db_path else _db_path + "?charset=utf8"


def iter_all_modules(package, prefix=''):
    """
    获取某package下所有module列表(深度遍历)
    :param package,
    :param prefix
    """
    if type(package) is not str:
        path, prefix = package.__path__[0], package.__name__ + '.'
    else:
        path = package
    for _, name, is_package in pkgutil.iter_modules([path]):
        if is_package:
            for m in iter_all_modules(os.path.join(path, name), prefix=name + '.'):
                yield prefix + m
        else:
            yield prefix + name


environment = Environment()
