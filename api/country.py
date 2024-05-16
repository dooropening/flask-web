from flask import Blueprint, render_template
from flask import request
from api.mongo_local_operation import collection


country_bp = Blueprint('country', __name__)


@country_bp.route('/country')
def country_quotes():
    # 从数据库中获取国家名言数据
    # 这里你需要编写适合你数据结构的查询代码
    countries = collection.distinct("country")  # 假设国家信息存储在名为 'country' 的字段中
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'name': 'Country'}]

    # 渲染模板并传递数据给模板
    return render_template('country.html', countries=countries, breadcrumbs=breadcrumbs)


@country_bp.route('/country/<country_name>')
def country_quotes_detail(country_name):
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'url': '/country', 'name': 'Country'}, {'name': country_name}]
    page = int(request.args.get('page', default=1))
    per_page = 10
    # 从数据库中获取特定国家的名言数据
    # 这里你需要编写适合你数据结构的查询代码
    quotes = collection.find({"country": country_name}).skip((page-1)*per_page).limit(per_page)
    quote_list = list(quotes)  # 转换为列表

    # 获取总记录数以计算总页数
    total_quotes = collection.count_documents({"country": country_name})
    total_pages = (total_quotes + per_page - 1) // per_page  # 向上取整

    return render_template('country_quotes_detail.html', country_name=country_name, quotes=quotes, quote_list=quote_list, breadcrumbs=breadcrumbs, page=page, total_pages=total_pages)
