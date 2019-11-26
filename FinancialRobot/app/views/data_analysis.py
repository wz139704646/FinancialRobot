from app.utils.DBHelper import MyHelper
# from app.utils.RegressionHelper import *
from flask import Blueprint, render_template, request
from app.dao.DataAnalysisDao import DataAnalysisDao
from app.utils.auth import check_token
from app.utils.json_util import *
from flask import Blueprint, render_template, request, session, jsonify
from app.utils.json_util import *
from app.utils.crawler import *
import uuid
import urllib
import re

# 都是对于利润表/负债表/主要指标表/现金流量表的分析操作
# 因为我们的数据，所以时间均是09-18 / 10-19

analysis_results = Blueprint('analysis_results', __name__)


@analysis_results.before_request
@check_token
def res():
    pass


# 0 时间（年份tuple)
@analysis_results.route("/data/time0918", methods=["GET", "POST"])
def get09_18_tuple():
    res = {x: x + 2009 for x in range(0, 10)}
    return jsonify(return_success(res))


@analysis_results.route("/data/time1019", methods=["GET", "POST"])
def get10_19_tuple():
    res = {x: x + 2010 for x in range(0, 10)}
    return jsonify(return_success(res))


# 1 主要指标表
# 返回09-18年的净利润增长率tuple
@analysis_results.route("/data/profitRates", methods=["GET", "POST"])
def get_asset_growth_rate_per_year():
    info = DataAnalysisDao().query_main_indicators()
    for i in range(len(info)):
        if info[i][0] == '净利润增长率（%）':
            dict_of_years_and_rates = {x + 2008: info[i][x] for x in range(1, 11)}
            return jsonify(return_success(dict_of_years_and_rates))
    return jsonify(return_unsuccess('无法获取相关净利润增长率信息'))


# 返回09-18年每股收益tuple
@analysis_results.route("/data/earningsPerShare", methods=["GET", "POST"])
def get_earnings_per_share():
    info = DataAnalysisDao().query_main_indicators()
    for i in range(len(info)):
        if info[i][0] == '每股收益（元）':
            dict_of_years_and_rates = {x + 2008: info[i][x] for x in range(1, 11)}
            return jsonify(return_success(dict_of_years_and_rates))
        return jsonify(return_unsuccess('无法获取相关每股收益信息'))


# # 输入一个表和想预测的年份，返回拟合曲线预测的year年的值，默认表第一个列是年份
# @analysis_results.route("/data/predict", methods=["GET", "POST"])
# def predict(tbl, year):
#     regression_results = fit_line(tbl)
#     s = regression_results.item(0)
#     i = regression_results.item(1)
#     return round(year * s + i, 2)


# # 返回一个表，接受两个tuple作为两列，第一列是years，第二列是值values
# @analysis_results.route("/data/createTable", methods=["GET", "POST"])
# def create_table(years_tuple, values_tuple):
#     tbl = ds.Table().with_columns(
#         'year', tuple(map(lambda x: int(x), years_tuple)),
#         'earnings', tuple(map(lambda x: float(x), values_tuple))
#     )
#     return tbl


# 连接销售表和商品表，并返回不同商品种类/销量占比/销售额占比的二维tuple
# ((None, 0.0156, Decimal('48.00')), ('日用品类', 0.1719, Decimal('4175.84')), ('食品类', 0.8125, Decimal('3722.42')))
@analysis_results.route("/data/getSalesProportions", methods=["GET", "POST"])
def analyze_sales():
    info = DataAnalysisDao().query_sales_proportions()
    total_num = 0
    for i in range(len(info)):
        total_num += info[i][1]
    info = tuple(map(lambda tu: tuple([tu[0], round(int(tu[1]) / total_num, 4), float(tu[2])]), info))
    sum_proportions = 0
    for i in range(len(info)):
        sum_proportions += info[i][1]
    if sum_proportions != 1:
        info = tuple(map(lambda tu: tuple([tu[0], tu[1] + (1 - sum_proportions) / len(info), tu[2]]), info))
    sales_dict = {t[0]: t[2] for t in info}
    if not sales_dict:
        return jsonify(return_unsuccess('无法获取相关销售比例信息'))
    return jsonify(return_success(sales_dict))


