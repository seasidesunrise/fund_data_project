import datetime
import json

import requests
from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = "http://fund.eastmoney.com/js/fundcode_search.js"
response = requests.get(url)

all_funds_txt = response.text
all_funds_txt = all_funds_txt[all_funds_txt.find('=') + 2:all_funds_txt.rfind(';')]

print(all_funds_txt)

all_funds_list = json.loads(all_funds_txt)

print(all_funds_list)

print("start %s, return funds total count: %d" % (datetime.datetime.now(), len(all_funds_list)))


# 创建对象的基类:
Base = declarative_base()


# 定义Fund对象
class Fund(Base):
    # 表的名称
    __tablename__ = 'fundzoo'

    # 表的结构
    fundcode = Column(String(255), primary_key=True)
    fundname_abbr = Column(String(255))
    fundname_szm = Column(String(255))
    fundname_quanpin = Column(String(255))
    fund_type = Column(String(255))


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
    print(fund)
    # 创建新Fund对象:
    tmp_fund = Fund(fundcode=fundcode, fundname_abbr=fundname_abbr,
                    fundname_szm=fundname_szm, fundname_quanpin=fundname_quanpin,
                    fund_type=fund_type)
    # 添加到session:
    session.merge(tmp_fund)

# 提交即保存到数据库:
session.commit()
# 关闭session:
session.close()