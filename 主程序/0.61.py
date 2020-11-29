#-*- coding:utf-8 -*-


from io import BytesIO
import gzip

from urllib import request,parse
import json
import time
import os
import sys
import shutil
import _thread
import traceback

'''
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
'''
__版本__=0.61
__doc__="版本:"+str(__版本__)



数据文件目录="smaqjypt_数据/"
错误信息文件目录=数据文件目录+"错误信息/"
用户表文件目录=数据文件目录+"用户表/"
用户数据文件=数据文件目录+"用户信息.json"
专题id文件=数据文件目录+"专题id表.json"
#安静模式=False
#安静模式=True
交互模式=True
安静模式=not 交互模式

发生错误={"获取专题id":{}}


临时用户数据=False
临时专题id=False


安静模式_=False


初次使用=False
try:
	exit
	文件类型=0
except:
	exit=sys.exit
	文件类型=1

def 清屏():
	'''
清空屏幕,部分命令行或终端不支持

'''
	if(os.name == "nt"):
		os.system('cls')
	elif(os.name == "posix"):
		os.system('clear')

def 获取键盘输入_linux():
	'''
在类linux使用,调用后可得到一个键盘输入而不显示在屏幕

返回值:
	输入键盘的字符

'''
	fd=sys.stdin.fileno()
	old_settings=termios.tcgetattr(fd)
	try:
		tty.setraw(sys.stdin.fileno())
		键盘输入=sys.stdin.read(1)
	except:''
	termios.tcsetattr(fd,termios.TCSADRAIN,old_settings)
	return 键盘输入

def 密码输入_linux(提示文字="密码:"):
	'''
在类linux使用,调用后可输入显示为星号"*"的密码,左右键可移动光标(部分终端不支持),输入完成后按回车,返回值为输入的密码

参数:
	提示文字
		调用函数后给用户输入密码的提示文字,显示在左侧

返回值:
	输入的密码

'''
	文本=""
	光标位置=0
	print(提示文字,end="",flush=True)
	while 1:
		键盘输入=获取键盘输入_linux()
		if(键盘输入==""):
			''
		elif(键盘输入=='\r'):
			break
		elif(键盘输入=='\x03'):#Ctrl+C
			raise KeyboardInterrupt
		elif(键盘输入=='\b' or 键盘输入=='\x7f'):#退格
			if(光标位置):
				文本=文本[0:光标位置-1]+文本[光标位置:]
				光标位置-=1
				#print("*"*(len(文本)-光标位置)+"\b "+"\b"*(len(文本)-光标位置+1),end="",flush=True)
		elif(键盘输入=='\x1b'):
			键盘输入=获取键盘输入_linux()
			if(键盘输入=='\x5b'):#方向键
				键盘输入=获取键盘输入_linux()
				if(键盘输入=='\x44'):#左
					if(光标位置):
						#print("\b",end="",flush=True)
						光标位置-=1
				if(键盘输入=='\x43'):#右
					if(光标位置<len(文本)):
						#print("*",end="",flush=True)
						光标位置+=1
		else:
			#print("//"+str(键盘输入.hex())+"//")
			try:文本=文本[0:光标位置]+键盘输入+文本[光标位置:]
			except:
				''#print("\r提示:无效的文本   ")
			else:
				光标位置+=1
				#print("*"*(len(文本)-光标位置+1)+"\b"*(len(文本)-光标位置),end="",flush=True)
		#print("\b"*(光标位置-1)+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#
		print("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#星号输入
		#print(hex(ord(str(键盘输入))))
		#print("\r"+提示文字+文本+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#明文输入
		#'''
	print()
	return 文本


def 密码输入_win(提示文字="密码:"):
	'''
在win使用,调用后可输入显示为星号"*"的密码,左右键可移动光标(部分命令行或终端不支持),输入完成后按回车,返回值为输入的密码

参数:
	提示文字
		调用函数后给用户输入密码的提示文字,显示在左侧

返回值:
	输入的密码

'''
	文本=""
	光标位置=0
	print(提示文字,end="",flush=True)
	#if(1):
	while 1:
		try:
			键盘输入=''
			键盘输入=msvcrt.getch()#.decode(encoding="utf-8").decode("hex")#.decode(encoding="utf-8")
		except:print('1')
		#print(" "+str(键盘输入.hex()),end="",flush=True)
		#'''
			#return input("12")
		if(键盘输入==""):
			''
		elif(键盘输入==b'\r'):
			break
		elif(键盘输入==b'\x03'):#Ctrl+C
			raise KeyboardInterrupt
		elif(键盘输入==b'\x08'):#退格
			if(光标位置):
				文本=文本[0:光标位置-1]+文本[光标位置:]
				光标位置-=1
				#print("*"*(len(文本)-光标位置)+"\b "+"\b"*(len(文本)-光标位置+1),end="",flush=True)
		elif(键盘输入==b'\xe0'):#方向键
			键盘输入=msvcrt.getch()
			if(键盘输入==b'\x4b'):#左
				if(光标位置):
					#print("\b",end="",flush=True)
					光标位置-=1
			if(键盘输入==b'\x4d'):#右
				if(光标位置<len(文本)):
					#print("*",end="",flush=True)
					光标位置+=1
		else:
			#print("//"+str(键盘输入.hex())+"//")
			try:文本=文本[0:光标位置]+键盘输入.decode(encoding="utf-8")+文本[光标位置:]
			except:
				''#print("\r提示:无效的文本   ")
			else:
				光标位置+=1
				#print("*"*(len(文本)-光标位置+1)+"\b"*(len(文本)-光标位置),end="",flush=True)
		#print("\b"*(光标位置-1)+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#
		print("\r"+提示文字+"*"*len(文本)+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#星号输入
		#print("\r"+提示文字+文本+" "+"\b"*(len(文本)-光标位置+1),end="",flush=True)#明文输入
		#'''
	print()
	return 文本

def 密码输入_明文(提示文字="密码:"):
	'''
在不支持使用星号"*"来隐藏密码时使用

参数:
	提示文字
		调用函数后给用户输入密码的提示文字,显示在左侧

返回值:
	输入的密码

'''
	print("注意:密码会显示")
	return input(提示文字)


try:
	import msvcrt
	密码输入=密码输入_win
	
	
	支持二维码_调整=1
	

	def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="任意",提示信息_2="键",提示信息_3="继续"):
		print(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3,end="",flush=True)
		if(msvcrt.getch()==b'\x03'):
			raise KeyboardInterrupt
		print()
except:
	try:
		import termios
		import sys,tty
		密码输入=密码输入_linux


		支持二维码_调整=2

		def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="任意",提示信息_2="键",提示信息_3="继续"):
			print(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3,end="",flush=True)
			if(获取键盘输入_linux()=='\x03'):
				raise KeyboardInterrupt
			print()
	except:
		密码输入=密码输入_明文
		def 按任意键继续(提示信息="",提示信息_0="按",提示信息_1="回车",提示信息_2="键",提示信息_3="继续"):
			print(提示信息+提示信息_0+提示信息_1+提示信息_2+提示信息_3,end="",flush=True)
			input(提示信息)



if(not os.path.isdir(数据文件目录)):

	#print('用户协议:')
	# if(input('若同意,输入"y"确认')!="y"):
	# 	exit()
	初次使用=True
	if(os.path.isfile(数据文件目录[0:-1])):
		按任意键继续('错误:无法创建文件夹"'+数据文件目录[0:-1]+'",该名称已被文件'+数据文件目录[0:-1]+'"占用,',提示信息_3='尝试删除')
		if(os.path.isfile(数据文件目录[0:-1])):
			os.remove(数据文件目录[0:-1])
	
	os.makedirs(数据文件目录[0:-1])
	
	
	with open(专题id文件,"w")as f:f.write("{}")
	
	with open(用户数据文件,"w")as f:f.write("{}")

if(not os.path.isdir(错误信息文件目录)):
	if(os.path.isfile(错误信息文件目录[0:-1])):
		按任意键继续('错误:无法创建文件夹"'+错误信息文件目录[0:-1]+'",该名称已被文件'+错误信息文件目录[0:-1]+'"占用,',提示信息_3='尝试删除')
		if(os.path.isfile(错误信息文件目录[0:-1])):
			os.remove(错误信息文件目录[0:-1])
	
	os.makedirs(错误信息文件目录[0:-1])
	
	with open(错误信息文件目录+"问题反馈帮助.txt","w")as f:f.write("若要反馈问题,可反馈到邮箱1738078451@qq.com,标题为\"问题反馈\",在正文中描述问题是如何发生的,并将错误信息添加到附件中,错误信息不会包括个人信息")

if(not os.path.isdir(用户表文件目录)):
	if(os.path.isfile(用户表文件目录[0:-1])):
		按任意键继续('错误:无法创建文件夹"'+用户表文件目录[0:-1]+'",该名称已被文件'+用户表文件目录[0:-1]+'"占用,',提示信息_3='尝试删除')
		if(os.path.isfile(用户表文件目录[0:-1])):
			os.remove(用户表文件目录[0:-1])
	
	os.makedirs(用户表文件目录[0:-1])