# 按年月查看不同商品种类/销量占比/销售额占比
@analysis_results.route("/data/getSalesProportionsByYearAndMonth", methods=["GET", "POST"])
def analyze_sales_by_year_and_month(year, month):
    info = DataAnalysisDao().query_sales_sum_proportions_by_year_and_month(year, month)
    total_num = 0
    try:
        for i in range(len(info)):
            total_num += info[i][1]
    except():
        Exception('sql failed!')
    info = tuple(map(lambda tu: tuple([tu[0], round(int(tu[1]) / total_num, 4), tu[2]]), info))
    sum_proportions = 0
    for i in range(len(info)):
        sum_proportions += info[i][1]
    if sum_proportions != 1:
        info = tuple(map(lambda tu: tuple([tu[0], tu[1] + (1 - sum_proportions) / len(info), tu[2]]), info))
    return info


# 按年查看不同种类总销售额变化
@analysis_results.route("/data/getTotalSalesByYearAndMonth", methods=["GET", "POST"])
def analyze_sales_by_year():
    _json = request.json
    year = int(_json.get('year'))
    if not year:
        return jsonify(return_unsuccess('无法获取总销售额信息'))
    types = DataAnalysisDao().query_type_from_goods()
    dict_keys = []
    for m in range(1, 13):
        for typeOfGoods in types:
            if m < 10:
                month = "0" + str(m)
            else:
                month = str(m)
            temp_key = month + str(typeOfGoods[0])
            dict_keys.append(temp_key)
    dict_of_year_month_type_and_total_sales = {key: 0 for key in dict_keys}
    for i in range(1, 13):
        if i < 10:
            month = "0" + str(i)
        else:
            month = str(i)
        info = DataAnalysisDao().query_sales_sum_proportions_by_year_and_type(year, month)
        for tu in info:
            if i < 10:
                month = "0" + str(i)
            else:
                month = str(i)
            dict_of_year_month_type_and_total_sales[month + str(tu[0])] = float(tu[1])
    if not dict_of_year_month_type_and_total_sales:
        return jsonify(return_unsuccess('无法获取总销售额信息'))
    return jsonify(return_success(dict_of_year_month_type_and_total_sales))


# 查看某年某月的营业收入
@analysis_results.route("/data/getOperatingIncomeByYearAndMonth", methods=["GET", "POST"])
def analyze_operating_income_by_year():
    _json = request.json
    year = int(_json.get('year'))
    month = int(_json.get('month'))
    info = DataAnalysisDao().query_operating_income_by_year_and_month(year, month)
    dict_of_day_type_and_operating_income = {}
    days = list(range(1, 32))
    for i in range(len(days)):
        if days[i] < 10:
            days[i] = '0' + str(days[i])
        else:
            days[i] = str(days[i])
    for d in days:
        for t in ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']:
            dict_of_day_type_and_operating_income[d + t] = 0
    for tu in info:
        if int(tu[0]) < 10:
            dict_of_day_type_and_operating_income['0' + str(tu[0]) + str(tu[1])] = float(tu[2])
        else:
            dict_of_day_type_and_operating_income[str(tu[0]) + str(tu[1])] = float(tu[2])
    if not dict_of_day_type_and_operating_income:
        return jsonify(return_unsuccess('无法获取当月营收信息'))
    return jsonify(return_success(dict_of_day_type_and_operating_income))


