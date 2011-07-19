from docutils import core

import jinja2
from jingo import Register, env

register = Register(env)

@register.filter
def restructuredtext(blob):
    html = core.publish_string(blob, writer_name='html')
    return jinja2.Markup(html[html.find('<body>')+6:html.find('</body>')])

