from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class JSONResponse(HttpResponse):
	'''
	将内容转化为JSON格式的HttpResponse
	'''
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)

@csrf_exempt
def snippet_list(request):
	'''
	展示所有存在的snippet, 或者建立新的snippet
	'''
	if request.method == 'GET':  # 获得所有数据
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return JSONResponse(serializer.data)
	elif request.method == 'POST': # 提交数据
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():  # 如果数据存在就保存并提交，反之报错
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)

@csrf_exempt
def snippet_detail(request, pk):
	'''
	展示，更新或者删除一个snippet
	'''
	try:
		snippet = Snippet.objects.get(pk=pk)  # 尝试的获取数据
	except Snippet.DoesNotExist:  # 如果数据不存在就报错
		return HttpResponse(status=400)
	if request.method == 'GET':  # 如果是获取数据，就返回数据
		serializer = SnippetSerializer(snippet)
		return JSONResponse(serializer.data)
	elif request.method == 'PUT':  # 如果是发送数据
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet)  # 先将数据序列化
		if serializer.is_valid():  # 如果数据存在就保存，反之就报错
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400)
	elif request.method == 'DELETE':  # 如果是删除数据，就直接清空数据，并返回一个不存在的画面
		snippet.delete()
		return HttpResponse(status=204)