# 查看总的营收占比
@analysis_results.route("/data/getTotalOperatingIncome", methods=["GET", "POST"])
def analyze_total_operating_income():
    info = DataAnalysisDao().query_total_operating_income()
    dict_of_type_and_total_operating_income = {t: float(0) for t in ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']}
    for tu in info:
        dict_of_type_and_total_operating_income[str(tu[0])] = float(tu[1])
    if not dict_of_type_and_total_operating_income:
        return jsonify(return_unsuccess('无法获取总营收信息'))
    return jsonify(return_success(dict_of_type_and_total_operating_income))


# 查看某年的某月的营业支出
@analysis_results.route("/data/getOperatingExpenditureByYearAndMonth", methods=["GET", "POST"])
def analyze_operating_expenditures_by_year_and_month():
    _json = request.json
    year = int(_json.get('year'))
    month = int(_json.get('month'))
    info = DataAnalysisDao().query_operating_expenditure_by_year_and_month(year, month)
    dict_of_day_type_and_operating_expenditure = {}
    days = list(range(1, 32))
    for i in range(len(days)):
        if days[i] < 10:
            days[i] = '0' + str(days[i])
        else:
            days[i] = str(days[i])
    for d in days:
        for t in ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']:
            dict_of_day_type_and_operating_expenditure[d + t] = 0
    for tu in info:
        if int(tu[0]) < 10:
            dict_of_day_type_and_operating_expenditure['0' + str(tu[0]) + str(tu[1])] = float(tu[2])
        else:
            dict_of_day_type_and_operating_expenditure[str(tu[0]) + str(tu[1])] = float(tu[2])
    if not dict_of_day_type_and_operating_expenditure:
        return jsonify(return_unsuccess('无法获取当月营收信息'))
    return jsonify(return_success(dict_of_day_type_and_operating_expenditure))


# 查看某年的每个月的营业支出
@analysis_results.route("/data/getOperatingExpenditureByYear", methods=["GET", "POST"])
def analyze_operating_expenditures_by_year():
    _json = request.json
    year = int(_json.get('year'))
    types = ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']
    dict_keys = []
    info = DataAnalysisDao().query_operating_expenditure_by_year_with_types(str(year))
    for m in range(1, 13):
        for typeOfGoods in types:
            if m < 10:
                month = "0" + str(m)
            else:
                month = str(m)
            temp_key = month + str(typeOfGoods[0])
            dict_keys.append(temp_key)
    dict_of_day_type_and_operating_expenditures = {key: 0 for key in dict_keys}
    for tu in info:
        if int(str(tu[0])) < 10:
            dict_of_day_type_and_operating_expenditures["0" + str(tu[0]) + str(tu[1])] = float(tu[2])
        else:
            dict_of_day_type_and_operating_expenditures[str(tu[0]) + str(tu[1])] = float(tu[2])
    if not dict_of_day_type_and_operating_expenditures:
        return jsonify(return_unsuccess('无法获取当月营收信息'))
    return jsonify(return_success(dict_of_day_type_and_operating_expenditures))

    # _json = request.json
    # year = int(_json.get('year'))
    # if not year:
    #     return jsonify(return_unsuccess('无法获取年份参数'))
    # info = DataAnalysisDao().query_operating_expenditure_by_year(year)
    # dict_of_month_and_operating_expenditure = {str(month): str(0) for month in range(1, 13)}
    # for tu in info:
    #     dict_of_month_and_operating_expenditure[str(tu[0])] = str(tu[1])
    # if not dict_of_month_and_operating_expenditure:
    #     return jsonify(return_unsuccess('无法获取营业支出信息'))
    # return jsonify(return_success(dict_of_month_and_operating_expenditure))


# 查看总的营业支出占比
@analysis_results.route("/data/getTotalOperatingExpenditure", methods=["GET", "POST"])
def analyze_total_operating_expenditure():
    info = DataAnalysisDao().query_total_operating_expenditure()
    dict_of_type_and_total_operating_expenditure = {t: float(0) for t in ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']}
    for tu in info:
        dict_of_type_and_total_operating_expenditure[str(tu[0])] = float(tu[1])
    if not dict_of_type_and_total_operating_expenditure:
        return jsonify(return_unsuccess('无法获取总营业支出信息'))
    return jsonify(return_success(dict_of_type_and_total_operating_expenditure))


# 查看每年的营业利润
@analysis_results.route("/data/getOperatingProfits", methods=["GET", "POST"])
def analyze_operating_profits():
    info = DataAnalysisDao().query_operating_profits()
    dict_of_year_and_operating_profits = {i + 2010: info[0][i + 1] for i in range(0, 10)}
    if not dict_of_year_and_operating_profits:
        return jsonify(return_unsuccess('无法获取营业利润信息'))
    return jsonify(return_success(dict_of_year_and_operating_profits))


# 查看每年的利润总额
@analysis_results.route("/data/getTotalProfits", methods=["GET", "POST"])
def analyze_total_profits():
    info = DataAnalysisDao().query_total_profits()
    dict_of_year_and_operating_profits = {i + 2010: info[0][i + 1] for i in range(0, 10)}
    if not dict_of_year_and_operating_profits:
        return jsonify(return_unsuccess('无法获取利润总额信息'))
    return jsonify(return_success(dict_of_year_and_operating_profits))


# 查看每年的净利润
@analysis_results.route("/data/getNetProfit", methods=["GET", "POST"])
def analyze_net_profit():
    info = DataAnalysisDao().query_net_profit()
    dict_of_year_and_net_profit = {i + 2010: info[0][i + 1] for i in range(0, 10)}
    if not dict_of_year_and_net_profit:
        return jsonify(return_unsuccess('无法获取净利润信息'))
    return jsonify(return_success(dict_of_year_and_net_profit))


# 返回每年的毛利率 毛利率=(销售收入-销售成本)/销售收入≈营业利润或利润总额/(销售收入（营业收入）)
@analysis_results.route("/data/getGrossProfitRate", methods=["GET", "POST"])
def analyze_gross_profit_rate():
    operating_profits = DataAnalysisDao().query_operating_profits()
    operating_incomes = DataAnalysisDao().query_operating_income()
    dict_of_year_and_gross_profit_rate = {
        i + 2010: 100 * float(float(operating_profits[0][i + 1]) / float(operating_incomes[0][i + 1])) for i in
        range(0, 10)}
    if not dict_of_year_and_gross_profit_rate:
        return jsonify(return_unsuccess('无法获取毛利率信息'))
    return jsonify(return_success(dict_of_year_and_gross_profit_rate))


# 返回每年的净利率 净利率=净利润/(销售收入（营业收入）)
@analysis_results.route("/data/getNetProfitRate", methods=["GET", "POST"])
def analyze_net_profit_rate():
    net_profits = DataAnalysisDao().query_net_profit()
    operating_incomes = DataAnalysisDao().query_operating_income()
    dict_of_year_and_net_profit_rate = {
        i + 2010: 100 * float(float(net_profits[0][i + 1]) / float(operating_incomes[0][i + 1])) for i in range(0, 10)}
    if not dict_of_year_and_net_profit_rate:
        return jsonify(return_unsuccess('无法获取净利率信息'))
    return jsonify(return_success(dict_of_year_and_net_profit_rate))


# 返回每年的周转率 资产周转率=(销售收入（营业收入）)/资产总额
@analysis_results.route("/data/getTurnoverRate", methods=["GET", "POST"])
def analyze_turnover_rate():
    operating_incomes = DataAnalysisDao().query_operating_income()
    total_assets = DataAnalysisDao().query_total_assets()
    dict_of_year_and_total_assets = {
        i + 2010: 100 * float(float(operating_incomes[0][i + 1]) / float(total_assets[0][i + 1])) for i in range(0, 10)}
    if not dict_of_year_and_total_assets:
        return jsonify(return_unsuccess('无法获取资产周转率信息'))
    return jsonify(return_success(dict_of_year_and_total_assets))


# 返回每年的债务率 债务率=总负债/总资产
@analysis_results.route("/data/getDebtRate", methods=["GET", "POST"])
def analyze_debt_rate():
    total_diets = DataAnalysisDao().query_total_diets()
    total_assets = DataAnalysisDao().query_total_assets()
    dict_of_year_and_total_assets = {i + 2010: 100 * float(float(total_diets[0][i + 1]) / float(total_assets[0][i + 1]))
                                     for i in range(0, 10)}
    if not dict_of_year_and_total_assets:
        return jsonify(return_unsuccess('无法获取债务率信息'))
    return jsonify(return_success(dict_of_year_and_total_assets))


# 返回每年的流动比率 流动比率=流动资产/流动负债
@analysis_results.route("/data/getLiquidRatio", methods=["GET", "POST"])
def analyze_liquid_ratio_rate():
    total_diets = DataAnalysisDao().query_total_diets()
    total_assets = DataAnalysisDao().query_total_assets()
    total_fixed_assets = DataAnalysisDao().query_fiexed_assets()
    dict_of_year_and_total_assets = {
        i + 2010: 100 * float(float(total_assets[0][i + 1]) - float(total_fixed_assets[0][i + 1])) / float(
            total_diets[0][i + 1]) for i in range(0, 9)}
    if not dict_of_year_and_total_assets:
        return jsonify(return_unsuccess('无法获取流动比率信息'))
    return jsonify(return_success(dict_of_year_and_total_assets))


# 返回每年的现金比率 现金比率=现金/流动负债
@analysis_results.route("/data/getCashRatio", methods=["GET", "POST"])
def analyze_cash_ratio():
    total_diets = DataAnalysisDao().query_total_diets()
    total_cash = DataAnalysisDao().query_cash()
    dict_of_year_and_total_assets = {i + 2010: 100 * float(total_cash[0][i + 1]) / float(total_diets[0][i + 1]) for i in
                                     range(0, 10)}
    if not dict_of_year_and_total_assets:
        return jsonify(return_unsuccess('无法获取现金比率信息'))
    return jsonify(return_success(dict_of_year_and_total_assets))


# 返回http://quotes.money.163.com/f10/hydb_000001.html的第一个表的每一行的4个数据 爬虫文件crawler.py在utils中
@analysis_results.route("/data/getIndustryData", methods=["GET", "POST"])
def getData():
    names = getCompanyNames()[0:7]
    values = getValues()
    if len(names) != len(values) or len(names) == 0:
        return jsonify(return_unsuccess('无法获取网页信息，出现bug'))
    dict_of_name_and_value = {names[i]: values[i] for i in range(7)}
    return jsonify(return_success(dict_of_name_and_value))


# 查看仓库不同种类商品价值比例
@analysis_results.route("/data/getRatioOfGoodsInWarehouse", methods=["GET", "POST"])
def analyze_goods_ratio():
    info = DataAnalysisDao().query_goods_in_warehouse()
    dict_of_type_and_ratio = {t: float(0) for t in ['食品类', '日用品类', '童装类', '营养品类', '玩具类',  '其他类']}
    for tu in info:
        dict_of_type_and_ratio[str(tu[0])] = float(tu[1])
    if not dict_of_type_and_ratio:
        return jsonify(return_unsuccess('无法获取仓库信息'))
    return jsonify(return_success(dict_of_type_and_ratio))


# 查询返回某年某月的销售记录
@analysis_results.route("/data/getSalesDetailByYearAndMonth", methods=["GET", "POST"])
def analyze_sales_detail_by_month():
    _json = request.json
    year = int(_json.get('year'))
    month = int(_json.get('month'))
    info = DataAnalysisDao().query_sales_info_by_year_and_month(year, month)
    detail = []
    for tu in info:
        detail.append(str(tu[2]) + ' ' + str(tu[0]) + '向' + str(tu[1]) + '购买了' + str(tu[3]) + str(tu[4]) + str(tu[5]) + '，共计' + str(tu[6]) + '元。')
    dict_of_index_and_detail = {i: detail[i] for i in range(len(detail))}
    if not dict_of_index_and_detail:
        return jsonify(return_unsuccess('无法获取销售信息'))
    return jsonify(return_success(dict_of_index_and_detail))


# 查询返回某年某月某日的销售记录
@analysis_results.route("/data/getSalesDetailByDate", methods=["GET", "POST"])
def analyze_sales_detail_by_date():
    _json = request.json
    year = int(_json.get('year'))
    month = int(_json.get('month'))
    day = int(_json.get('day'))
    info = DataAnalysisDao().query_sales_info_by_date(year, month, day)
    detail = []
    for tu in info:
        detail.append(str(tu[2]) + ' ' + str(tu[0]) + '向' + str(tu[1]) + '购买了' + str(tu[3]) + str(tu[4]) + str(tu[5]) + '，共计' + str(tu[6]) + '元。')
    dict_of_index_and_detail = {i: detail[i] for i in range(len(detail))}
    if not dict_of_index_and_detail:
        return jsonify(return_unsuccess('无法获取销售信息'))
    return jsonify(return_success(dict_of_index_and_detail))


# 商品名
# 查询返回某类的销售记录
@analysis_results.route("/data/getSalesDetailByCategory", methods=["GET", "POST"])
def analyze_sales_detail_by_category():
    _json = request.json
    category = str(_json.get('category'))
    info = DataAnalysisDao().query_sales_info_by_category(category)
    print(info)
    detail = []
    for tu in info:
        detail.append((str(tu[6]), str(tu[5]), str(round(tu[6] / tu[3], 2)), str(tu[3]), str(tu[0]), str(tu[1])))
    print (detail)
    dict_of_index_and_detail = {i: detail[i] for i in range(len(detail))}
    if not dict_of_index_and_detail:
        return jsonify(return_unsuccess('无法获取销售信息'))
    return jsonify(return_success(dict_of_index_and_detail))


# 采购 进货来源 采购时间 采购总金额 商品名字 个数 单价
# 查询返回某类的采购记录
@analysis_results.route("/data/getPurchaseDetailByCategory", methods=["GET", "POST"])
def analyze_purchase_detail_by_category():
    _json = request.json
    category = str(_json.get('category'))
    info = DataAnalysisDao().query_purchase_info_by_category(category)
    detail = []
    for tu in info:
        print(detail)
        detail.append((str(tu[0]), str(tu[1]), str(tu[2]), str(tu[3]), str(tu[4]), str(tu[5]), str(tu[6]), str(tu[7])))
    dict_of_index_and_detail = {i: detail[i] for i in range(len(detail))}
    if not dict_of_index_and_detail:
        return jsonify(return_unsuccess('无法获取采购信息'))
    return jsonify(return_success(dict_of_index_and_detail))


# 查询返回number个低库存商品
@analysis_results.route("/data/getBackorderGoods", methods=["GET", "POST"])
def analyze_BackorderGoods():
    _json = request.json
    number = str(_json.get('number'))
    info = DataAnalysisDao().query_backorder_goods(number)
    goods = []
    for tu in info:
        goods.append((str(tu[0]), str(tu[1]), str(tu[2])))
    dict_of_index_and_goods = {i: goods[i] for i in range(len(goods))}
    print(dict_of_index_and_goods)
    if not dict_of_index_and_goods:
        return jsonify(return_unsuccess('无法获取低库存商品信息'))
    return jsonify(return_success(dict_of_index_and_goods))