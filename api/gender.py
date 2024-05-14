from flask import Blueprint, render_template
from flask import request
from mongo_local_operation import collection

gender_bp = Blueprint('gender', __name__)


@gender_bp.route('/gender')
def gender_quotes():
    # 从数据库中获取国家名言数据
    # 这里你需要编写适合你数据结构的查询代码
    genders = collection.distinct("gender")
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'name': 'gender'}]

    # 渲染模板并传递数据给模板
    return render_template('gender.html', genders=genders, breadcrumbs=breadcrumbs)


@gender_bp.route('/gender/<gender_name>')
def gender_quotes_detail(gender_name):
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'url': '/gender', 'name': 'gender'}, {'name': gender_name}]
    page = int(request.args.get('page', default=1))
    per_page = 10
    quotes = collection.find({"gender": gender_name}).skip((page-1)*per_page).limit(per_page)
    quote_list = list(quotes)  # 转换为列表

    # 获取总记录数以计算总页数
    total_quotes = collection.count_documents({"gender": gender_name})
    total_pages = (total_quotes + per_page - 1) // per_page  # 向上取整

    return render_template('gender_quotes_detail.html', gender_name=gender_name, quotes=quotes, quote_list=quote_list, breadcrumbs=breadcrumbs, page=page, total_pages=total_pages)
