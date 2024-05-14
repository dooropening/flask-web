from flask import Blueprint, render_template
from flask import request
from mongo_local_operation import collection


attribute_bp = Blueprint('attribute', __name__)


@attribute_bp.route('/attribute')
def attribute_quotes():
    # 使用聚合框架获取所有文档中的身份信息
    pipeline = [
        {"$unwind": "$attribute"},
        {"$group": {"_id": "$attribute"}}
    ]
    attributes_cursor = collection.aggregate(pipeline)

    # 将游标转换为列表
    attributes = [doc['_id'] for doc in attributes_cursor]

    # 渲染模板并传递数据给模板
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'name': 'attribute'}]
    return render_template('attribute.html', attributes=attributes, breadcrumbs=breadcrumbs)


@attribute_bp.route('/attribute/<attribute_name>')
def attribute_quotes_detail(attribute_name):
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'url': '/attribute', 'name': 'attribute'}, {'name': attribute_name}]
    page = int(request.args.get('page', default=1))
    per_page = 10
    # 从数据库中获取特定身份的名言数据
    quotes = collection.find({"attribute": attribute_name}).skip((page-1)*per_page).limit(per_page)
    quote_list = list(quotes)  # 转换为列表

    # 获取总记录数以计算总页数
    total_quotes = collection.count_documents({"attribute": attribute_name})
    total_pages = (total_quotes + per_page - 1) // per_page  # 向上取整

    return render_template('attribute_quotes_detail.html', attribute_name=attribute_name, quotes=quotes, quote_list=quote_list, breadcrumbs=breadcrumbs, page=page, total_pages=total_pages)
