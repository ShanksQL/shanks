# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/6/11 3:23 PM'

import logging
import sys
from environment import environment
from db.base_model import Base
from sqlalchemy import MetaData
from sqlalchemy.schema import CreateTable, CreateColumn


class AdjustTableStructure(object):
    def __init__(self):
        pass

    @staticmethod
    def adjust_table():
        environment.initialize(sys.argv[1:])
        env = environment
        code_tables = Base.metadata.sorted_tables

        meta = MetaData()
        meta.reflect(bind=env.engine)
        db_tables = meta.sorted_tables
        db_tables_map = {}
        for t2 in db_tables:
            db_tables_map[str(t2)] = t2

        no_tables_list = []

        logging.info("\n\n\n")

        add_column_list = []

        for t1 in code_tables:
            # print "alter table "+str(t1)+" engine=InnoDB;"
            if str(t1) not in db_tables_map.keys():
                no_tables_list.append(t1)
            else:
                db_table = db_tables_map[t1.name]
                db_table_column_map = {}
                for c in db_table.c:
                    db_table_column_map[c.name] = c
                for c in t1.c:
                    if c.name not in db_table_column_map.keys():
                        add_column_list.append(c)

        # print add_column_list

        logging.info(no_tables_list)
        for no_table in no_tables_list:
            no_table.mysql_engine = "InnoDB"
            logging.info(CreateTable(no_table))
            no_table.create(env.engine)
            sql = "alter table " + no_table.name + " engine=InnoDB"
            env.engine.execute(sql)

        for column in add_column_list:
            # print CreateColumn(column)
            sql = "alter table " + column.table.name + " add " + str(CreateColumn(column)) + " ;"
            env.engine.execute(sql)
            logging.info(sql)

        logging.info("complete")


def main():
    AdjustTableStructure().adjust_table()


if __name__ == '__main__':
    main()
