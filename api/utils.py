
def generate_breadcrumbs(name, current_url=None):
    breadcrumbs = [{'url': '/', 'name': 'Home'}]

    if current_url:
        breadcrumbs.append({'url': current_url, 'name': name})
    else:
        breadcrumbs.append({'name': name})

    return breadcrumbs
