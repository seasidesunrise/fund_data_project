import datetime
import os
import re
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
parentPath = os.path.split(curPath)[0]
rootPath = os.path.split(parentPath)[0]
sys.path.append(rootPath)

import requests
from sqlalchemy import *
from sqlalchemy.orm import *

from src import FundDataDict
from src.funddata import FundData


## 根据fundcode列表，从天天基金抓取所有历史净值数据，并dump到对应的mysql表，表名：fund_{fundcode}
## 如果已经存在表，或表中已经存在净值记录，dump操作会执行update。
##
## TODO: 后续需要补充，是否是指数型基金、如果是指数基金，update对应交易日的TTM估值数据
##
def main():
    # 初始化数据库连接
    engine = create_engine("mysql+pymysql://root:123321@localhost:3306/fund_analysis", encoding='utf-8')

    fundcode_list = get_focused_fund_pool(engine)
    print(fundcode_list)

    for fundcode in fundcode_list:
        do_job(engine, fundcode)


def do_job(engine, fundcode):
    # 创建DBSession类型
    DBSession = sessionmaker(bind=engine)
    # 创建session对象
    session = DBSession()

    last_update_time = get_last_update_time(engine, fundcode)
    print(last_update_time)
    total_page = -1
    page = 1
    current_date = ''

    cond = True
    while cond:
        # http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=160220&per=20&page=1
        url = 'http://fund.eastmoney.com/f10/F10DataApi.aspx?type=lsjz&code=' + fundcode + '&per=20&page=' + str(page)
        print(url)

        resp = requests.get(url)
        html_fund_value = resp.text
        # print(resp.text)
        tr_re = re.compile(r'<tr>(.*?)</tr>')
        item_re = re.compile(
            r'''<td>(\d{4}-\d{2}-\d{2})</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td><td.*?>(.*?)</td>''',
            re.X)
        totalpage_re = re.compile(r'pages:(\d*),curpage')
        total_page = int(totalpage_re.search(html_fund_value).group(1))

        tablename = 'fund_' + fundcode
        FundData.FundData.__table__.name = tablename
        create_table_if_not_exist(engine, tablename)
        strtoday = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')

        for line in tr_re.findall(html_fund_value):
            print(line)
            match = item_re.match(line)
            if not match:
                continue
            entry = match.groups()
            print(entry)
            date = entry[0]
            dwjz = entry[1]
            ljjz = entry[2]
            rzzl = entry[3]
            buystatus = entry[4]
            salestatus = entry[5]
            fenhong = entry[6]

            # 使用原生sql，解决session.merge重复主键的问题
            tmpsql = "replace into " + tablename + "(fundcode, `date`, dwjz,ljjz, rzzl," \
                                                   "buystatus, salestatus, fenhong, is_index, pe, " \
                                                   "`lastmodified`) values ('" + fundcode + "'" \
                                                   ", '" + date + "'" \
                                                   ", '" + dwjz + "'" \
                                                   ", '" + ljjz + "'" \
                                                   ", '" + rzzl + "'" \
                                                   ", '" + buystatus + "'" \
                                                   ", '" + salestatus + "'" \
                                                   ", '" + fenhong + "'" \
                                                   ", 0" \
                                                   ", 0" \
                                                   ", '" + strtoday + "'" \
                                                   ")"
            print(tmpsql)
            # tmpFundData = FundData.FundData(fundcode, date, dwjz, ljjz, rzzl,
            #                                 buystatus, salestatus, fenhong, 0, 0,
            #                                 strtoday)
            # # 添加到session:
            # session.merge(tmpFundData)
            session.execute(tmpsql)
            current_date = date

            if page == 1 and current_date < last_update_time:
                cond = False
                break

        session.commit()
        if page > total_page:
            break
        page += 1

    tmpKv = FundDataDict.FundDataDict(key=fundcode, value=strtoday)
    session.merge(tmpKv)
    session.commit()
    session.close()


def create_table_if_not_exist(engine, tablename):
    # 绑定元信息
    metadata = MetaData(engine)
    # 创建表格，初始化数据库
    fund_table = Table(tablename, metadata,
                       Column('fundcode', String(255), comment='基金代码'),
                       Column('date', String(255), primary_key=True, comment='日期'),
                       Column('dwjz', String(255), comment='单位净值'),
                       Column('ljjz', String(255), comment='累计净值'),
                       Column('rzzl', String(255), comment='日增长率'),

                       Column('buystatus', String(255), comment='购买状态'),
                       Column('salestatus', String(255), comment='赎回状态'),
                       Column('fenhong', String(255), comment='分红配送'),
                       Column('is_index', Integer(), comment='是否指数基金，1是 0否'),
                       Column('pe', Float(), comment='如果是指数基金，则该列为对应的PE-TTM'),

                       Column('lastmodified', String(255), comment='最后修改时间')
                       )
    # 创建数据表，如果数据表存在则忽视！！！
    metadata.create_all(engine)


def get_last_update_time(engine, fundcode):
    sql = "select * from fund_data_dict where `key`='" + fundcode + "'"
    result = engine.execute(sql)
    rowCount = result.rowcount
    if rowCount > 0:
        for data in result:
            print(data)
            return str(data[1])
    else:
        return ""
    return ""


def get_focused_fund_pool(engine):
    sql = "select * from focused_fund_pool where `status`=1"
    result = engine.execute(sql)
    fundlist = []
    for data in result:
        fundlist.append(data[0])

    return fundlist


if __name__ == '__main__':
    main()
