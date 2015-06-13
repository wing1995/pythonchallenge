# coding=utf-8
__author__ = 'wing1995'
def ques_0(number,time):
	result = number ** time
	print result

# ques_0(2,38)
def ques_1(clause_1):
	clause_2=''
	al = 'qwertyuiopasdfghjklzxcvbnm'
	for i in clause_1:
		if i in al:
			t = ord(i)
			if t > 120:
				t = t-24
			else:
				t = t+2
			clause_2 += chr(t)
		else:
			clause_2 += i
	print clause_2

'''clause='map'
ques_1(clause)'''

def ques_2(file_1):
	f = open(file_1, 'r')
	dict_char = {}
	for eachLine in f:
		for each in eachLine:
			if dict_char.has_key(each):
				dict_char[each] += 1
			else:
				dict_char[each] = 1

	print dict_char

'''filename = 'C:\\Users\\wing1995\\Desktop\\rare.txt'
ques_2(filename)'''

import re,string
def ques_3(file_2):
	f = open(file_2, 'r')
	text = "".join(map(string.rstrip, f.readlines()))  # 将文件对象转换为字符串
	# print text
	f.close()
	result = "".join(re.findall('[a-z][A-Z]{3}([a-z])[A-Z]{3}[a-z]',text))
	print result

'''filename = 'C:\\Users\\wing1995\\Desktop\\re.txt'
ques_3(filename)'''

import re,urllib2
def ques_4(url):
	content_1 = urllib2.urlopen(url).read()
	data = re.findall('\d+',content_1)[0]
	data = string.atoi(data)
	time = 0
	while data:
		next_url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=%d' % data
		content_2 = urllib2.urlopen(next_url).read()
		print content_2
		try:
			data = re.findall('\d+',content_2)[-1]
			data = string.atoi(data)  # 将字符串转化为数字
		except IndexError, e:
			print "could not get the data:", e,",because the page is:",content_2
			if len(content_2) > 20:
				data = data / 2
			else:
				print content_2
		finally:
				time += 1

'''url = 'http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=60074'
ques_4(url)'''

# -*- coding: cp936 -*-
import urllib, pickle
def get_banner(banner):
    banner = pickle.loads(banner)
    for line in banner:
        l = "".join(map(lambda pair: pair[0] * pair[1], line))
        print l
'''banner = urllib.urlopen("http://www.pythonchallenge.com/pc/def/banner.p").read()
get_banner(banner)'''

import re
def get_data(filename):
    f = open(filename, 'r+')
    s = f.readlines()[0] # 得到字符串
    return s
def get_url(content):
    for i in range(300):
        print "%s" % content  # 打印文件内容
        search_url = re.findall("\.html", content)  # 最终目标
        name = re.findall("\d+", content)[-1]  #  得到下一次需要打开的文件名字
        if name:
            full_name = "C:\\Users\\Administrator_7\\Downloads\\" + name + '.txt'
            content = get_data(full_name)
        else:
            break

filename = "C:\\Users\\Administrator_7\\Downloads\\90052.txt"
content = get_data(filename)
data = get_url(content)
print data

