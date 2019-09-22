from requests_html import HTMLSession
import re

url_rule = r"(^http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)|([a-zA-Z]+.\w+\.+[a-zA-Z0-9\/_]+)"
content_rule = r'[\u4e00-\u9fa5\，\。\、\：]+'

def get_url(text):
    urls = re.findall(url_rule,text.strip().strip('\n'))
    try:
        if urls[0][1] == '':return urls[0][0]
        return False
    except:
        return False
def get_content(url):
    session = HTMLSession()
    try:
        content = ''.join(re.findall(content_rule,session.get(url).html.text))
        return content
    except:
        return ''