支持作者={"QQ":["https://i.qianbao.qq.com/wallet/sqrcode.htm?m=tenpay&f=wallet&u=1493440548&a=1&n=xzx&ac=CAEQpLCQyAUYqsX1_AUgZA%3D%3D_xxx_sign",[2183881429887,1123638912065,1598723748701,1605580479069,1601127118685,1123781735489,2187570009471,4050518784,2160578521258,1287982322297,229571837314,662601360170,2125783789228,140746175185,2050701419696,1994565185570,876954897932,1135984926673,721006375218,252486570186,2162627993900,1384341012441,1572080281848,1866466928146,374896835087,482943047665,155748236398,736978752225,988122206606,1827602487163,1434508393600,1512368201776,1117492931581,6391776533,2187452757846,1117924455184,1603754054135,1605531499781,1603224255440,1124566135650,2186282068516]],"微信":["wxp://f2f1cQJjDNbMoZc1x1pWGBubsDyZx2Hu-Vdm",[534599807,274515521,391518301,391831901,390111581,273909313,534074751,622080,432175919,381513787,499349639,168188579,475377848,422613619,427091357,254099363,75116937,319419443,132085069,34221544,499450362,1070871,532963669,273767186,391830513,390689453,391118055,273849659,534612346]],"支付宝":["https://qr.alipay.com/fkx16486yjrwnfci0um7o32",[533646463,272861505,391010141,391551837,391487069,273419585,534074751,618752,418220568,371468854,291190128,419837720,149693793,520450931,309618124,260125669,91880460,420262871,508408809,397043472,276533239,1646872,534115164,273892626,390989816,391101101,390915582,273884797,534560284]]}
#支持作者={"支付宝":["HTTPS://QR.ALIPAY.COM/FKX08622M1YUUOLO8IQL739",[33347199,17090369,24405853,24452701,24492125,17069889,33379711,36096,26117912,541788,2597555,10040888,27775998,20612248,24941548,20036007,19303925,76062,33362262,17108764,24424435,24393103,24408121,17136740,33381771]],"微信":["wxp://f2f0UaytZXTaH0ypV381WLZIgeah-Wc4yiIN",[532985727,274503745,391150685,390696797,391984221,274069057,534074751,1506304,442733430,295419213,148069240,328139534,427179201,412791308,450005215,507432586,100249017,60638753,333957147,18419880,333212151,1445649,534534490,273204511,390960635,391332945,390929141,274047218,534498618]],"QQ":["https://i.qianbao.qq.com/wallet/sqrcode.htm?m=tenpay&f=wallet&u=1493440548&a=1&n=xzx&ac=CAEQpLCQyAUYssT2-wU%3D_xxx_sign",[2188176397183,1116830567745,1603376628061,1602384584541,1604105768029,1117444428097,2187570009471,1420058368,2085574434461,1870747275898,1872699530294,490384871857,1808489396047,1041288073111,21190271583,1722910528318,1474688876990,2001565376776,240511676720,322911877631,166368708373,1456302614705,1919607313778,147259359681,479351650311,974017362500,1844826359541,1790315024995,1736888809802,905648108800,1576194272420,244137861028,1095059988465,8002356500,2184935577426,1118077240603,1598384850420,1602636763316,1603580017927,1121363914798,2187149935838]]}

def 支持作者_二维码(支持二维码_调整,指定二维码=0):
	支持作者_="\n付款是完全自愿的,不会因付款而拥有任何特权\n"
	if(len(支持作者)<指定二维码 or 指定二维码<0):
		return ""
	当前二维码=0
	for i in 支持作者:
		当前二维码+=1
		if(指定二维码!=0):
			if(当前二维码!=指定二维码):
				continue
		支持作者_+="\n\n"+i+"\n"+支持作者[i][0]+"\n"
		长度=len(str(bin(支持作者[i][1][0]))[2:])
		for i2 in 支持作者[i][1]:
			二维码_一行=str(bin(i2))[2:]
			二维码_一行=(长度-len(二维码_一行))*"  "+二维码_一行
			支持作者_+=二维码_一行.replace("0","  ").replace("1","▇"*支持二维码_调整)+"\n"
	return 支持作者_

__doc__+=支持作者_二维码(支持二维码_调整)

#使urllib 4xx-5xx状态码不引发异常
class HTTPErrorProcessor(request.BaseHandler):
	handler_order = 1000  # after all other processing
	def http_response(self, request, response):
		return response
	https_response = http_response
request.HTTPErrorProcessor=HTTPErrorProcessor


访问_暂停=False

def 访问(url,请求头={},请求方法=None,数据=None,cookie=None):
	'''
访问 http url.调用了urllib,简化了参数及流程

参数:
	url:
		访问的url,具体查看urllib.request.Request函数中参数url
	
	请求头:
		可选.默认请求头在"请求头_"中
		可传入  字典 列表 字符串  类型,但在本函数中最终都会转为字典:
			字典 类型:
				{"键1":"值1","键2":"值2","键3":"值3"}
			
			列表 类型:(": "可换为":")
				["键1: 值1","键2: 值2","键3: 值3"]

			字符串 类型:(": "可换为":","\n\r"可换为"\n")
				"""键1: 值1\n\r键2: 值2\n\r键3: 值3"""
	
	请求方法:
		可选.请求方法=method,具体查看urllib.request.Request函数中参数method
	
	数据:
		可选.上传的数据,本函数内已使用bytes函数将其utf-8编码
	
	cookie:
		可选.要发送的cookie,将会包括在请求头中.若请求头中已有cookie,将会追加在后面,若有重复,则会重复发送
		可传入  字典 列表 字符串  类型,但在本函数中最终都会转为字符串到请求头中:
			字典 类型:
				{"键1":["值1","域1","路径1","过期时间1"],"键2":["值2","域2","路径2","过期时间2"],"键3":["值3","域3","路径3","过期时间3"]}, 即与 "字典的响应cookie" 相同
				或
				{"键1":"值1","键2":"值2","键3":"值3"}

返回值:
	列表:
		字符串的url:
			若进行了重定向,该值可能与参数的url不同

		数字的状态码:
			参见"HTTP状态码"

		字符串的响应头:
			原始的响应头,包括"Set-Cookie"

		字典的响应头:
			整理后的便于程序使用的响应头,不包括"Set-Cookie"

		字符串的响应cookie:
			从响应头"Set-Cookie"中提出的不包括"domain" "path" "expires"的cookie,仅有"键1=值1; 键2=值2; 键3=值3"

		字典的响应cookie:
			从响应头"Set-Cookie"中提出的包括"domain" "path" "expires"的cookie,有 {"键1":["值1","域1","路径1","过期时间1"],"键2":["值2","域2","路径2","过期时间2"],"键3":["值3","域3","路径3","过期时间3"]}

		字符串的响应数据:
			正文内容

'''
	global 访问_暂停
	请求头_={
	'User-Agent':'Ptyhno-lrulib',
	'Accept-Encoding':'gzip',
	'Accept-Language':'zh-CN,zh;q=0.9',
	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}
	if(数据):
		data=bytes(数据,encoding="utf8")
	else:
		data=None
	if(isinstance(请求头,dict)):
		请求头_.update(请求头)
	elif(isinstance(请求头,list)or isinstance(请求头,str)):
		if(isinstance(请求头,str)):
			请求头.split("\n")
			for i in range(len(请求头)):
				if(请求头[i][-1]=="\r"):
					请求头[i]=请求头[i][0:-1]
		for i in 请求头:
			请求头_分割位置=请求头.index(":")
			if(请求头[请求头_分割位置+1]==""):
				请求头_[请求头[0:请求头_分割位置]]=请求头[请求头_分割位置+1:]
			elif(请求头[请求头_分割位置+1]==" "):
				请求头_[请求头[0:请求头_分割位置]]=请求头[请求头_分割位置+2:]

	else:
		raise TypeError("\"请求头\"的类型应为 dict list str 中的其中一种")
	
	url拆分=parse.urlparse(url)
	if(cookie):
		if(not "cookie" in 请求头_):
			请求头_["cookie"]=""
		else:
			请求头_["cookie"]+="; "
		if(isinstance(cookie,dict)):
			for i in cookie:
				if(isinstance(cookie[i],list)):
					if(time.mktime(time.strptime(cookie[i][3][5:-4],"%d-%b-%Y %H:%M:%S"))>time.time()):
						路径正确=False
						域名正确=False
						路径=url拆分.path
						cookie路径=cookie[i][2]
						if(cookie路径[-1]=="/"):
							if(len(路径)>len(cookie路径[0:-1])and 路径[0:len(cookie路径)]==cookie路径):
								路径正确=True
						else:
							if(cookie路径==路径):
								路径正确=True
						

						域名=url拆分.hostname
						cookie域名=cookie[i][1]
						if(cookie域名[0]=="."):
							if(len(cookie域名[1:].split("."))>1 and len(域名)>len(cookie域名[1:])and 域名[-len(cookie域名[1:]):]==cookie域名[1:]and 域名[0:-len(cookie域名[1:])].split(".")[-1]==""):
								域名正确=True
						else:
							if(cookie域名==域名):
								域名正确=True
						
						if(路径正确 and 域名正确):
							请求头_["cookie"]+=i+"="+cookie[i][0]+"; "

				elif(isinstance(cookie[i],str)):
					请求头_["cookie"]+=i+"="+cookie[i]+"; "
				
		elif(isinstance(cookie,list)):
			请求头_["cookie"]+="; ".join(cookie)+"; "
		
		elif(isinstance(cookie,str)):
			请求头_["cookie"]+=cookie+"; "
		else:
			raise TypeError("\"cookie\"的类型应为 dict list str 中的其中一种")


		请求头_["cookie"]=请求头_["cookie"][0:-2]

	url字符="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.~!*'();:@&=+$,/?#[]%"
	for i in url:
		if(not i in url字符):
			raise UnicodeEncodeError("url中包含特殊字符")
	请求=request.Request(url,data=data,headers=请求头_,method=请求方法)
	#"""
	错误_计数=0
	访问_暂停_=True
	while 1:
		if(访问_暂停 and 访问_暂停_):
			time.sleep(0.2)
		else:
			try:
				响应=request.urlopen(请求)
				访问_暂停_=True
				访问_暂停=False
				break
				'''
			except request.URLError as 错误:
				print(repr(错误))
				print(repr(错误).split("(")[0])
				raise
			#'''
			except(request.URLError,request.http.client.HTTPException,request.http.client.NotConnected,request.http.client.InvalidURL,request.http.client.UnknownProtocol,request.http.client.UnknownTransferEncoding,request.http.client.UnimplementedFileMode,request.http.client.IncompleteRead,request.http.client.ImproperConnectionState,request.http.client.CannotSendRequest,request.http.client.CannotSendHeader,request.http.client.ResponseNotReady,request.http.client.BadStatusLine,request.http.client.LineTooLong,request.http.client.RemoteDisconnected) as 错误:
				#print(错误.args[0])
				#if("args" in 错误.args[0]):
				#	print(错误.args[0].args)
				try:
					if(访问_暂停 and 访问_暂停_):
						continue
					else:
						访问_暂停=True
						request.urlopen("https://www.baidu.com",timeout=10)
						raise
				except:
					错误_计数+=1
					if(安静模式_):
						print(" 错误:"+str(错误)+","+str(错误_计数)+"次")
						if(错误_计数>5):
							按任意键继续(" 错误:"+str(错误)+",共"+str(错误_计数)+"次,",提示信息_3='再次重试')
						else:
							time.sleep(3)
					else:
						按任意键继续(" 错误:"+str(错误)+",",提示信息_3='重试')
					访问_暂停_=False
	#"""
	#响应=request.urlopen(请求)

	响应头_原始=str(响应.info())
	响应头_=响应头_原始.split("\n")[0:-2]
	响应头_整理={}
	响应头_cookie_未整理=[]
	响应头_cookie_字符串=""
	响应头_cookie_整理={}
	for i in 响应头_:
		i_=i.split(": ",1)
		if(i_[0]=="Set-Cookie"):
			响应头_cookie_未整理.append(i_[1])
		else:
			响应头_整理[i_[0]]=i_[1]
	
	for i in 响应头_cookie_未整理:
		i_=i.split("; ")
		响应头_cookie_字符串=响应头_cookie_字符串+i_[0]+"; "
		i__=i_[0].split("=")
		i_1={}
		for i2 in i_[1:]:
			i2_=i2.split("=",1)
			if(len(i2_)==2):
				i_1[i2_[0]]=i2_[1]
			else:
				i_1[i2_[0]]=""
		
		响应url_=parse.urlparse(响应.geturl())
		try:
			i_1["domain"]
			if(i_1["domain"][0]!="."):
				i_1["domain"]="."+i_1["domain"]
		except:
			i_1["domain"]=响应url_.hostname
		try:
			i_1["expires"]
		except:
			i_1["expires"]=""
		try:
			i_1["path"]
		except:
			i_1["path"]="/"
		
		响应头_cookie_整理[i__[0]]=[i__[1],i_1["domain"],i_1["path"],i_1["expires"]]
	
	响应头_cookie_字符串=响应头_cookie_字符串[0:-2]
	
	return [响应.geturl(),响应.getcode(),响应头_原始,响应头_整理,响应头_cookie_字符串,响应头_cookie_整理,解码(响应.read())]
	

	
