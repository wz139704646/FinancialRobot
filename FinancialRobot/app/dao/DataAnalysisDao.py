#!/usr/bin/env python
# -*- coding:utf-8 -*-
from app.utils.DBHelper import MyHelper


class DataAnalysisDao:

    def query_main_indicators(self):
        return MyHelper().executeQuery("select * from main_indicators01;")

    def query_sales_proportions(self):
        return MyHelper().executeQuery("select type, count(goodsId),  sum(sumprice) from Sell, Goods where Sell.goodsId = Goods.id group by type;")

    def query_sales_sum_proportions_by_year_and_month(self, year, month):
        return MyHelper().executeQuery("select type, count(goodsId),  sum(sumprice) from Sell, Goods where Sell.goodsId = Goods.id and date_format(Sell.date, '%%Y-%%m') = '" + str(year) + "-" + month + "' group by type;")

    def query_sales_sum_proportions_by_year_and_type(self, year, month):
        return MyHelper().executeQuery("select type, sum(sumprice) as sum from Sell, Goods where Sell.goodsId = Goods.id and date_format(Sell.date, '%%Y-%%m') = '" + str(year) + "-" + month + "' group by type;")

    def query_type_from_goods(self):
        return MyHelper().executeQuery("select type from Goods;")

    def query_operating_expenditure_by_year(self, year):
        return MyHelper().executeQuery("select month(date), sum(number*purchasePrice) from Purchase where year(date) = " + str(year) + " group by month(date);")

    def query_operating_profits(self):
        return MyHelper().executeQuery("select * from Profit_01 where row_info = '营业利润';")

    def query_total_profits(self):
        return MyHelper().executeQuery("select * from Profit_01 where row_info = '利润总额';")

    def query_operating_income_by_year_and_month(self, year, month):
        return MyHelper().executeQuery("select DAY(date), type, sum(sumprice) from Sell, Goods where year(date) = " + str(year) + " and month(date) = " + str(month) + " and Sell.goodsId = Goods.id group by DAY(date), type;")

    def query_total_operating_income(self):
        return MyHelper().executeQuery("select type, sum(sumprice) from Sell, Goods where Sell.goodsId = Goods.id group by type;")

    def query_operating_expenditure_by_year_and_month(self, year, month):
        return MyHelper().executeQuery("select DAY(date), type, sum(Purchase.number*Purchase.purchasePrice) from Purchase, Goods where year(date) = " + str(year) + " and month(date) = " + str(month) + " and Purchase.goodId = Goods.id group by DAY(date), type;")

    def query_total_operating_expenditure(self):
        return MyHelper().executeQuery("select type, sum(Purchase.number*purchasePrice) from Purchase, Goods where Purchase.goodId = Goods.id group by type;")

    def query_net_profit(self):
        return MyHelper().executeQuery("select * from Profit_01 where row_info = '净利润';")

    def query_operating_income(self, ):
        return MyHelper().executeQuery("select * from Profit_01 where row_info = '营业收入';")

    def query_total_assets(self):
        return MyHelper().executeQuery("select * from Diet01 where Diet01.`﻿info` = '总资产';")

    def query_total_diets(self):
        return MyHelper().executeQuery("select * from Diet01 where Diet01.`﻿info` = '总负债';")

    def query_fiexed_assets(self):
        return MyHelper().executeQuery("select * from Diet01 where Diet01.`﻿info` = '持有至到期投资';")

    def query_cash(self):
        return MyHelper().executeQuery("select * from Diet01 where Diet01.`﻿info` = '现金及存放中央银行款项';")

    def query_goods_in_warehouse(self):
        return MyHelper().executeQuery("select type, sum(sellprice*number) from Goods, GoodsStore where Goods.id = goodsId group by type;")

    def query_sales_info_by_year_and_month(self, year, month):
        return MyHelper().executeQuery("select s.customerName, c.name, date, number, unitInfo, goodsName, sumprice from Sell as s, Company as c where c.id = s.companyId and MONTH(date) = " + str(month) + " and YEAR(date) = " + str(year) + " and number <> 0 and sumprice is not NULL order by date;")

    def query_sales_info_by_date(self, year, month, day):
        return MyHelper().executeQuery(
            "select s.customerName, c.name, date, number, unitInfo, goodsName, sumprice from Sell as s, Company as c where c.id = s.companyId and MONTH(date) = " + str(month) + " and YEAR(date) = " + str(year) + " and DAY(date) = " + str(day) + " and number <> 0 and sumprice is not NULL order by date;")

    def query_sales_info_by_category(self, category):
        return MyHelper().executeQuery("select s.customerName, c.name, date, number, g.unitInfo, goodsName, sumprice from Sell as s, Company as c, Goods as g where c.id = s.companyId and g.id = goodsId and g.type = '" + category + "' and number <> 0 and sumprice is not NULL order by date;")

    def query_purchase_info_by_category(self, category):
        return MyHelper().executeQuery("select c1.name, CONCAT(c2.name, s.name), date, p.number * p.purchasePrice, p.goodName, p.number, p.purchasePrice) from Purchase as p, Supplier as s, Company as c1, Company as c2, Goods as g where c1.id = p.companyId and p.supplierId = s.id and c2.id = s.companyId and p.goodname = g.name and g.type = '"+ category + "' and number <> 0 order by date;")