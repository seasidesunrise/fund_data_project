from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

##
# CREATE TABLE `fundlist` (
#   `fundcode` varchar(255) COLLATE utf8_bin NOT NULL COMMENT '基金代码',
#   `fundname_abbr` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '基金简称',
#   `fundname_szm` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '基金名称首字母',
#   `fundname_quanpin` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '基金名称全拼',
#   `fund_type` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '基金类型：混合型、债券型等',
#   PRIMARY KEY (`fundcode`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
# #
# 定义Fund对象

class Fund(declarative_base()):
    # 表的名称
    __tablename__ = 'fundlist'

    # 表的结构
    # 基金代码
    fundcode = Column(String(255), primary_key=True)
    # 基金简称
    fundname_abbr = Column(String(255))
    # 基金简称首字母
    fundname_szm = Column(String(255))
    # 基金简称全拼
    fundname_quanpin = Column(String(255))
    # 基金类型
    fund_type = Column(String(255))

    def __init__(self, fundcode, fundname_abbr, fundname_szm, fundname_quanpin, fund_type):
        self.fundcode = fundcode
        self.fundname_abbr = fundname_abbr
        self.fundname_szm = fundname_szm
        self.fundname_quanpin = fundname_quanpin
        self.fund_type = fund_type