def 解码(输入):
	'''
解码http响应正文或其他 gzip utf-8 gbk 内容

参数:
	输入:
		要解码的数据

返回值:
	解码后的数据

'''
	if(输入[0:2]==b'\x1f\x8b'):
		fileobj=BytesIO(输入)
		输入_=gzip.GzipFile(fileobj=fileobj).read()
		fileobj.close()
	else:
		输入_=输入
	try:return 输入_.decode('utf-8')
	except:return 输入_.decode('gbk')
			

错误信息_信息={}

def 错误信息_(信息):
	global 错误信息_信息
	try:
		错误信息_信息[信息]+=1
	except:
		错误信息_信息[信息]=1
		print(错误信息_信息)

#import getpass
#os.chdir(sys.path[0])
'''
'''


'''
输入_值 = None
def 输入():
	global 输入_值
	输入_值 = 9
	输入_值 = input()
	time.sleep(0.04)
	输入_值 = None

def 密码输入(文字=""):
	global 输入_值
	if(输入_值 == None):
		_thread.start_new_thread(输入,())
		time.sleep(0.1)
	文字长度=int((len(文字.encode('utf-8')) - len(文字))/2 + len(文字))
	while(输入_值 == 9):
		print("\r"+" "*(os.get_terminal_size().columns-5-文字长度),end = "    \r"+文字,flush=True)
		time.sleep(0.002)
	print("\r\t\t\t\t\t\t")
	return 输入_值
'''
def 登录(用户名,密码,保存用户信息=True):
	'''
使用用户名和密码登录 三明安全教育平台

参数:
	用户名:
		要登录的用户名
	
	密码:
		用户名对应的密码
	
	保存用户信息:
		登录成功后是否保存用户信息到 用户数据文件 中

返回值:
	列表:
		cookie:
			登录后网页的"Set-Cookie"的字符串
		
		返回数据_序列化
			登录后经过整理的便于程序使用的网页内容

'''
	global 临时用户数据
	url字符='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
	for i in 用户名+密码:
		if(not i in url字符):
			return ["",{'ret':'-1'}]
	访问结果=访问("https://fujianlogin.xueanquan.com/LoginHandler.ashx?userName="+用户名+"&password="+密码+"&type=login&loginType=1")
	返回数据=访问结果[6].replace("data:{","").replace("ret: 1,","").replace("{","").replace("}","").replace("(","").replace(")","").split(",")
	返回数据_序列化={}
	cookie=访问结果[4]
	for index in 返回数据:
		index=index.replace("'","").split(":")
		返回数据_序列化[index[0]]=index[1]
	#input(cookie)
	if(返回数据_序列化['ret']=='1'and 保存用户信息):
		if(isinstance(临时用户数据,dict)):
			临时用户数据[用户名]=[cookie,返回数据_序列化]
		else:
			try:
				try:
					with open(用户数据文件,"r")as f:data=json.loads(f.read())
				except:
					if(安静模式_):
						print('注意:用户数据文件"'+用户数据文件+'"不正确,将使用临时数据,退出后会丢失')
						临时用户数据={}
					else:
						按任意键继续('注意:用户数据文件"'+用户数据文件+'"不正确,',提示信息_3='尝试重置')
						#f.write("{}")
						data={}
				if(not isinstance(临时用户数据,dict)):
					data[用户名]=[cookie,返回数据_序列化]
					with open(用户数据文件,"w")as f:
						f.write(json.dumps(data,ensure_ascii=False,indent="\t",sort_keys=True))#格式化的json
						#f.write(json.dumps(data,ensure_ascii=False,separators=(',',':')))#压缩的json
			except:
				if(安静模式_):
					print('注意:用户数据文件"'+用户数据文件+'"不能写入,已跳过,请检查是否有写权限')
			
		
		
	return [cookie,返回数据_序列化]

def 查询已完成作业(cookie):
	'''
"查询作业"的子函数
查询用户在 三明安全教育平台 中已的完成作业

参数:
	cookie:
		"登录"得到的"cookie"

返回值:
	字典:
		字符串的作业id:字符串类型的完成时间

'''
	访问结果=访问("https://sanming.xueanquan.com/JiaTing/CommonHandler/MyHomeWork.ashx?method=myhomeworkinfo",cookie=cookie)
	返回数据=json.loads(访问结果[6])
	已完成作业={}
	if(返回数据["WinterInfo"]["Status"]):
		已完成作业[1]=返回数据["WinterInfo"]["FinishTime"]
	if(返回数据["SummerInfo"]["Status"]):
		已完成作业[2]=返回数据["SummerInfo"]["FinishTime"]
	for index in 返回数据["FinishInfo"]:
		已完成作业[index["WorkId"]]=index["FinishTime"]
	已完成作业2={}
	for index in 已完成作业:
		已完成作业2[str(index)]=已完成作业[index].replace("T"," ")
	return 已完成作业2

def 查询所有作业(grade,classroom,citycode):
	'''
"查询作业"的子函数
查询用户在 三明安全教育平台 中所有的作业

参数:
	grade:
		年级,"登录"得到的"返回数据_序列化"中的"grade"
	
	classroom:
		班级,"登录"得到的"返回数据_序列化"中的"classroom"
	
	citycode:
		城市代码,"登录"得到的"返回数据_序列化"中的"citycode"

返回值:
	字典:
		字符串的作业id:
			列表:
				作业标题
				作业类型
				布置时间
				完成时间: 暂时为None,在"查询作业"中会与"查询已完成作业"的结果合并为完成时间,若未完成则仍为None
				作业showhdtcbox: 网页中作业的"showhdtcbox"的信息,在"完成安全学习"会用到

'''
	访问结果=访问("https://file.safetree.com.cn/webapi.fujian/jt/MyHomeWork.html?grade="+grade+"&classroom="+classroom+"&cityid="+citycode)
	#响应头=str(response.info()).split("\n")
	返回数据=访问结果[6].replace("');document.writeln('","").split('tr>')
	#print(返回数据)
	作业={}
	aa=0
	for 一项作业_乱 in 返回数据:
		aa+=1
		if(一项作业_乱[-1]=="/"and "title"in 一项作业_乱):
			if("专题活动"in 一项作业_乱):
				类型=一项作业_乱.split("\\")[1][1:]
			elif("安全学习"in 一项作业_乱):
				类型=1
			else:
				类型=2			
			#以双引号拆分字符串
			一项作业_引号分割=一项作业_乱.split('"')
			aaa=0
			标题=""
			for 作业信息_引号分割 in 一项作业_引号分割:
				if(作业信息_引号分割[-6:]=="title="):
					标题 = 一项作业_引号分割[aaa+1]
				elif(作业信息_引号分割[-9:]=="<td name="):
					作业id = 一项作业_引号分割[aaa+1][15:]
				aaa+=1
			布置时间=""
			
			一项作业_表格分割=一项作业_乱.split('td>')
			#以表格标签拆分字符串
			for 作业信息_表格分割 in 一项作业_表格分割:
				#获取日期
				if(作业信息_表格分割[0:32]=="                                "and 作业信息_表格分割[36:37]=="-"and 作业信息_表格分割[39:40]=="-"):
					布置时间=作业信息_表格分割[32:42]
			作业showhdtcbox位置=一项作业_乱.index('onclick=" showhdtcbox(')+22
			作业showhdtcbox=json.loads("["+一项作业_乱[作业showhdtcbox位置:一项作业_乱.index(')',作业showhdtcbox位置)].replace("\\'",'"')+"]")
			try:作业[作业id]=[标题,类型,布置时间,None,作业showhdtcbox]
			except:pass
	
	try:
	#if(1):
		##寒暑假专题链接插入
		#寒暑假专题信息插入
		try:作业["1"][1]="寒假专题"
		except KeyError:''
		#else:
			#寒假专题链接位置=返回数据[0].index('(sporttype == 1) {                    window.open("//huodong." + host.join(\\\'.\\\') + ')+84
			#作业["1"][1]="https://huodong.xueanquan.com"+返回数据[0][寒假专题链接位置:寒假专题链接位置+80].split('"')[1]
		try:作业["2"][1]="暑假专题"
		except KeyError:''
		#else:
			#暑假专题链接位置=返回数据[0].index('(sporttype == 2) {                    window.open("//huodong." + host.join(\\\'.\\\') + ')+84
			#作业["2"][1]="https://huodong.xueanquan.com"+返回数据[0][暑假专题链接位置:暑假专题链接位置+80].split('"')[1]
	except:''#print("警告:寒暑假专题链接获取失败")
	return 作业

