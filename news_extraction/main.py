# -*- coding: utf8 -*-
from bottle import run, route, static_file,request,template
import project_pyltp,url_parser,sql_data,random
from collections import defaultdict

@route('/')
def index0():         
    return static_file('index.html', root='./webpage') 
    
@route('/html/')
def index():         
    return static_file('index.html', root='./html') 
    #return path 
    
@route('/<path>')
def webpage(path):
    return static_file(path, root='./webpage') 

@route('/download/<path>')
def webpage(path):
    return static_file(path, root='./download',download=path)

@route('/images/<path>')
def images(path):
    return static_file(path, root='./webpage/images')   
 
@route('/assets/css/<path>')
def css1(path):
    return static_file(path, root='./webpage/assets/css')

@route('/assets/js/<path>')
def js2(path):
    return static_file(path, root='./webpage/assets/js')
@route('/assets/fonts/<path>')
def fonts(path):
    return static_file(path, root='./webpage/assets/fonts')
@route('/demo')
def submit():
	try:
		text = request.query.textin
		if text == '':
			return '<script>alert(\'输入为空，请重新输入新闻内容，{}\')</script>'.format('谢谢使用！')
	except :
		return '<script>alert({})</script>'.format('网络异常，请重试！谢谢使用！')	
	
	flag = url_parser.get_url(text)
	
	if flag:
		content =  url_parser.get_content(flag)
		return text_deal_two(content)
	
	else:
		return text_deal_two(text)
@route('/try')
def submit_try():
        content = sql_data.news_content[random.randint(0,81000)]
        return text_deal(content)

def text_deal(text):

	text_list  = project_pyltp.text_split(text.strip().strip('\n'))
	content = defaultdict(list)
	content_list = []
	for number,text_one in enumerate(text_list):
		get_result = project_pyltp.sentence_parser(text_one)
		if not get_result[2]:continue
		if [x for x in get_result[2] if x in project_pyltp.say_words]:
			content[number+1] = get_result
	if content:
		content_list = list(content.items())
		content_list.insert(0,('No.',['人物名称','言论内容','言词态度']))
		content_list = [(x[0],x[1][0],x[1][1],x[1][2]) for x in content_list]
	if not content_list:
		return template('make_table',rows=[('Sorry!','','该新闻中没有发现人物言论！try模式下连续刷新即可获得新的结果。谢谢使用！','By SXQL')])
	return template('make_table', rows=content_list)

def text_deal_all(text):

        text_list  = project_pyltp.text_split(text.strip().strip('\n'))
        content = defaultdict(list)

        for number,text_one in enumerate(text_list):
                content[number+1] = project_pyltp.sentence_parser(text_one)
        if content:
                content_list = list(content.items())
                content_list.insert(0,('No.',['人物名称','言论内容','言论态度']))
                content_list = [(x[0],x[1][0],x[1][1],x[1][2]) for x in content_list]
        return template('make_table', rows=content_list)

def text_deal_two(text):

        text_list  = project_pyltp.text_split(text.strip().strip('\n'))
        content = defaultdict(list)
        content_list = []
        for number,text_one in enumerate(text_list):
                get_result = project_pyltp.sentence_parser(text_one)
                if not get_result[2]:continue
                if [x for x in get_result[2] if x in project_pyltp.say_words]:
                        content[number+1] = get_result
        if content:
                content_list = list(content.items())
                content_list.insert(0,('No.',['人物名称','言论内容','言词态度']))
                content_list = [(x[0],x[1][0],x[1][1],x[1][2]) for x in content_list]
        if not content_list:
                return template('make_table',rows=[('Sorry!','','该新闻中没有发现人物言论！谢谢使用！','By SXQL')])
        return template('make_table_new', rows=content_list)

if __name__ == '__main__':
	run(host="0.0.0.0", port=8229,debug=True)
