from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base


##
# CREATE TABLE `fund_data_dict` (
#  `key` varchar(255) COLLATE utf8_bin NOT NULL COMMENT '主键',
#  `value` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '取值',
#  PRIMARY KEY (`key`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
# #
# 定义FundDataDict对象


class FundDataDict(declarative_base()):
    # 表的名称
    __tablename__ = 'fund_data_dict'
    
    # 表的结构
    # key
    key = Column(String(255), primary_key=True)
    # value
    value = Column(String(255))

    def __init__(self, key, value):
        self.key = key
        self.value = value