def 查询作业(cookie,返回数据_序列化):
	'''
查询用户在 三明安全教育平台 中已完成和所有作业

参数:
	cookie:
		"登录"得到的"cookie"
	
	返回数据_序列化:
		"登录"得到的"返回数据_序列化"

返回值:
	字典:
		字符串的作业id:
			列表:
				作业标题
				作业类型
				布置时间
				完成时间:若未完成则为None
				作业showhdtcbox: 网页中作业的"showhdtcbox"的信息,在"完成安全学习"会用到

'''
	#print(返回数据_序列化)
	所有作业=查询所有作业(返回数据_序列化["Grade"],返回数据_序列化["ClassRoom"],返回数据_序列化["CityCode"])
	已完成作业=查询已完成作业(cookie)
	for 作业id in 所有作业:
		if(作业id in 已完成作业):
			#所有作业[作业id].append(已完成作业[作业id])
			所有作业[作业id][3]=已完成作业[作业id]
		else:
			#print(作业id)
			#所有作业[作业id].append(0)
			所有作业[作业id][3]=0
	return 所有作业

def 完成安全学习(cookie,返回数据_序列化,workid,showhdtcbox):
	'''
完成用户在 三明安全教育平台 中的一项作业

参数:
	cookie:
		"登录"得到的"cookie"

	返回数据_序列化:
		"登录"得到的"返回数据_序列化"
	
	workid:
		在"查询作业"或"查询所有作业"中得到的"作业id"

	showhdtcbox:
		在"查询作业"或"查询所有作业"中得到的"showhdtcbox"

返回值:
	提示信息或1,若为1则已完成

'''
	请求头={"cookie":cookie}

	作业信息=访问("https://sanming.xueanquan.com/JiaTing/EscapeSkill/SeeVideo.aspx?gid="+str(showhdtcbox[3])+"&li="+str(showhdtcbox[0]),请求头)[6]
	#print(作业信息)
	作业信息_有用部分_位置=作业信息.index("SeeVideo.TemplateIn2(")+21
	作业信息_有用部分=作业信息[作业信息_有用部分_位置:作业信息.index(")",作业信息_有用部分_位置)].replace('"','').replace("'",'').replace(" ",'').split(",")
	
	作业信息_videoid_位置=作业信息.index("SeeVideo.SkillCheckName(")+24
	作业信息_videoid=作业信息[作业信息_videoid_位置:作业信息_videoid_位置+9].split('"')[1]

	作业信息_testID_位置=作业信息.index("SeeVideo.TestPaperlistGet(")+26
	作业信息_testID=作业信息[作业信息_testID_位置:作业信息_testID_位置+9].split('"')[1]
	#input(作业信息_videoid)
	#return 作业信息_有用部分
	
	#(workid,	fid,	title,			require,	purpose,	contents,	testwanser,			testinfo,				testMark,		testReulst,	SiteName,		siteAddrees,	watchTime,	CourseID,callback,context)
	#"466032", 	"912", 	"关注饮食安全", ""		,	"",			"",			testanswer="0|0|0",	testinfo="已掌握技能",	testMark=100,	1,			WcContent="",	"",				"",			"1336"

	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=CourseAllGet&_session=rw",请求头,"POST","gid="+str(showhdtcbox[3]))
	
	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=I_VideoGet&_session=rw",请求头,"POST","gradeid="+str(showhdtcbox[3]))
	
	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=SkillCheckName&_session=rw",请求头,"POST","videoid="+str(作业信息_videoid)+"\x0d\x0agradeid="+str(showhdtcbox[3])+"\x0d\x0acourseid="+作业信息_有用部分[13])

	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=AllSituation&_session=rw",请求头,"POST","gradeid="+str(返回数据_序列化["Grade"]))
	#print(.decode("utf-8"))
	
	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=VideoDetailInfoGet&_session=rw",请求头,"POST","Vid="+str(作业信息_videoid)+"\x0d\x0acourseid="+作业信息_有用部分[13]+"\x0d\x0acourseid="+作业信息_有用部分[13])
	#'''
	TestPaperlistGet=json.loads(访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=TestPaperlistGet&_session=rw",请求头,"POST","testID="+str(作业信息_testID))[6].replace("'",'"'))
	
	qID=""
	for i in TestPaperlistGet["Rows"]:
		qID+=str(i["id"])+","
	qID=qID[0:-1]
	#print(qID)
	访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=TestPaperThreelistGet2&_session=rw",请求头,"POST","qID="+qID)
	#'''
	data = [
	#"workid="+str(workid),
	"workid="+作业信息_有用部分[0],
	"fid="+作业信息_有用部分[1],
	"title="+作业信息_有用部分[2],
	"require="+作业信息_有用部分[3],
	"purpose="+作业信息_有用部分[4],
	"contents="+作业信息_有用部分[5],
	"testwanser=0|0|0",
	"testinfo=已掌握技能",
	"testMark=100",
	"testReulst="+作业信息_有用部分[9],
	"SiteName="+作业信息_有用部分[10],
	"siteAddrees="+作业信息_有用部分[11],
	"watchTime="+作业信息_有用部分[12],
	"CourseID="+作业信息_有用部分[13]
	]
	data2 = ""
	for index in data:
		data2 += "\x0d\x0a"+index
	
	#res = request.Request("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=TemplateIn2&_session=rw",data=bytes(data2,encoding="utf8"),headers=headers,method="GETUCodeStr")
	访问结果=访问("https://sanming.xueanquan.com/jiating/ajax/FamilyEduCenter.EscapeSkill.SeeVideo,FamilyEduCenter.ashx?_method=TemplateIn2&_session=rw",请求头,"POST",data2)
	
	返回数据=访问结果[6]
	#返回数据 = response.read()
	#print(返回数据)
	if(返回数据=="'4'"or 返回数据=="'1'"):
		return 1
	else:
		#以下提示信息来自"安全教育平台"
		if(返回数据 == "'-4'"):
			return "正在操作中，请勿重复提交"
		elif(返回数据 == "'-2'"):
			return "不能提前参加下半学年的训练"
		elif(返回数据 == "'-5'"):
			return "您不是学生用户，不参与测试记录"
		else:
			#这个不是"安全教育平台"的信息
			return "意外的返回信息:"+str(返回数据)


def 获取专题id(url,作业id):
	'''
获取"三明安全教育平台"的"专题活动"的id
获取时,会先检查本地文件,若没有,则从url对应的网页获取,若仍失败,则从github的项目中获取,若仍失败,则返回0.获取成功后,会保存到本地文件,之后该专题id只需在文件中检查

参数:
	url:
		该专题页面的url
	
	作业id:
		该专题的作业id

返回值:
	专题id

'''

	global 临时专题id
	try:
	#if 1:
		if(isinstance(临时专题id,dict)):
			数据=临时专题id
		else:
			with open(专题id文件,"r")as f:数据=json.loads(f.read())
	except:
		if((not isinstance(临时专题id,dict))and 临时专题id!=False):
			print('注意:"专题id文件'+专题id文件+'"不正确')
	
	else:
		try:
			return str(数据[str(作业id)])
		except:
			pass

	
	if(安静模式_ and 作业id in 发生错误["获取专题id"]):
		return 0
			
	if(not 安静模式):
		print("未记录的id,通过网络获取")
	#获取专题id_网页 要封装为函数是因为可能需要重复调用
	专题id=获取专题id_网页(url)
	if(not 专题id):
		数据_=获取文件("%E6%95%B0%E6%8D%AE/%E4%B8%93%E9%A2%98id%E8%A1%A8.json","json")
		if(数据_ is None):
			return 0
		try:
			专题id=数据_[str(作业id)]
		except:
			if(安静模式_):
				发生错误["获取专题id"][作业id]="获取错误"
			if(not 安静模式):
				print("获取id失败")
				return 0
	if(isinstance(临时专题id,dict)):
		临时专题id[str(作业id)]=专题id
	else:
		try:
			with open(专题id文件,"r")as f:文件数据=json.loads(f.read())
		except:
			专题id文件_使用临时数据=False
			if(安静模式_):
				专题id文件_使用临时数据=True
				
				
			else:
				#按任意键继续('注意:"专题id文件'+专题id文件+'"不正确,',提示信息_3='尝试重置')
				if(input('注意:"专题id文件'+专题id文件+'"不正确,输入 "y"(小写) 并回车尝试重置,输入其他并回车则使用临时数据:')=='y'):
					文件数据={}
				else:
					专题id文件_使用临时数据=True
			
			if(专题id文件_使用临时数据):
				print('注意:"专题id文件'+专题id文件+'"不正确,将使用临时数据,退出后会丢失')
				
				临时专题id={}
				临时专题id[str(作业id)]=专题id

		if(not isinstance(临时专题id,dict)):
			文件数据[str(作业id)]=专题id
			try:
				with open(专题id文件,"w") as f:f.write(json.dumps(文件数据,ensure_ascii=False,indent="\t",sort_keys=True))
			except:
				if(安静模式_):
					临时专题id=文件数据
				else:
					input('注意:"专题id文件'+专题id文件+'"不能写入,已跳过,请检查是否有写权限,要写入的内容:\n'+json.dumps(文件数据,ensure_ascii=False,indent="\t",sort_keys=True)+"\n你可以将以上信息手动写入")
				文件数据={}
	return 专题id


def 获取专题id_网页(url,跳转=0):
	'''
"获取专题id"的子函数
"获取专题id_网页"的子函数.有些网页要跳转,将跳转后的url传给"获取专题id_网页"
从网页获取"三明安全教育平台"的"专题活动"的id

参数:
	url:
		该专题页面的url
	
	跳转:
		可选.若该函数是自身调用,则会传入该参数,用于跳转次数过多停止

返回值:
	"专题id"或0,若为0即获取失败

'''
	if(跳转>10):
		return 0
	访问结果=访问(url)
	返回数据=访问结果[6]
	if("window.location.href" in 返回数据 and "<title>跳转中...</title>" in 返回数据):
		#部分专题需跳转
		url2位置=返回数据.index("window.location.href")+21
		#res2 = request.Request("https:"+返回数据[url2位置:url2位置+70].split("'")[1],method="GET")
		#response2 = request.url2open(res2)
		#返回数据 = response2.read().decode("utf-8")
		url2=返回数据[url2位置:url2位置+70].split("'")[1]
		if(url2[0:2]=="//"):
			url2="https:"+url2
		elif(url2[0:4]=="http"):
			''
		else:
			url2="https://"+url2
		if(url2[-11:]=="/index.html"):
			try:return 获取专题id_网页(url2[0:-11]+"/huodong.html")
			except:return 获取专题id_网页(url2[0:-11]+"/shipin.html")
		
		if(not 安静模式):
			print("跳转到"+url2)
		return 获取专题id_网页(url2,跳转+1)
	#print(返回数据)
	id位置=返回数据.index("data-specialId")+15
	return 返回数据[id位置:id位置+10].split('"')[1]

专题数据={}

def 完成专题活动(cookie,返回数据_序列化,specialId):
	'''
完成用户在 三明安全教育平台 中的一项普通专题

参数:
	cookie:
		"登录"得到的"cookie"
	
	返回数据_序列化:
		"登录"得到的"返回数据_序列化"

	专题id:
		"获取专题id"得到的"专题id"

返回值:
	0或1. 0为未完成,1为已完成

'''
	if(not specialId):

		return "不能获取专题id"
	specialId=str(specialId)
	
	if(specialId in 专题数据):
		数据=专题数据[specialId]
	else:
		try:
			with open(数据文件目录+specialId+".json","r",encoding="utf-8")as f:数据=json.loads(f.read())
		#try:''
		except:
			if(not 安静模式):
				print('专题未记录,从github获取')
			#return "文件\""+specialId+".json\"读取错误"
		数据=获取文件("%E6%95%B0%E6%8D%AE/"+specialId+".json","json")
		if(数据 is None):
			if(not 安静模式):
				print('获取失败')
			return 0
			try:
				with open(数据文件目录+specialId+".json","w",encoding="utf-8")as f:f.write(json.dumps(数据))
			except:
				if(not 安静模式):
					print("注意:\""+specialId+"\"不能写入")
		专题数据[specialId]=数据
	
	#完成状态=1
	请求头={
		"Cookie":cookie,
		"content-type":"application/json",
	}
	专题点击url="https://huodongapi.xueanquan.com/p/fujian/Topic/topic/platformapi/api/v1/records/sign"
	专题问卷url="https://huodongapi.xueanquan.com/Topic/topic/main/api/v1/records/survey"
	for index in 数据:
		if(数据[index]=="sign"):
			返回数据=访问(专题点击url,请求头,"POST","{specialId:"+specialId+", step:"+index+"}")[6]
		elif(str(type(数据[index]))=="<class 'list'>"):
			数据_替换=[]
			for index2 in 数据[index]:
				if("answer" in index2 and index2["answer"][0:5]=="用户_性别"):
					选项=json.loads(index2["answer"][5:].replace("'",'"'))
					if(返回数据_序列化["Sex"]=="1"):#男
						index2["answer"]=选项["男"]
					elif(返回数据_序列化["Sex"]=="2"):#女
						index2["answer"]=选项["女"]
					else:
						index2["answer"]=""
				数据_替换.append(index2)
			返回数据=访问(专题问卷url,请求头,"POST",json.dumps({"user":{"userID":"0","userName":返回数据_序列化["UserName"],"trueName":返回数据_序列化["TrueName"],"regionalAuthority":返回数据_序列化["regionalAuthority"],"userType":"Users","prvCode":返回数据_序列化["PrvCode"],"cityCode":返回数据_序列化["CityCode"],"schoolId":返回数据_序列化["SchoolID"],"schoolName":返回数据_序列化["SchoolName"],"grade":返回数据_序列化["Grade"],"classRoom":返回数据_序列化["ClassRoom"],"comeFrom":返回数据_序列化["ComeFrom"]},"UserAnswers":数据[index],"specialId":specialId,"step":index},ensure_ascii=False))[6]
			返回数据=访问(专题点击url,请求头,"POST","{specialId:"+specialId+", step:"+index+"}")[6]
		#if(not 返回数据["result"]):
		#	完成状态=0
	完成状态=json.loads(访问("https://huodongapi.xueanquan.com/p/fujian/Topic/topic/platformapi/api/v1/records/finish-status?specialId="+specialId,请求头)[6])
	if(完成状态["finishStatus"]):
		return 1
	else:
		return 0

def 完成寒暑假专题活动(cookie,返回数据_序列化,专题布置时间):
	'''
完成用户在 三明安全教育平台 中的一项寒暑假专题

参数:
	cookie:
		"登录"得到的"cookie"
	
	返回数据_序列化:
		"登录"得到的"返回数据_序列化"

	专题布置时间:
		"查询作业"得到的"布置时间"

返回值:
	0或1. 0为未完成,1为已完成

'''
	try:
		with open(数据文件目录+专题布置时间+".txt","r")as f:数据=json.loads(f.read())
	#try:''
	except:return "文件\""+专题布置时间+".txt\"读取错误"
	else:
		请求头={
			"Cookie":cookie,
			"content-type":"application/json",
		}
		
		#return 返回数据
		完成状态=1
		for index in 数据:
			try:index["url"]
			except KeyError:index["url"]="https://huodongapi.xueanquan.com/p/fujian/Topic/topic/platformapi/api/v1/holiday/sign"
			try:index["data"]=json.dumps(index["data"])
			except KeyError:return "文件\""+专题布置时间+".txt\"的\""+index+"\"中缺少\"data\"参数"
			except:pass
			访问结果=访问(index["url"],请求头,"POST",index["data"])
			返回数据=json.loads(访问结果[6])
			if(not 安静模式):
				print(返回数据)
			if(not 返回数据["result"]):
				完成状态=0
	if(完成状态):
		return 1
	else:
		return 0


def 登录_(用户名="",密码="",保存用户信息=True):
	'''
比"登录"更人性化的登录(真正的登录还是调用"登录",因此 返回值 与"登录"相同)
可传入参数,也可直接调用,直接调用有交互式的用户名和密码输入,传入参数不会有交互式提示
若没有传入或输入密码,则会检查是否已保存在"用户数据文件"中,再尝试简单的密码:"123456","123456首字母","首字母123456" 在下面的"弱密码列表"中

参数:
	用户名:
		要登录的用户名
	
	密码:
		用户名对应的密码
	
	保存用户信息:
		登录成功后是否保存用户信息到 用户数据文件 中

返回值:
	列表:
		cookie:
			登录后网页的"Set-Cookie"的字符串
		
		返回数据_序列化
			登录后经过整理的便于程序使用的网页内容
	或
	False:
		当用户不输入用户名时返回False

'''
	自动=False
	用户信息=["",{'ret':'-1'}]
	if(用户名==""and 密码!=""):
		return 用户信息
	if(isinstance(临时用户数据,dict)):
		data=临时用户数据
	else:
		try:
			with open(用户数据文件,"r")as f:
				try:
					data=json.loads(f.read())
				except:
					if(not 安静模式_):
						print('注意:用户数据文件"'+用户数据文件+'"不正确')
		except:data=0
	while((not 自动)and 用户信息[1]['ret']=='-1'):
		if(用户名!=""):
			自动=True
		if(not 自动):
			#print('-'*18)
			用户名=input("用户名:")
		
		if(not 用户名):
			return False
		
		if(not 自动):
			密码=密码输入()
			time.sleep(0.08)
		if(not 密码):
				
			try:data[用户名]
			except:
				
				#弱密码登录
				#简单首字母运算
				拼音=用户名.strip('0123456789')
				首字母=''
				a=1
				while(a<=len(拼音)):
					if(拼音[a-1:a+1]=="zh" or 拼音[a-1:a+1]=="ch" or 拼音[a-1:a+1]=="sh"):
						首字母+=拼音[a-1:a]
						a+=2
						
					elif(拼音[a-1:a]=="b" or 拼音[a-1:a]=="p" or 拼音[a-1:a]=="m" or 拼音[a-1:a]=="f" or 拼音[a-1:a]=="d" or 拼音[a-1:a]=="t" or 拼音[a-1:a]=="l" or 拼音[a-1:a]=="k" or 拼音[a-1:a]=="h" or 拼音[a-1:a]=="j" or 拼音[a-1:a]=="q" or 拼音[a-1:a]=="w" or 拼音[a-1:a]=="y" or 拼音[a-1:a]=="r" or 拼音[a-1:a]=="x" or 拼音[a-1:a]=="z" or 拼音[a-1:a]=="c" or 拼音[a-1:a]=="s"):
						首字母+=拼音[a-1:a]
						a+=1
					elif((拼音[a-1:a]=="g" or 拼音[a-1:a]=="n")and a<len(拼音) and not(拼音[a:a+1]=="b" or 拼音[a:a+1]=="p" or 拼音[a:a+1]=="m" or 拼音[a:a+1]=="f" or 拼音[a:a+1]=="d" or 拼音[a:a+1]=="t" or 拼音[a:a+1]=="l" or 拼音[a:a+1]=="k" or 拼音[a:a+1]=="h" or 拼音[a:a+1]=="j" or 拼音[a:a+1]=="q" or 拼音[a:a+1]=="w" or 拼音[a:a+1]=="y" or 拼音[a:a+1]=="r" or 拼音[a:a+1]=="x" or 拼音[a:a+1]=="z" or 拼音[a:a+1]=="c" or 拼音[a:a+1]=="s" or 拼音[a:a+1]=="g" or 拼音[a:a+1]=="n")):
						首字母+=拼音[a-1:a]
						a+=1
					else:
						a+=1
				
				#print("首字母:"+首字母)
				弱密码列表=[
					"123456",
					"123456"+首字母,
					首字母+"123456",
				]
				a=0
				for index in 弱密码列表:
					a+=1
					if(not 安静模式_):
						print("尝试"+str(a)+"/"+str(len(弱密码列表))+"个",end="\r",flush=True)
					用户信息=登录(用户名,index,保存用户信息)
					if(用户信息[1]['ret']=='-1'):
						''
						#print("尝试'"+index+"'失败")
					else:
						if(not 安静模式_):
							print("登录成功\t\t")
						break
				if(用户信息[1]['ret']=='-1'and not 安静模式_):
					print("登录失败\t\t")
			else:
				if(not 安静模式_):
					print("使用已保存的用户信息")
				用户信息=[data[用户名][0],data[用户名][1]]
		else:
			用户信息=登录(用户名,密码,保存用户信息)
			if(用户信息[1]['ret']=='-1'):
				if(安静模式_):
					print("注意:\""+用户名+"\"用户名或密码错误")
				else:
					print("用户名或密码错误")
			elif(not 安静模式_):
				print("登录成功")
		
		用户名=""
	return 用户信息

def 自动完成(用户信息=["",{'ret':'-1'}],自动=False):
	'''
快速完成用户在 三明安全教育平台 中的所有未完成作业(不保证一定完成)

参数:
	用户信息:
		"登录"时得到的列表,即[cookie,返回数据_序列化]

	自动:
		可无人值守,自动跳过已知异常

返回值:
	0或1. 0为未完成,1为已完成

'''
	if(用户信息[1]['ret']=='-1'):
		if(自动):
			return 0
		用户信息=登录_()
	if(isinstance(用户信息,bool)and 用户信息==False):
		return False
	if(用户信息[1]['ret']=='-1'):
		print("错误:登录失败")
		return 0
	if(用户信息[1]["UserType"]!="0"):
		print("错误:非学生账号不能完成")
		return 0
	#print("当前帐号:"+用户信息[1]["UserName"])
	作业=查询作业(用户信息[0],用户信息[1])
	#print(作业)
	成功完成作业=1
	完成作业=0
	for 作业id in 作业:
		if(not 作业[作业id][3]and 作业[作业id][4][4]!=0):
		#if(1):
			完成作业=1
			#成功完成作业=1
			返回数据=0
			if(1):
			#try:
				if(作业[作业id][1] == 1):
					#安全学习
					if(not 安静模式):
						print("尝试完成安全学习\""+作业[作业id][0]+"\"")
					返回数据=完成安全学习(用户信息[0],用户信息[1],作业id,作业[作业id][4])
				
				elif(作业[作业id][1]=="寒假专题" or 作业[作业id][1]=="暑假专题"):
					返回数据=完成寒暑假专题活动(用户信息[0],用户信息[1],作业[作业id][2])
					
				elif(作业[作业id][1]!=3):
					#专题活动
					if(not 安静模式):
						print("尝试完成专题活动\""+作业[作业id][0]+"\"")
					返回数据=完成专题活动(用户信息[0],用户信息[1],获取专题id(作业[作业id][1],作业id))
			#except:print("发生错误")
			if(not 安静模式):
				if(返回数据==1):
					print("已完成\""+作业[作业id][0]+"\"\t\t\t\t\t\t")
				else:
					print("未完成\""+作业[作业id][0]+"\",信息:"+str(返回数据)+"\t\t\t\t\t\t")
					成功完成作业=0
	if((not 完成作业)and(not 安静模式)):
		print("没有未完成的作业")
	if(成功完成作业):
		return 1
	return 0


def 显示作业列表(用户信息=["",{'ret':'-1'}]):
	'''
列出用户在 三明安全教育平台 中的所有作业,可选择完成

参数:
	用户信息:
		"登录"时得到的列表,即[cookie,返回数据_序列化]

'''
	清屏()
	if(用户信息[1]['ret']=='-1'):
		用户信息=登录_()
	if(isinstance(用户信息,bool)and 用户信息==False):
		return False
	while 1:
		按任意键继续()
		清屏()
		#print('-'*18)
		print("用户名:"+用户信息[1]["UserName"]+"\n")
		作业=查询作业(用户信息[0],用户信息[1])
		print("作业id\t类型    \t布置时间\t完成时间\t\t标题\n")
		for 作业id in 作业:
			#作业id
			作业_输出=作业id+"\t"
			#类型
			if(作业[作业id][1]==1):
				作业_输出+="安全学习"
			elif(作业[作业id][1]==2):
				作业_输出+="未知    "
			else:
				作业_输出+="专题活动"
			#布置时间
			作业_输出+="\t"+作业[作业id][2]+"\t"
			#完成时间
			if(作业[作业id][3]):
				作业_输出+=作业[作业id][3]
			else:
				作业_输出+="未完成                "
			#标题
			已结束=""
			if(作业[作业id][4][4]==0):
				已结束="(已结束)"
			作业_输出+="\t"+已结束+作业[作业id][0]
			print(作业_输出)
			
		输入=input("输入作业id以尝试完成:")
		if(输入 in 作业):
			'''
			if(作业[输入][3]):
				print("该作业已完成,无需再完成")
			elif(作业[输入][4][4]==0):
				print("该作业已结束,不能完成")
			else:
			#'''
			if(1):
				作业id=输入
		elif(输入==""):
			break
		else:
			print("输入错误,请重新输入")
			continue
			
		#try:
		if 1:
			if(作业[作业id][1] == 1):
				#安全学习
				print("尝试完成安全学习\""+作业[作业id][0]+"\"")
				返回数据=完成安全学习(用户信息[0],用户信息[1],作业id,作业[作业id][4])
			
			elif(作业[作业id][1]=="寒假专题" or 作业[作业id][1]=="暑假专题"):
				返回数据=完成寒暑假专题活动(用户信息[0],用户信息[1],作业[作业id][2])
				
			elif(作业[作业id][1]!=3):
				#专题活动
				print("尝试完成专题活动\""+作业[作业id][0]+"\"")
				返回数据=完成专题活动(用户信息[0],用户信息[1],获取专题id(作业[作业id][1],作业id))
		'''
		except:
			print("发生错误")
			返回数据=0
		#'''
		if(返回数据==1):
			print("已完成\""+作业[作业id][0]+"\"")
		else:
			print("未完成\""+作业[作业id][0]+"\",信息:"+str(返回数据))
		#input("按回车键继续")


已完成数=0
打印信息_长度=0

def 使用用户名密码完成__(用户名,密码,总数):
	'''
"使用用户名密码表完成"函数调用时多线程使用的子函数,不建议单独调用

'''
	global 已完成数,未完成表,未完成表_其他错误,未完成表_密码错误
	global 打印信息_长度
	完成状态=False
	
	try:完成状态=自动完成(登录_(用户名,密码),True)
	except:pass
	已完成数+=1
	
	填充空白=打印信息_长度-len(str(用户名))
	print("\r"+"   第\t"+str(已完成数)+"\t个,共\t"+str(总数)+"\t个\t"+str(已完成数*100/总数)[:5]+"%"+"\t"+str(用户名)+" "*填充空白+"\b"*填充空白,end='',flush=True)
	打印信息_长度=len(str(用户名))

	
	if(not 完成状态):
		未完成表.append(用户名)
		if(完成状态 is False):
			未完成表_其他错误.append(用户名)
		else:
			未完成表_密码错误.append(用户名)
	


def 保存临时数据():
	'''
保存临时数据,包括 专题id文件 和 用户数据文件


'''
	try:
		临时用户数据
	except:
		临时用户数据={}
	
	try:
		临时专题id
	except:
		临时专题id={}
	
	if((not 临时用户数据)and(not 临时专题id)):
		print('目前 "临时用户数据" 和 "临时专题id" 都是空的,因此此操作只会按原样写入文件,可检测写入是否正常')

	try:
		with open(用户数据文件,"r")as f:临时用户数据.update(json.loads(f.read()))
	except:pass
	
	try:
		with open(专题id文件,"r")as f:临时专题id.update(json.loads(f.read()))
	except:pass

	try:
		with open(专题id文件,"w")as f:f.write(json.dumps(临时专题id,ensure_ascii=False,indent="\t",sort_keys=True))
	except:
		print('注意:专题id文件保存失败')
	
	try:
		with open(用户数据文件,"w")as f:f.write(json.dumps(临时用户数据,ensure_ascii=False,indent="\t",sort_keys=True))
	except:
		print('注意:用户数据文件保存失败')

	if(not 安静模式_):
		print('完成')


线程数=10


def 使用用户名密码表完成(表,保存表=True,保存表_文件名=None,打印未完成=True):
	'''
使用包含用户名和密码的表完成这些用户的所有作业
已使用多线程,可更改"线程数"来调整最大线程数

参数:
	表:
		包含用户名和密码的字典
		{"用户名1":"密码1","用户名2":"密码2"}

返回值:
	列表
		未完成表:
			没有完成的用户名列表
		未完成表_其他错误:
			因发生错误而不能完成的的用户名列表
			一般是因为网络错误,少数是因为程序错误.若能浏览器正常地"访问三明安全教育平台",却出现大片其他错误,则说明这些方法已不适用
		未完成表_密码错误:
			因密码错误而不能完成的的用户名列表

'''
	if(not 表):
		return
	global 已完成数,未完成表,未完成表_其他错误,未完成表_密码错误
	global 临时用户数据,临时专题id
	global 安静模式,安静模式_
	global 打印信息_长度
	a=0

	安静模式2=安静模式
	安静模式2_=安静模式_

	安静模式=True
	安静模式_=True
	已完成数=0
	未完成表=[]
	未完成表_其他错误=[]
	未完成表_密码错误=[]
	
	打印信息_长度=6
	
	try:
		with open(用户数据文件,"r")as f:临时用户数据=json.loads(f.read())
	except:临时用户数据={}
	
	try:
		with open(专题id文件,"r")as f:临时专题id=json.loads(f.read())
	except:临时专题id={}
	
	if(保存表):
		保存表_内容=""
		for i in 表:
			保存表_内容+=i+"\n"
		try:
			if(保存表_文件名):
				保存表_文件名=str(保存表_文件名)
			else:
				时间=time.time()
				保存表_文件名=time.strftime("%Y%m%d-%H%M%S",time.localtime(时间))+"."+str(时间).split(".")[1]
			with open(用户表文件目录+保存表_文件名+".txt","w") as f:
				f.write(保存表_内容)
		except:
			print("注意:用户表保存失败")
	
	print("\r 第\t0\t个,共\t"+str(len(表))+"\t个\t0%\t准备中",end='',flush=True)
	for index in 表:
		a+=1
		#print()
		while(已完成数<a-线程数):
			time.sleep(0.1)
		_thread.start_new_thread(使用用户名密码完成__,(index,表[index],len(表)))
		time.sleep(0.2)
	while(已完成数<len(表)):
		time.sleep(0.2)
	
	#print()
	print("\r 成功\t"+str(len(表)-len(未完成表))+"\t个,共\t"+str(len(表))+"\t个\t"+" "*(打印信息_长度+8))
	
	try:
		with open(专题id文件,"w")as f:f.write(json.dumps(临时专题id,ensure_ascii=False,indent="\t",sort_keys=True))
	except:
		print('注意:专题id文件保存失败')
	
	try:
		with open(用户数据文件,"w")as f:f.write(json.dumps(临时用户数据,ensure_ascii=False,indent="\t",sort_keys=True))
	except:
		print('注意:用户数据文件保存失败')
		
	if(打印未完成):
		if(未完成表):
			print('未完成列表:')
			for i in 未完成表:
				print('\t',end='')
				print(i)
			if(未完成表_其他错误 and not 未完成表_密码错误):
				print("这些都是因其他错误而未完成的")
			if(未完成表_密码错误 and not 未完成表_其他错误):
				print("这些都是因密码错误而未完成的")
			if(未完成表_其他错误 and 未完成表_密码错误):
				print("\n\n其中\n\n")
				print("因其他错误而未完成的有:")
				for i in 未完成表_其他错误:
					print('\t',end='')
					print(i)
				print()
				print("因密码错误而未完成的有:")
				for i in 未完成表_密码错误:
					print('\t',end='')
					print(i)
		else:
			print("已全部完成")
	#未完成表.sort()
	安静模式=安静模式2
	安静模式_=安静模式2_
	return [未完成表,未完成表_其他错误,未完成表_密码错误]



def 使用管理员用户获取学生表(管理员用户信息):
	'''
获取管理员名下的所有学生

参数:
	管理员用户信息:
		使用管理员的"用户名"和"密码"在"登录"得到的"用户信息"

返回值:
	用户信息_表:
		学生账号的字典:
			账号:
				列表:
					学生id
					姓名
					重置密码地址

'''
	if(管理员用户信息[1]["UserType"]!="1"):
		return 0
	
	访问结果=访问("https://sanming.xueanquan.com/eduadmin/ClassManagement/ClassManagement",{"Cookie":管理员用户信息[0]},"POST","status=&keywords=&pageNum=1&numPerPage=2500&orderField=&orderDirection=DESC&TrueName=")
	a=访问结果[6]
	学生账号信息_表格部分_拆分=a[a.index("<tbody>")+7:a.index("</tbody>")].replace("  ","").replace("</tr>","").replace("\r\n","").split("<tr")[1:]

	用户信息_表={}

	for index in 学生账号信息_表格部分_拆分:
		index_拆分=index.split("<td")
		index_rel=index_拆分[0][index.index("rel"):].split('"',3)[1]
		学生id,账号=index_rel.split('/')
		姓名=index_拆分[2].split('>')[1].split('<')[0]
		重置密码地址="https://sanming.xueanquan.com"+index_拆分[5].split("href")[1].split('"')[1]
		用户信息_表[账号]=[学生id,姓名,重置密码地址]
	return 用户信息_表
	


def 完成管理员名下学生作业(管理员用户信息):
	'''
完成管理员名下学生作业

参数:
	管理员用户信息:
		使用管理员的"用户名"和"密码"在"登录"得到的"用户信息"

'''
	if(not 管理员用户信息):
		return False

	if(管理员用户信息[1]["UserType"]!="1"):
		print("该用户非管理员用户")
		return 0
	
	用户信息_表=使用管理员用户获取学生表(管理员用户信息)
	#input(用户信息_表)
	要完成表={}
	for index in 用户信息_表:
		要完成表[index]=""
	
	时间=time.time()
	未完成表1=使用用户名密码表完成(要完成表,保存表_文件名=管理员用户信息[1]["UserName"]+"_"+time.strftime("%Y%m%d-%H%M%S",time.localtime(时间))+"."+str(时间).split(".")[1],打印未完成=True)

	未完成表1_密码错误=未完成表1[2]

	未完成表2=[[],[],[]]
	if(未完成表1_密码错误 and input('有未完成,将尝试重置密码,输入"y"继续,否则跳过')=="y"):
	
	
		重置密码用户名列表=未完成表1_密码错误
		
		for index in 重置密码用户名列表:
			try:
				重置密码地址=用户信息_表[index][2]
			except:
				print("注意:\""+str(index)+"\"不在该管理员名下,不能重置")
			else:
				访问结果=访问(重置密码地址,{"Cookie":管理员用户信息[0]})
				a=json.loads(访问结果[6])
				if(a["statusCode"]=="200"):
					print("成功,重置密码\""+index+"\",信息:"+a["message"])
				else:
					print("失败,重置密码\""+index+"\",状态"+str(a["statusCode"])+",信息:"+a["message"])
				
		if(重置密码用户名列表):
			未完成表2=使用用户名密码表完成(要完成表,保存表=False,打印未完成=False)
			if(未完成表2[2]):
				print("错误:重置密码后仍有未完成")
	
	if(未完成表1[1] or 未完成表2[0]):
		未完成表=未完成表1[1]
		for i in 未完成表2[0]:
			if i not in 未完成表:
				未完成表.append(i)
		print("未完成:")
		for i in 未完成表:
			print("\t"+i)

	else:
		print("已全部完成")

def 获取文件(路径,类型=None):
	'''

'''
	try:
		数据=访问("https://raw.githubusercontent.com/xzx482/smaqjypt_/main/"+路径)[6]
	except:
		try:
			数据=访问("http://xgithub.dynv6.net/"+路径)[6]
		except:
			return None
	if(类型=="json"):
		try:
			return json.loads(数据)
		except:
			return None
	return 数据

'''
while 1:
	自动完成()
#'''


#'''
if __name__ == '__main__':
	try:
		print('联网检查更新(按Ctrl+C可取消)...')

		版本更新_获取=request.urlopen("https://raw.githubusercontent.com/xzx482/smaqjypt_/main/%E6%95%B0%E6%8D%AE/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC.json",timeout=8)
		if(版本更新_获取.getcode()>=300):
			raise
	except KeyboardInterrupt:
		pass
	except:
		try:
			版本更新_获取=request.urlopen("http://xgithub.dynv6.net/%E6%95%B0%E6%8D%AE/%E6%9C%80%E6%96%B0%E7%89%88%E6%9C%AC.json",timeout=13)
			if(版本更新_获取.getcode()>=300):
				raise
		except KeyboardInterrupt:
			pass
		except:
			try:
				request.urlopen("https://baidu.com")
			except KeyboardInterrupt:
				pass
			except:
				print('注意:网络不正常')
				按任意键继续()
			else:
				版本更新_获取=None
				print('注意:github.io不能访问')
				按任意键继续()
		if(版本更新_获取):
			#if 1:
			try:
				版本更新_内容=json.loads(版本更新_获取.read().decode('utf-8'))
				if(版本更新_内容["版本"]>__版本__):
					print('有更新')
					try:print(版本更新_内容['更新内容'],end='')
					except:pass
					if(input('\n输入"y"并回车可更新:')):
						if 1:
						#try:
							print('下载...')
							#for i in 版本更新_内容['url'][文件类型]:
							for i in 版本更新_内容['url'][0]:
								try:
									新文件_响应=request.urlopen(i)
									新文件=新文件_响应.read()
									if(新文件_响应.getcode()>=300):
										raise
								except:
									continue
								else:
									文件名=sys.argv[0]
									新文件名=".".join(文件名.split(".")[0:-1])+"."+i.split(".")[-1]
									print('更新文件...')
									with open(新文件名,"wb")as f:
										f.write(新文件)
									#with open('ndb.bat','w')as f:
									#	f.write('ping 127.0.0.1 -n 2;move "'+文件名+'" "'+文件名+'.old";ping 127.0.0.1 -n 2;move nd "'+"\\".join(文件名.split("\\")[0:-1])+'"')
									#os.system('start ndb.bat')
									按任意键继续('更新完成,',提示信息_3='重启程序')
									os.system("start "+新文件名.split("\\")[-1])
									exit()
									#break
							print('更新失败')
							'''
						except:
							print('更新失败')	
						'''	
			except SystemExit:
				raise
			except:
				print('获取更新失败')
				按任意键继续()

	交互模式=True
	安静模式=not 交互模式
	#初次使用=True
	启用提示=False
	try:
		if(初次使用):
			清屏()
			print('你好,这应该是你第一次使用,选择"1"可进入操作教程,若不是,请选择"2"\n请输入你想选择的答案前面的序号,并按回车键\n1.是第一次使用\n2.不是第一次使用')
			while 1:
				输入=input("请选择:")
				if(输入=="1"):
					清屏()
					print('教程\n基本操作:\n\t输入对应的序号并按回车即可进入.现在,请输入"1"并回车,进入"这是一个选项"选项.\n1.这是一个选项')
					while 1:
						输入=input("请选择:")
						if(输入=="1"):
							清屏()
							print("教程>这是一个选项\n\t若要返回上一级,则不输入内容并回车.现在,请返回上一级")
							print("<这里没有选项>")
							while 1:
								if(input("请选择:")==""):
									break
							break
						elif(输入==''):
							exit()
					清屏()
					print('教程\n假装这是刚才的上一级')
					print('若要退出,可按"Ctrl+C",现在,请尝试退出')
					try:
						while 1:
							input()
					except KeyboardInterrupt:
						print('正常情况下,刚才的操作会退出,但教程还未结束,如果真的要退出,可连续地按"Ctrl+C",在其他地方遇到类似的也可以连续地按"Ctrl+C"')
						按任意键继续()
						清屏()
						print('在"按任意键继续"时,也可以按"Ctrl+C"退出')
						try:
							按任意键继续()
						except:
							print('')
						清屏()
						print('教程已结束.')
						print('现在,你可以到主页面看看,或者试试用"Ctrl+C"退出')
						print('在本次退出前,使用功能都会有提示.若之后还想看到提示,可到"6.其他">"1.启用提示"')
						启用提示=True
						按任意键继续()
					break
				if(输入=="2"):
					初次使用=False
					break
				if(输入==""):
					exit()
		

		路径=[]
		while 1:
			清屏()
			路径=路径[0:0]
			路径.append("smaqjypt")
			输入_=input('>'.join(路径)+"\t 版本:"+str(__版本__)+"\n1.手动输入用户名密码自动完成\n2.手动输入用户名密码手动选择完成\n3.使用用户名密码表完成\n4.使用已保存的用户名表完成\n5.完成管理员名下所有学生作业\n6.其他\n请选择:")
			if(输入_==""):
				break
			if(输入_=="1"):
				if(启用提示):
					print('输入学生的账号密码(已登录过的或密码为"123456"的可不输密码),即可完成该学生的所有作业')
				while(1):
					a_adw=自动完成()
					if(isinstance(a_adw,bool)and a_adw==False):
						break
			elif(输入_=="2"):
				if(启用提示):
					print('输入学生的账号密码(已登录过的或密码为"123456"的可不输密码),即可显示该学生的作业,输入作业id即可完成该作业')
					按任意键继续()
				while(1):
					a_adw=显示作业列表()
					if(isinstance(a_adw,bool)and a_adw==False):
						break
			elif(输入_=="3"):
				if(启用提示):
					print('批量完成学生作业\n用户名和密码之间用半角冒号":"分开(比如张三的账号是"zhangsan2333",密码是"234567"则这样写:"zhangsan2333:234567");\n若没有更改密码可不需要冒号(比如张三的账号是"zhangsan2333",密码是默认的"123456"则可以只这样写:"zhangsan2333");\n每行一个账号(和密码),全部输入完后,再输入一个空行(即不输入任何内容再按一次回车)就可以开始了;\n全部尝试后,若有密码不正确,会显示出来;\n输入的表会保存在"'+用户表文件目录+'",以便之后使用;\n可以开始输入了')
				print('请输入:')
				表={}
				while 1:
					输入=input(">")
					if(输入):
						if(":"in 输入):
							用户名_,密码_=输入.split(":",1)
						else:
							用户名_=输入
							密码_=""
						表[用户名_]=密码_
					else:
						break
				if(表):
					print("输入结束")
					使用用户名密码表完成(表)
					按任意键继续()
				else:
					continue
			elif(输入_=="4"):
				if(启用提示):
					print('批量完成学生作业,使用已保存的用户表,用户表在'+用户表文件目录+'中,可来自"使用用户名密码表完成""完成管理员名下所有学生作业"中保存的表,也可自行保存txt格式的文本到该目录下(注意编码是"UTF-8",一行一个账号,不能有密码,需提前登录并保存用户信息)')
				#while 1:
				用户表表=os.listdir(用户表文件目录)
				用户表表_=[]
				for i in 用户表表:
					if(i.split(".")[-1]=="txt"):
						用户表表_.append(i)
				if(not 用户表表_):
					print("没有已保存的用户名表")
					按任意键继续()
					continue
				用户表表=用户表表_
				for i in range(len(用户表表)):
					print(str(i+1)+":"+用户表表[i][0:-4])
				输入=input()
				#if(not 输入):
				#	break
				文件名=None
				try:
					输入_数字=int(输入)
					if(0<输入_数字 and 输入_数字<=len(用户表表)):
						文件名=用户表表[输入_数字-1]
					else:
						raise BaseException
				except:
					if(输入 and 输入 in 用户表表):
						文件名=输入
					elif(输入+".txt" in 用户表表):
						文件名=输入+".txt"
				if(文件名):
					表={}
					try:
						with open(用户表文件目录+文件名,"r") as f:表_=f.read()
						for i in 表_.split("\n")[0:-1]:
							表[i]=""
					except:
						print("错误:\""+用户表文件目录+文件名+"\"读取错误")

					if(表):
						使用用户名密码表完成(表,False)
						按任意键继续()
				
			elif(输入_=="5"):
				if(启用提示):
					print('输入管理员的账号和密码,即可自动完成其名下所有学生的作业')
				用户信息=登录_()
				if(用户信息):
					完成管理员名下学生作业(用户信息)
					按任意键继续()
				else:
					continue
			elif(输入_=="6"):
				while 1:
					路径=路径[0:1]
					路径.append("其他")
					清屏()
					print('>'.join(路径)+'\n1.启用提示\n2.保存临时数据\n3.打赏/捐助作者\n9.删除数据')
					输入=input('请选择:')
					if(输入==''):
						break
					elif(输入=='1'):
						启用提示=True
						print("提示已启用")
						time.sleep(0.4)
					elif(输入=='2'):
						保存临时数据()
						按任意键继续()
					elif(输入=='3'):
						while 1:
							路径=路径[0:2]
							路径.append("打赏/捐助作者")
							清屏()
							print('>'.join(路径)+'\n请选择支付方式\n1.QQ\n2.微信\n3.支付宝\n4.全部')
							输入__=input('请选择:')
							if(输入__==''):
								break
							输入正确=True
							while 输入正确:
								路径=路径[0:3]
								清屏()
								输入正确=False
								if(输入__=='1'):
									输入正确=True
									二维码_=支持作者_二维码(支持二维码_调整,1)
									路径.append("QQ")
								if(输入__=='2'):
									输入正确=True
									二维码_=支持作者_二维码(支持二维码_调整,2)
									路径.append("微信")
								if(输入__=='3'):
									输入正确=True
									二维码_=支持作者_二维码(支持二维码_调整,3)
									路径.append("支付宝")
								if(输入__=='4'):
									输入正确=True
									二维码_=支持作者_二维码(支持二维码_调整,0)
									路径.append("全部")
								print('>'.join(路径)+二维码_)
								if(输入正确):
									print('当前调整值为'+str(支持二维码_调整)+',若二维码不能正常显示,可尝试增加或减少\n若调整后仍不能正常显示,可将支付软件名称下方、二维码上方的文本生成二维码来扫描')
									if(支持二维码_调整<4):
										print('\n1.增加',end='')
									if(支持二维码_调整>1):
										print('\n2.减少',end='')
									print()
									输入___=input('请选择:')
									if(输入___==''):
										break
									elif(输入___=='1'):
										if(支持二维码_调整<4):
											支持二维码_调整+=1
									elif(输入___=='2'):
										if(支持二维码_调整>1):
											支持二维码_调整-=1
												
					elif(输入=="9"):
						确认值="yqs"
						if(input('输入"'+确认值+'"确认删除数据:')==确认值):
							print("正在删除数据",end="",flush=True)
							shutil.rmtree(数据文件目录)
							按任意键继续("\r已删除数据  \n")
							print("再见.")
							time.sleep(0.2)
							清屏()
							exit()
						else:
							按任意键继续("未删除数据\n")
	#except KeyboardInterrupt:
	#	if(not 安静模式):
	#		print("\n用户中断执行")
	except KeyboardInterrupt:pass
	except(SystemExit,EOFError):pass
	except OSError:
		etype,value,tb=traceback.sys.exc_info()
		错误信息="".join(traceback.TracebackException(type(value),value,tb,limit=None).format(chain=None))
		#print(错误.args[0])
		#if("args" in 错误.args[0]):
		print("\n"+"-"*10+"操作系统错误,错误信息如下"+"-"*10)
		print(错误信息,end="")
		print("-"*10+"操作系统错误,错误信息如上"+"-"*10)
		print("操作系统错误是无法预料的.可尝试重新运行程序,重启,使用其他设备,更换网络环境.具体可根据错误信息的最后一行来尝试解决问题")
		按任意键继续(提示信息_3="退出")
	except:
		try:
			#错误信息="".join(traceback.StackSummary.from_list(traceback.extract_tb(*traceback.sys.exc_info()).format())
			etype,value,tb=traceback.sys.exc_info()
			错误信息="".join(traceback.TracebackException(type(value),value,tb,limit=None).format(chain=None))
			print("-"*10+"出错了,错误信息如下"+"-"*10)
			print(错误信息,end="")
			#traceback.print_exception(*traceback.sys.exc_info())
			print("-"*10+"出错了,错误信息如上"+"-"*10)
			时间=time.time()
			错误信息文件路径=错误信息文件目录+time.strftime("%Y%m%d-%H%M%S",time.localtime(时间))+"."+str(时间).split(".")[1]+".txt"
			try:
			#if 1:
				with open(错误信息文件路径,"w") as f:
					f.write("版本:"+str(__版本__)+"\n")
					f.write("时间:"+str(时间)+"\n")
					f.write(错误信息)
					print("错误信息已保存到\""+错误信息文件路径+"\"")
					print("若要反馈此问题,可反馈到邮箱1738078451@qq.com,标题为\"问题反馈\",在正文中描述该问题是如何发生的,并将错误信息添加到附件中,错误信息不会包括个人信息")
			except:pass
			按任意键继续(提示信息_3="退出")
		except:
			input("\n出错了,按回车键退出,按Ctrl+C键继续引发错误以查看详细信息\n")
