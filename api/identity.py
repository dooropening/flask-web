from flask import Blueprint, render_template
from flask import request
from mongo_local_operation import collection


identity_bp = Blueprint('identity', __name__)


@identity_bp.route('/identity')
def identity_quotes():
    # 使用聚合框架获取所有文档中的身份信息
    pipeline = [
        {"$unwind": "$identity"},
        {"$group": {"_id": "$identity"}}
    ]
    identities_cursor = collection.aggregate(pipeline)

    # 将游标转换为列表
    identities = [doc['_id'] for doc in identities_cursor]

    # 渲染模板并传递数据给模板
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'name': 'identity'}]
    return render_template('identity.html', identities=identities, breadcrumbs=breadcrumbs)


@identity_bp.route('/identity/<identity_name>')
def identity_quotes_detail(identity_name):
    breadcrumbs = [{'url': '/', 'name': 'Home'}, {'url': '/identity', 'name': 'identity'}, {'name': identity_name}]
    page = int(request.args.get('page', default=1))
    per_page = 10
    # 从数据库中获取特定身份的名言数据
    quotes = collection.find({"identity": identity_name}).skip((page-1)*per_page).limit(per_page)
    quote_list = list(quotes)  # 转换为列表

    # 获取总记录数以计算总页数
    total_quotes = collection.count_documents({"identity": identity_name})
    total_pages = (total_quotes + per_page - 1) // per_page  # 向上取整

    return render_template('identity_quotes_detail.html', identity_name=identity_name, quotes=quotes, quote_list=quote_list, breadcrumbs=breadcrumbs, page=page, total_pages=total_pages)
