# _*_ coding: utf-8 _*_

import xlwt
import logging
import os
import sys
import shutil
from datetime import datetime

abspath = os.path.abspath(__file__)
dirname = os.path.dirname(abspath)
code_path = dirname + r'\code'
sys.path.append(code_path)

from my_sql import MySql
from db_update import db_update
from kun_ming_week import kun_ming_week
from zhong_zhi_week import zhong_zhi_week
from ji_gou_week import ji_gou_week

logging.disable(logging.NOTSET)
logging.basicConfig(level = logging.DEBUG, format = ' %(asctime)s | %(levelname)s | %(message)s' )

# ******主程序开始******

def main():

    logging.debug("……程序开始运行……")
        
    # 建立数据库连接
    sql = MySql(r"Data\data.db")
    logging.debug("数据库连接成功")
    
    # 更新数据库，数据库更新完毕后将原始数据文件进行备份
    # 同时避免多次无意义的更新数据库
    table_name = "昆明机构周报.xlsx"
    if os.path.isfile(table_name):
        db_update(table_name, sql)
        backup_path = dirname + r"\Backup"
        backup_name = backup_path +"\\" + table_name[:-5] + datetime.today().strftime("%Y%m%d") + ".xlsx"
        shutil.copyfile(table_name, backup_name)
        os.remove(table_name)
    
    # 建立Excel工作簿
    book = xlwt.Workbook(encoding = "utf-8")

    ## 添加昆明机构周报工作表
    #kun_ming = book.add_sheet("昆明机构周报")
    
    #logging.debug("开始写入昆明机构周报表")
    ## 将数据写入昆明机构周报工作表
    #kun_ming_week(kun_ming, sql, "车险", 1)
    #kun_ming_week(kun_ming, sql, "人身险", 2)
    #kun_ming_week(kun_ming, sql, "财产险", 3)
    #logging.debug("昆明机构周报表写入完成")

    # 添加三级机构周报工作表
    zhong_zhj = book.add_sheet("三级机构周报")

    logging.debug("开始写入三级机构周报表")
    # 将数据写入三级机构周报表
    zhong_zhi_week(zhong_zhj, sql)
    logging.debug("三级机构周报表写入完成")

    # 添加四级机构周报工作表
    ji_gou = book.add_sheet("四级机构周报")

    logging.debug("开始写入四级机构周报表")
    # 将数据写入四级机构周报表
    ji_gou_week(ji_gou, sql)
    logging.debug("四级机构周报表写入完成")
    
    # 保存数据至Excel工作表中
    book.save("数据统计表.xlsx")

    # 关闭数据库
    sql.closs()
    logging.debug("数据库关闭")
    logging.debug("……程序运行结束……")

# ******启动方式判断******

if __name__ == '__main__':
    main()


