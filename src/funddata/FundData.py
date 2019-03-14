from sqlalchemy import Column, String, Integer, Float, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

# CREATE TABLE `fund_005919` (
#   `fundcode` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '基金代码',
#   `date` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL COMMENT '日期',
#   `dwjz` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '单位净值',
#   `ljjz` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '累计净值',
#   `rzzl` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '日增长率',
#   `buystatus` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '购买状态',
#   `salestatus` varchar(255) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL COMMENT '赎回状态',
#   `fenhong` varchar(255) COLLATE utf8_bin DEFAULT NULL COMMENT '分红配送',
#   `is_index` tinyint(3) DEFAULT NULL COMMENT '是否指数基金，1是 0否',
#   `pe` double DEFAULT NULL COMMENT '如果是指数基金，则该列为对应的PE-TTM',
#   PRIMARY KEY (`date`)
# ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

class FundData(declarative_base()):
    # 表名：fund_{fund_code}
    __tablename__ = 'fund_data'

    fundcode = Column(String(255))
    date = Column(String(255), primary_key=True)
    dwjz = Column(String(255))
    ljjz = Column(String(255))
    rzzl = Column(String(255))

    buystatus = Column(String(255))
    salestatus = Column(String(255))
    fenhong = Column(String(255))
    is_index = Column(Integer())
    pe = Column(Float())
    lastmodified = Column(String(255))

    def __init__(self, fundcode, date, dwjz, ljjz, rzzl,
                 buystatus, salestatus, fenhong, is_index, pe,
                 lastmodified):
        self.fundcode = fundcode
        self.date = date
        self.dwjz = dwjz
        self.ljjz = ljjz
        self.rzzl = rzzl

        self.buystatus = buystatus
        self.salestatus = salestatus
        self.fenhong = fenhong
        self.is_index = is_index
        self.pe = pe

        self.lastmodified = lastmodified
