import datetime
import json
import os
import sys

curPath = os.path.abspath(os.path.dirname(__file__))
parentPath = os.path.split(curPath)[0]
rootPath = os.path.split(parentPath)[0]
sys.path.append(rootPath)

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.fundlist import Fund
from src import FundDataDict

# 全量基金获取接口：http://fund.eastmoney.com/js/fundcode_search.js
# 执行这个程序：更新全量基金基本信息到fundlist数据库表、并记录最后更新时间到fund_data_dict
#
# crontab: 每天晚上21:34执行定时任务
# 34 21 * * * /usr/local/bin/python3 /Users/seasidesunrise/PycharmProjects/fund_data_project/src/fundlist/SaveOrOverwriteAllFunds.py > /tmp/fundlist.log 2>&1
#
def main(argv):
    url = "http://fund.eastmoney.com/js/fundcode_search.js"
    fundlist_key = "fundlist_last_modified"
    response = requests.get(url)
    all_funds_text = response.text
    all_funds_text = all_funds_text[all_funds_text.find('=') + 2:all_funds_text.rfind(";")]
    all_funds_list = json.loads(all_funds_text)

    strtoday = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M')
    print("date: %s, get %d total fund from ttjj..." % (strtoday, len(all_funds_list)))

    # 初始化数据库连接:
    engine = create_engine("mysql+pymysql://root:123321@localhost:3306/fund_analysis", encoding='utf-8')
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=engine)
    # 创建session对象:
    session = DBSession()

    for fund in all_funds_list:
        fundcode = fund[0]
        fundname_abbr = fund[2]
        fundname_szm = fund[1]
        fundname_quanpin = fund[4]
        fund_type = fund[3]
        # print(fund)
        # 创建新Fund对象:
        tmp_fund = Fund.Fund(fundcode=fundcode, fundname_abbr=fundname_abbr,
                            fundname_szm=fundname_szm, fundname_quanpin=fundname_quanpin,
                            fund_type=fund_type)
        # 添加到session:
        session.merge(tmp_fund)

    tmpKv = FundDataDict.FundDataDict(key=fundlist_key, value=strtoday)
    session.merge(tmpKv)

    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
    print("\nsave all fund infos to db finished, and update lastModified time to db at %s!\n" % strtoday)


if __name__ == "__main__":
    main(sys.argv)
