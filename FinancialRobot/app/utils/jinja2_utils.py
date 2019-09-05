import jinja2


def render_without_request(template_name, filters={}, **context):
    """
    用法同 flask.render_template
    :param filters: 自行添加的过滤器
    :param template_name: 模板文件名
    :param context: 传输的变量
    :return: str 渲染后的模板
    """
    env = jinja2.Environment(
        loader=jinja2.PackageLoader('app', 'templates')
    )
    filters = filters or {}
    env.filters.update(filters)

    template = env.get_template(template_name)
    return template.render(**context)
