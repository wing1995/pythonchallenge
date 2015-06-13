# -*- coding: utf-8 -*-
import easygui as g
from pymongo import Connection
import sys
'''先连接数据库'''
con = Connection()
db = con.xywy_spider  # 连接xywy数据库
posts = db.spider  # 连接test中的xywyQuestion集合，相当于MySQL中的表


def get_data(question):  # 从数据库中获得数据
	'''str_q = []
	for each in question:  # 匹配输入的文字中的任何一个字
		str_q = each + '.*?'  # 增加匹配概率'''
	post_1 = posts.find({'question': {'$regex': str(question)}})  # 可以用正则匹配也可以用regex模糊匹配，各有优点
	count = post_1.count()  # 计算结果
	g.msgbox('一共有%d条相关结果' % count)  # 消息盒子
	all_results = []
	for each_1 in post_1:  # 遍历每一个结果
		results = '有人遇到了类似的问题：%s' % each_1['question']  # 输出问题
		all_results.append(results)
	return all_results

g.msgbox('嗨，欢迎进入我问我答疾病查询系统…………')
while 1:
	question = g.enterbox(msg='', title='请输入您的问题(注意：关键字越多，查询结果越少)')
	msg = '您的问题关键字是：'+str(question)
	title = '请选择与您类似的病例'
	choices = get_data(question)
	if choices:  # 如果找到了答案，将会返回具体的病例以及医生的答案
		choice = g.choicebox(msg, title, choices)
		post = posts.find({'question': {'$regex': str(choice).strip('有人遇到了类似的问题：')}})
		for each in post:
			analyse = each['analyse']
			suggestion = each['suggestion']
			msg = '如下是您想要的答案：'
			title = '医生的建议和分析'
			if each['suggestion']:
				result = g.msgbox(msg, title, '分析：' + analyse.replace('。', '\n') + '\n建议：' + suggestion.replace('。', '\n'))
			else:
				result = g.msgbox(msg, title, '分析：' + each['analyse'])

	else:
		continue

	msg = '您对这样的答案满意吗？'
	title = '请选择'

	if g.ccbox(msg, title, choices=('满意', '不满意')):
		g.msgbox(msg='很高兴为您解决疑惑，欢迎下次继续使用！', ok_button='goodbye!')
		sys.exit(0)
	else:
		pass


