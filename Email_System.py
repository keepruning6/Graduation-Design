# -*- coding:utf-8 -*-
import Tkinter
from PIL import Image,ImageTk
import webbrowser
import smtplib
import sys
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.header import Header
from email.mime.image import MIMEImage  #导入图片
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication 
import easygui
from Receive_Email import Receive_Email  # 邮件解析模块
import tkFileDialog
from SpamEmail import spamEmailBayes     #垃圾邮件过滤模块
import re
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
#from Tkinter import *




class Email_System:
	def __init__(self):
		self.root=Tkinter.Tk()
		self.user=''
		self.passwd=''
		self.smtp_server=''
		self.pop_server=''
		self.path=[]
		self.image=[]
		self.black_lists=[]


	def pop3_init(self):
		try:
		    self.pop3_server = poplib.POP3(self.pop_server)  #从传入参数获取pop服务器名称
		    self.pop3_server.user(self.user)          #从传入参数获取用户名
		    self.pop3_server.pass_(self.passwd)       #从传入参数获取密码
		except Exception as e:
			print "POP CONNECT ERROR ->", str(e)


	def sendmail(self):
		try:
			recipient=self.sjr.get()
			subject=self.subj.get()
			texte=self.tex.get('1.0','end')
		except Exception as e:
			print "RECEIVER INTO ERROR ->", str(e)
		message = MIMEMultipart()
		message['From']= Header('Email_liao<'+self.user+'>','utf-8')  #邮件头包括三部分发件人，收件人，邮件主题也就是from,to,self.subject
		message['To']= Header(recipient,'utf-8')
		message['Subject']= Header(subject,'utf-8')
		textt = MIMEText(texte, 'plain', 'utf-8')
		message.attach(textt)

		if len(self.path) != 0:
			try:
				for file_path in self.path:
					file_name =file_path.rsplit('\\',1)[-1]     #从留下路径的最后一部分并作为命名的一部分
					file_part = MIMEApplication(open(file_path, 'rb').read())                    #打开附件
					file_part.add_header('Content-Disposition', 'attachment', filename=file_name)#为附件命名
					message.attach(file_part)                                                        #添加附件
				print "ADD SUCCESS"
			except Exception as e:
				print "ADD FILE ERROR ->", str(e)



		if len(self.image) != 0:
			try:
				for image_path in self.image:
					image_name=image_path.rsplit('\\',1)[-1]         #从留下路径的最后一部分并作为命名的一部分
					image_part = MIMEImage(open(image_path, 'rb').read())          
					image_part.add_header('Content-Disposition', 'attachment', filename=image_name)
					message.attach(image_part)                                                    
				print "ADD SUCCESS"
			except Exception as e:
				print "ADD IMAGE ERROR ->", str(e)


		remain_windows = Tkinter.Tk()                 #发送成功窗口
		remain_windows.title("提示消息")
		remain_windows.geometry("240x100")
		remain_windows.config(bg='Honeydew')


		try:
			smtpObj=smtplib.SMTP()
			smtpObj.connect(self.smtp_server,25)
			smtpObj.login(self.user,self.passwd)
			smtpObj.sendmail(self.user,recipient,message.as_string())
			print "success"

			remain_lable = Tkinter.Frame(remain_windows)                        #调用一个纯容器
			Tkinter.Label(remain_lable, text="Send Success!",bg="Honeydew").pack(fill="y", expand="yes") #调用一个标签，内容为发送成功
			remain_lable.pack()

			exit_button = Tkinter.Frame(remain_windows)                                 #调用一个纯容器
			Tkinter.Button(exit_button, text="Confirm",bg="Honeydew", command=remain_windows.destroy).pack() #调用一个确认按钮，并显示确认字样，显示之后摧毁窗口
			exit_button.pack()                                                       #显示这个按钮                                                    #显示这个标签
			remain_windows.mainloop()

		except smtplib.SMTPException as e: 
			print str(e)
			remain_lable = Tkinter.Frame(remain_windows)                              #在窗口处显示发送失
			Tkinter.Label(remain_lable, text="Send Failed!").pack(fill="y", expand="yes")
			remain_lable.pack()
			remain_windows.mainloop()





	def add_file(self):
		try:
		    _path = easygui.fileopenbox() #打开文件对话框,返回文件绝对路径字符串
		    if _path is None:
		    	return 1
		    else:
		    	self.path.append(_path)
		    	for i in self.path:
		    		if self.path.index(i) == 0:
		    			Tkinter.Label(self.send_mailui, text=i).place(x=20, y=(self.path.index(i)+1)*30 + 480)#在屏幕显示路径
		    		else:
		    			Tkinter.Label(self.send_mailui, text=i).place(x=20, y=(self.path.index(i)+1)*20 + 490)
		except Exception as e:
			print "ADD FILE ERROR ->", str(e)



	def add_image(self):
		try:
		    _image = easygui.fileopenbox() #打开文件对话框,返回图片绝对路径字符串
		    if _image is None:
		    	return 1
		    else:
		    	self.image.append(_image)
		    	for i in self.image:
		    		if self.image.index(i) == 0:
		    			Tkinter.Label(self.send_mailui, text=i).place(x=110, y=(self.image.index(i)+1)*30 + 480)
		    		else:
		    			Tkinter.Label(self.send_mailui, text=i).place(x=110, y=(self.image.index(i)+1)*20 + 490)
		except Exception as e:
			print "ADD IMAGE ERROR ->", str(e)



	def send_mail(self):
		self.send_mailui=Tkinter.Tk()
		self.send_mailui.title('写邮件')
		self.send_mailui.geometry('800x550')
		self.send_mailui.config(bg='Honeydew')
		Tkinter.Label(self.send_mailui,text='你好：',font='宋体,14',bg='Honeydew').place(x=300,y=10)
		Tkinter.Label(self.send_mailui,text=self.user,font='宋体,14',bg='Honeydew').place(x=400,y=10)
		Tkinter.Label(self.send_mailui,text='收件人:',font='宋体,14',bg='Honeydew').place(x=10,y=40,width=150,height=50)
		Tkinter.Label(self.send_mailui,text='主题:',font='宋体,14',bg='Honeydew').place(x=10,y=100,width=150,height=50)
		Tkinter.Label(self.send_mailui,text='正文:',font='宋体,14',bg='Honeydew').place(x=10,y=160,width=150,height=50)
		self.sjr=Tkinter.Entry(self.send_mailui)
		self.sjr.place(x=160,y=50,width=400,height=30)
		self.subj=Tkinter.Entry(self.send_mailui)
		self.subj.place(x=160,y=110,width=400,height=30)
		scroll_bar=Tkinter.Scrollbar(self.send_mailui)

		self.tex=Tkinter.Text(self.send_mailui,width=100,height=20,yscrollcommand=scroll_bar.set)
		self.tex.place(x=20,y=210)
		scroll_bar.config(command=self.tex.yview)
		scroll_bar.pack(side='right',fill='y')

		Tkinter.Button(self.send_mailui,text='附件',font='宋体,12',bg='Honeydew',command=self.add_file).place(x=20,y=480,width=80,height=30)
		Tkinter.Button(self.send_mailui,text='图片',font='宋体,12',bg='Honeydew',command=self.add_image).place(x=110,y=480,width=80,height=30)
		Tkinter.Button(self.send_mailui,text='发送',font='宋体,14',bg='Honeydew',command=self.sendmail).place(x=650,y=500,width=100,height=40)

	def filesave(self):
		askopenfileui=Tkinter.Tk()
		askopenfileui.withdraw()
		filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file")
		for key in self.attachment:
			data=self.attachment[key]
		if filename:
			with open(filename,'w') as f1:      #使用with as代替try except
				f1.write(data)


	def open_mail(self,mouse):
		view_mailui=Tkinter.Tk()
		view_mailui.title("查看邮件")
		view_mailui.geometry("800x550")
		view_mailui.config(bg='AliceBlue')

		self.pop3_init()
		for i in range(0, len(self.msg)+1):      #获取用户点击查看邮件的索引号
			if self.msg_list.select_includes(i):
				id_flag = list(self.msg_list.curselection())[0]
				print id_flag
				break

		res,line,octect=self.pop3_server.retr(self.mails_len-id_flag)
		message_content = b'\r\n'.join(line).decode('utf-8')
		message =Parser().parsestr(message_content)
		recv=Receive_Email()                      #实例化导入模块
		header_list = recv.email_header(message)  # 包含From To Subject
		content = recv.email_content(message)     #返回正文
		tim=recv.email_time_size(message)         #返回时间
		self.attachment=recv.email_attachement(message) #返回附件


		Tkinter.Label(view_mailui,text=header_list[2],font='宋体,14',bg='LightSkyBlue',fg='Black').place(x=200,y=0)
		Tkinter.Label(view_mailui,text='发件人:',font='宋体,14',bg='AliceBlue').place(x=10,y=40,width=150,height=30)
		Tkinter.Label(view_mailui,text='收件人:',font='宋体,14',bg='AliceBlue').place(x=10,y=80,width=150,height=30)
		Tkinter.Label(view_mailui,text='时间:',font='宋体,14',bg='AliceBlue').place(x=10,y=120,width=150,height=30)
	#	Tkinter.Label(view_mailui,text='大小:',font='宋体,14',bg='AliceBlue').place(x=10,y=160,width=150,height=30)
		Tkinter.Label(view_mailui,text=header_list[0],font='宋体,14',bg='AliceBlue').place(x=160,y=45)
		Tkinter.Label(view_mailui,text=header_list[1],font='宋体,14',bg='AliceBlue').place(x=160,y=85)
		Tkinter.Label(view_mailui,text=tim,font='宋体,14',bg='AliceBlue').place(x=160,y=125)
	#	Tkinter.Label(view_mailui,text='50k',font='宋体,14',bg='AliceBlue').place(x=160,y=165)

		scroll_bar=Tkinter.Scrollbar(view_mailui)
		view_text=Tkinter.Text(view_mailui,width=105,height=22,yscrollcommand=scroll_bar.set)
		view_text.place(x=20,y=160)
		scroll_bar.config(command=view_text.yview)
		scroll_bar.pack(side='right',fill='y')

		for i in content:
			view_text.insert('end',i)

		Tkinter.Button(view_mailui,text='回复',font='宋体,12',bg='Honeydew').place(x=20,y=470,width=80,height=30)
		Tkinter.Button(view_mailui,text='附件下载',font='宋体,12',bg='Honeydew',command=self.filesave).place(x=110,y=470,width=80,height=30)
		Tkinter.Button(view_mailui,text='退出',font='宋体,14',bg='Honeydew',command=view_mailui.destroy).place(x=650,y=500,width=100,height=40)
		if self.attachment:
			for key in self.attachment:
				if len(self.attachment)==1:
					Tkinter.Label(view_mailui,text=key,bg='Honeydew').place(x=110,y=500)
				else:
					Tkinter.Label(view_mailui,text=key,bg='Honeydew').place(x=110,y=510)


	def refresh_windows(self):
		self.mail_win.destroy()
		self.mail_window()


	def add_black_list(self):
		black_name = self.black_name.get()
		if black_name == "":
			print black_name
			print "no message"
		else:
			print black_name
			self.black_lists.append(str(black_name))
			self.black_list.insert('end', str(black_name))
	def delete_black_name(self):
		self.black_lists[:] = []
		self.black_list.delete(self.black_list.curselection(), self.black_list.curselection())



	def black_list_windows(self):
		black_ui = Tkinter.Tk()
		black_ui.title("邮箱黑名单")
		black_ui.geometry("320x320")
		black_ui.config(bg='LemonChiffon')
		self.black_name = Tkinter.Entry(black_ui)
		self.black_name.place(x=10, y=11)
		# 滚动条
		scroll_bar = Tkinter.Scrollbar(black_ui)
		scroll_bar.pack(side='right', fill='y')
		# 按钮
		Tkinter.Button(black_ui, text=" 加入 ",bg='LemonChiffon',command=self.add_black_list).place(x=180, y=9)
		Tkinter.Button(black_ui, text=" 清空 ",bg='LemonChiffon',command=self.delete_black_name).place(x=240, y=9)
		# 显示
		self.black_list = Tkinter.Listbox(black_ui, yscrollcommand=scroll_bar.set, width=35)
		self.black_list.place(x=10, y=40)
		if len(self.black_lists) != 0:
			for bl in self.black_lists:
				self.black_list.insert('end', bl)
		black_ui.mainloop()


	def draft_windows(self):
		draft_ui= Tkinter.Tk()
		draft_ui.title('垃圾邮件收放点')
		draft_ui.geometry('650x360')
		draft_ui.config(bg='PowderBlue')

		Tkinter.Label(draft_ui,text='草稿箱',font=('宋体',20),bg='PowderBlue').pack()

		draft_scroll= Tkinter.Scrollbar(draft_ui)
		draft_scroll.pack(side='right',fill='y')
		self.draft_listbox= Tkinter.Listbox(draft_ui,yscrollcommand=draft_scroll.set,selectmode='browse',width=85,height=14)
		self.draft_listbox.place(x=10,y=40)
		draft_scroll.config(command=self.draft_listbox.yview)
		self.draft_listbox.bind("<Double-Button-1>",self.open_mail)


		draft_buttdel=Tkinter.Button(draft_ui,text='删除',command=lambda x=self.draft_listbox:x.delete('active'),font=('宋体',16),bg='PowderBlue')
		draft_buttdel.place(x=50,y=300)
		draft_buttback=Tkinter.Button(draft_ui,text='退出',command=draft_ui.destroy,font=('宋体',16),bg='PowderBlue')
		draft_buttback.place(x=500,y=320)


		draft_ui.mainloop()






	def spam_windows(self):     #垃圾邮件功能
		spam_ui= Tkinter.Tk()
		spam_ui.title('垃圾邮件收放点')
		spam_ui.geometry('650x360')
		spam_ui.config(bg='Peru')

		Tkinter.Label(spam_ui,text='垃圾邮件',font=('宋体',20),bg='Peru').pack()

		spam_scroll= Tkinter.Scrollbar(spam_ui)
		spam_scroll.pack(side='right',fill='y')
		self.spam_listbox= Tkinter.Listbox(spam_ui,yscrollcommand=spam_scroll.set,selectmode='browse',width=85,height=14)
		self.spam_listbox.place(x=10,y=40)
		spam_scroll.config(command=self.spam_listbox.yview)
		self.spam_listbox.bind("<Double-Button-1>",self.open_mail)


		spam_buttdel=Tkinter.Button(spam_ui,text='删除',command=lambda x=self.spam_listbox:x.delete('active'),font=('宋体',16),bg='Peru')
		spam_buttdel.place(x=50,y=300)
		spam_buttback=Tkinter.Button(spam_ui,text='退出',command=spam_ui.destroy,font=('宋体',16),bg='Peru')
		spam_buttback.place(x=500,y=320)


		spam_ui.mainloop()


	def spam_filter(self):
		#spam类对象
		spam=spamEmailBayes()
		#保存词频的词典
		spamDict={}
		normDict={}
		testDict={}
		#保存每封邮件中出现的词
		wordsList=[]
		wordsDict={}
		#保存预测结果,key为文件名，值为预测类别
		testResult={}
		#分别获得正常邮件、垃圾邮件及测试文件名称列表
		normFileList=spam.get_File_List(r"D:/Email_system/data/normal")
		spamFileList=spam.get_File_List(r"D:/Email_system/data/spam")
#		testFileList=spam.get_File_List(r"D:/Email_system/data/test")
		#获取训练集中正常邮件与垃圾邮件的数量
		normFilelen=len(normFileList)
		spamFilelen=len(spamFileList)
		#获得停用词表，用于对停用词过滤
		stopList=spam.getStopWords()
		#获得正常邮件中的词频
		for fileName in normFileList:
		    wordsList[:]=[]
		    for line in open("./data/normal/"+fileName):
		        #过滤掉非中文字符
		        rule=re.compile(r"[^\u4e00-\u9fa5]")
		        line=rule.sub("",line)
		        #将每封邮件出现的词保存在wordsList中
		        spam.get_word_list(line,wordsList,stopList)
		    #统计每个词在所有邮件中出现的次数
		    spam.addToDict(wordsList, wordsDict)
		normDict=wordsDict.copy()                       #获得p(w|h) 已知正常邮件下词出现的概率

		#获得垃圾邮件中的词频
		wordsDict.clear()
		for fileName in spamFileList:
		    wordsList[:]=[]
		    for line in open("./data/spam/"+fileName):
		        rule=re.compile(r"[^\u4e00-\u9fa5]")
		        line=rule.sub("",line)
		        spam.get_word_list(line,wordsList,stopList)
		    spam.addToDict(wordsList, wordsDict)
		spamDict=wordsDict.copy()                     #获得p(w|s)  已知垃圾邮件中词出现的概率


#		self.pop3_server = poplib.POP3(self.pop_server)
#		self.pop3_server.set_debuglevel(1)
#		print server.getwelcome().decode('utf-8')
#		self.pop3_server.user(self.user)
#		self.pop3_server.pass_(self.passwd)
#		print 'Messages:%s.Size:%s' %self.pop3_server.stat()
#		resp,mails,octects= self.pop3_server.list()
#		self.mails_len=len(mails)
#		print mails
		index = self.mails_len
#		all_recv_email=[]
		recev = Receive_Email()   #实例化导入模块
		while index>=1:
			resp,lines,octects=self.pop3_server.retr(index)
			msg_content = b'\r\n'.join(lines).decode('utf-8')
			msg =Parser().parsestr(msg_content)
			content = recev.email_content(msg)     #返回正文
			content=str(content)
			testDict.clear()
			wordsDict.clear()
			wordsList[:]=[]
			rule=re.compile(r"[^\u4e00-\u9fa5]")
			content=rule.sub("",content)
			spam.get_word_list(content,wordsList,stopList)
			spam.addToDict(wordsList, wordsDict)
			testDict=wordsDict.copy()
			#通过计算每个文件中p(s|w)来得到对分类影响最大的15个词
			wordProbList=spam.getTestWords(testDict, spamDict,normDict,normFilelen,spamFilelen)
			#对每封邮件得到的15个词计算贝叶斯概率  
			p=spam.calBayes(wordProbList, spamDict, normDict)
			if(p>0.9):
				testResult.setdefault(index,1)
			else:
				testResult.setdefault(index,0)
			index=index-1
		return testResult
	#计算分类准确率（测试集中文件名低于1000的为正常邮件）
#		testAccuracy=spam.calAccuracy(testResult)
#		for i,ic in testResult.items():
#		    print i+"/"+str(ic)
#		print testAccuracy









	def mail_window(self):
		self.mail_win=Tkinter.Tk()
		self.mail_win.title("邮件中心")
		self.mail_win.geometry("900x500")
		self.mail_win.configure(bg='AliceBlue')

		Tkinter.Label(self.mail_win, text="Welcome: ",font=('宋体',14),bg='AliceBlue').place(x=240,y=5)
		Tkinter.Label(self.mail_win, text=self.user,font=('宋体',14),bg='AliceBlue').place(x=340,y=5)

		Tkinter.Button(self.mail_win,text='收件箱',font=('宋体',14),bg='AliceBlue').place(x=10,y=30,width=200,height=50)
		Tkinter.Button(self.mail_win,text='发邮件',font=('宋体',14),bg='AliceBlue',command=self.send_mail).place(x=10,y=110,width=200,height=50)
		Tkinter.Button(self.mail_win,text='草稿箱',font=('宋体',14),bg='AliceBlue',command=self.draft_windows).place(x=10,y=190,width=200,height=50)
		Tkinter.Button(self.mail_win,text='垃圾邮件',font=('宋体',14),bg='AliceBlue',command=self.spam_windows).place(x=10,y=270,width=200,height=50)
		Tkinter.Button(self.mail_win,text='黑名单',font=('宋体',14),bg='AliceBlue',command=self.black_list_windows).place(x=10,y=350,width=200,height=50)


		scroll_bar = Tkinter.Scrollbar(self.mail_win)
		scroll_bar.pack(side='right',fill='y')   #滚动条靠右垂直填充
		#scroll_bar_x = Tkinter.Scrollbar(self.mail_win)
		#scroll_bar_x.pack(side='bottom', fill='x')     #滚动条向底部，水平方向填充
		self.msg_list = Tkinter.Listbox(self.mail_win, yscrollcommand=scroll_bar.set,font="宋体,15", selectmode='browse',bg='White')
		self.msg_list.place(x=240,y=30,width=600,height=300)
		scroll_bar.config(command=self.msg_list.yview)
		self.msg_list.bind("<Double-Button-1>",self.open_mail)

		Tkinter.Button(self.mail_win,text='删除',font=('宋体',12),bg='White',command=lambda x=self.msg_list:x.delete('active')).place(x=240,y=340,width=100,height=40)
		Tkinter.Button(self.mail_win,text='刷新',font=('宋体',12),bg='White',command=self.refresh_windows).place(x=360,y=340,width=100,height=40)
		Tkinter.Button(self.mail_win,text='退出',font=('宋体',12),bg='White',command=sys.exit).place(x=740,y=340,width=100,height=40)

		self.pop3_server = poplib.POP3(self.pop_server)
		self.pop3_server.set_debuglevel(1)
#		print server.getwelcome().decode('utf-8')
		self.pop3_server.user(self.user)
		self.pop3_server.pass_(self.passwd)
		print 'Messages:%s.Size:%s' %self.pop3_server.stat()
		resp,mails,octects= self.pop3_server.list()
		self.mails_len=len(mails)
#		print mails
		index = len(mails)
		all_recv_email=[]
		rece = Receive_Email()   #实例化导入模块
		self.result={}
		self.result=self.spam_filter() #调用垃圾邮件过滤方法，返回一个垃圾邮件测试的结果
#		for key in result:
#			print key
#			print result[key]
		for key in self.result:
			try:
				resp,lines,octects=self.pop3_server.retr(key)
				msg_content = b'\r\n'.join(lines).decode('utf-8')
				self.msg =Parser().parsestr(msg_content)
				header_part=rece.email_header(self.msg)

				if self.result[key]==0:
					all_recv_email.append(header_part)
#					header_view=header_part[1]+'  '+header_part[2]
#					self.msg_list.insert('end',header_view)
				else:
					From = 'From: ' + str(header_part[0])
					To = 'To: ' + str(header_part[1])
					Subject = 'Subject: ' + header_part[2]
					parma = From +''+To +''+ Subject
					self.spam_listbox.insert('end',parma)       #将垃圾邮件添加到spam_listbox
			except Exception as e:
				print e


		for item in all_recv_email:
			try:
				if len(self.black_lists) != 0:
					if str(item[0]).find(self.black_lists[0]) != -1:
						print self.black_lists[0]
						print "THIS EMAIL IN BLACK LIST"
						pass                                      #让跟黑名单上的邮箱无法显示
					else:
						From = 'From: ' + str(item[0])
						To = 'To: ' + str(item[1])
						Subject = 'Subject: ' + item[2]
						parma = From +''+To +''+ Subject
						self.msg_list.insert('end', parma)
				else:
					From = 'From: ' + str(item[0])
					To = 'To: ' + str(item[1])
					Subject = 'Subject: ' + item[2]
					parma = From + ''+To +''+ Subject
					self.msg_list.insert('end', parma)
			except Exception as e:
				print str(e)
		self.pop3_server.quit()


#		self.main_win.mainloop()



	def qq_refresh(self):         #刷新QQ登录窗口
		self.qq_ui.destroy()
		self.qq_login()

	def tx_check(self):
		self.qq_ui.withdraw()         #隐藏上一层窗口
		self.qq_check=Tkinter.Tk()
		self.qq_check.title("登录检查")
		self.qq_check.geometry("240x240")
		self.qq_check.configure(bg="Azure")
		self.qq_check.resizable(0,0)     #固定窗口
		try:
			self.user=self.qq_user.get() #从登录文本框中获得邮箱账户
			self.passwd=self.qq_pw.get() #获得密码
			self.smtp_server='smtp.qq.com'
			self.pop_server='pop.qq.com'
		except:
			Tkinter.Label(self.qq_check,text='please check your input',font=('宋体',14),bg='Azure').pack()

		try:
			self.server= smtplib.SMTP()   #获得SMTP对象
			self.server.connect(self.smtp_server,25)
			Tkinter.Label(self.qq_check,text='connect success',font=('宋体',14),bg='Azure').pack()
		except Exception as e:
			print 'ERROR->' +str(e)
			Tkinter.Label(self.qq_check,text='connect error',font=('宋体',14),bg='Azure').pack()

		try:
			self.server.login(self.user,self.passwd)
			self.server.quit()
			Tkinter.Label(self.qq_check,text='登录成功',font=('宋体',14),bg='Azure').pack()
			Tkinter.Button(self.qq_check,text='确定',font=('宋体',12),bg='Azure',height=2,width=10,command=self.mail_window).pack()
		except Exception as e:
			print 'login error' +str(e)
			Tkinter.Label(self.qq_check,text='请检查你的邮箱账户或密码',font=('宋体',14),bg='Azure').pack()
#		self.qq_check.mainloop()






	def qq_login(self):     #QQ登录界面
		self.root.withdraw()
		self.qq_ui=Tkinter.Tk()
		self.qq_ui.title("欢迎登录")
		self.qq_ui.geometry("440x440")
		self.qq_ui.resizable(0,0)
		self.qq_ui.configure(bg='Azure')

		self.qq_user=Tkinter.StringVar()     #textvariable将变量与Entry绑定
		self.qq_pw=Tkinter.StringVar()
		Tkinter.Label(self.qq_ui,text='欢迎登录腾讯QQ',font=("宋体",20),width=44,height=5,bg='Azure').pack(side='top')
		Tkinter.Label(self.qq_ui,text='邮箱地址:',font=('宋体',12),bg='Azure').place(x=85,y=150)
		self.qq_user=Tkinter.Entry(self.qq_ui,textvariable=self.qq_user)
		self.qq_user.place(x=160,y=150)
		Tkinter.Label(self.qq_ui,text='授权码 :',font=('宋体',12),bg='Azure').place(x=85,y=190)
		self.qq_pw=Tkinter.Entry(self.qq_ui,show='*',textvariable=self.qq_pw)
		self.qq_pw.place(x=160,y=190)
		Tkinter.Button(self.qq_ui,text='确定',font=('宋体',12),bg='Azure',width=10,height=2,command=self.tx_check).place(x=95,y=250)
		Tkinter.Button(self.qq_ui,text='取消',font=('宋体',12),bg='Azure',width=10,height=2,command=self.qq_refresh).place(x=210,y=250)
		Tkinter.Button(self.qq_ui,text='上一步',font=('宋体',12),bg='Azure',width=10,height=2,command=self.qq_ui.destroy).place(x=340,y=380)
		text = Tkinter.Text(self.qq_ui,font=('宋体',12),height=2,width=12,bg='Azure')   #添加一个超链接
		text.pack(side='left',anchor='se')
		text.insert(Tkinter.INSERT,'什么是授权码？')
		text.tag_add("link", '1.0', '1.19')          #指定tag名为link，从第一行的第0个到第一行第19列
		text.tag_config('link', foreground='blue', underline=True)   #为tag附加背景属性
		#绑定事件一定要传入event
		def show_hand_cursor(event):
		    text.config(cursor='arrow')
		def show_xterm_cursor(event):
		    text.config(cursor='xterm')
		def click(event):
		    webbrowser.open('https://service.mail.qq.com/cgi-bin/help?subtype=1&id=28&no=1001256')
		#鼠标指向
		text.tag_bind('link', '<Enter>', show_hand_cursor)
		#鼠标离开
		text.tag_bind('link', '<Leave>', show_xterm_cursor)
		#左键点击
		text.tag_bind('link', '<Button-1>', click)

#		self.qq_ui.mainloop()

	def w163_refresh(self):
		self.w163_ui.destroy()
		self.w163_login()

	def wy_check(self):
		self.w163_ui.withdraw()         #隐藏上一层窗口
		self.w163_check=Tkinter.Tk()
		self.w163_check.title("登录检查")
		self.w163_check.geometry("240x240")
		self.w163_check.configure(bg="LavenderBlush")
		self.w163_check.resizable(0,0)     #固定窗口
		try:
			self.user=self.w163_user.get() #从登录文本框中获得邮箱账户
			self.passwd=self.w163_pw.get() #获得密码
			self.smtp_server='smtp.163.com'
			self.pop_server='pop.163.com'
		except:
			Tkinter.Label(self.w163_check,text='please check your input',font=('宋体',14),bg='LavenderBlush').pack()

		try:
			self.server= smtplib.SMTP()   #获得SMTP对象
			self.server.connect(self.smtp_server,25)
			Tkinter.Label(self.w163_check,text='connect success',font=('宋体',14),bg='LavenderBlush').pack()
		except Exception as e:
			print 'ERROR->' +str(e)
			Tkinter.Label(self.w163_check,text='connect error',font=('宋体',14),bg='LavenderBlush').pack()

		try:
			self.server.login(self.user,self.passwd)
			self.server.quit()
			Tkinter.Label(self.w163_check,text='登录成功',font=('宋体',14),bg='LavenderBlush').pack()
			Tkinter.Button(self.w163_check,text='确定',font=('宋体',12),bg='LavenderBlush',height=2,width=10,command=self.mail_window).pack()
		except Exception as e:
			print 'login error' +str(e)
			Tkinter.Label(self.w163_check,text='请检查你的邮箱账户或密码',font=('宋体',14),bg='LavenderBlush').pack()
#		self.w163_check.mainloop()




	def w163_login(self):
		self.root.withdraw()
		self.w163_ui=Tkinter.Tk()
		self.w163_ui.title("欢迎登录")
		self.w163_ui.geometry("440x440")
		self.w163_ui.resizable(0,0)
		self.w163_ui.configure(bg='LavenderBlush')
	
		self.w163_user=Tkinter.StringVar()     #textvariable将变量与Entry绑定
		self.w163_pw=Tkinter.StringVar()
		Tkinter.Label(self.w163_ui,text='欢迎登录网易邮箱',font=("宋体",20),width=44,height=5,bg='LavenderBlush').pack(side='top')
		Tkinter.Label(self.w163_ui,text='邮箱地址:',font=('宋体',12),bg='LavenderBlush').place(x=85,y=150)
		self.w163_user=Tkinter.Entry(self.w163_ui,textvariable=self.w163_user)
		self.w163_user.place(x=160,y=150)
		Tkinter.Label(self.w163_ui,text='授权码 :',font=('宋体',12),bg='LavenderBlush').place(x=85,y=190)
		self.w163_pw=Tkinter.Entry(self.w163_ui,show='*',textvariable=self.w163_pw)
		self.w163_pw.place(x=160,y=190)
		Tkinter.Button(self.w163_ui,text='确定',font=('宋体',12),bg='LavenderBlush',width=10,height=2,command=self.wy_check).place(x=95,y=250)
		Tkinter.Button(self.w163_ui,text='取消',font=('宋体',12),bg='LavenderBlush',width=10,height=2,command=self.w163_refresh).place(x=210,y=250)
		Tkinter.Button(self.w163_ui,text='上一步',font=('宋体',12),bg='LavenderBlush',width=10,height=2,command=self.w163_ui.destroy).place(x=340,y=380)
		text = Tkinter.Text(self.w163_ui,font=('宋体',12),height=2,width=12,bg='LavenderBlush')   #添加一个超链接
	
		text.pack(side='left',anchor='se')
		text.insert(Tkinter.INSERT,'什么是授权码？')
		text.tag_add("link", '1.0', '1.19')          #指定tag名为link，从第一行的第0个到第一行第19列
		text.tag_config('link', foreground='blue', underline=True)   #为tag附加背景属性
		#绑定事件一定要传入event
		def show_hand_cursor(event):
		    text.config(cursor='arrow')
		def show_xterm_cursor(event):
		    text.config(cursor='xterm')
		def click(event):
		    webbrowser.open('https://help.mail.163.com/faq.do?m=list&categoryID=197')
		#鼠标指向
		text.tag_bind('link', '<Enter>', show_hand_cursor)
		#鼠标离开
		text.tag_bind('link', '<Leave>', show_xterm_cursor)
		#左键点击
		text.tag_bind('link', '<Button-1>', click)

#		self.w163_ui.mainloop()


	def aliyun_refresh(self):
		self.aliyun_ui.destroy()
		self.aliyun_login()


	def ali_check(self):
		self.aliyun_ui.withdraw()         #隐藏上一层窗口
		self.aliyun_check=Tkinter.Tk()
		self.aliyun_check.title("登录检查")
		self.aliyun_check.geometry("240x240")
		self.aliyun_check.configure(bg="PeachPuff")
		self.aliyun_check.resizable(0,0)     #固定窗口
		try:
			self.user=self.aliyun_user.get() #从登录文本框中获得邮箱账户
			self.passwd=self.aliyun_pw.get() #获得密码
			self.smtp_server='smtp.aliyun.com'
			self.pop_server='pop3.aliyun.com'
		except:
			Tkinter.Label(self.aliyun_check,text='please check your input',font=('宋体',14),bg='PeachPuff').pack()

		try:
			self.server= smtplib.SMTP()   #获得SMTP对象
			self.server.connect(self.smtp_server,25)
			Tkinter.Label(self.aliyun_check,text='connect success',font=('宋体',14),bg='PeachPuff').pack()
		except Exception as e:
			print 'ERROR->' +str(e)
			Tkinter.Label(self.aliyun_check,text='connect error',font=('宋体',14),bg='PeachPuff').pack()

		try:
			self.server.login(self.user,self.passwd)
			self.server.quit()
			Tkinter.Label(self.aliyun_check,text='登录成功',font=('宋体',14),bg='PeachPuff').pack()
			Tkinter.Button(self.aliyun_check,text='确定',font=('宋体',12),bg='PeachPuff',height=2,width=10,command=self.mail_window).pack()
		except Exception as e:
			print 'login error' +str(e)
			Tkinter.Label(self.aliyun_check,text='请检查你的邮箱账户或密码',font=('宋体',14),bg='PeachPuff').pack()
#		self.aliyun_check.mainloop()




	def aliyun_login(self):
		self.root.withdraw()
		self.aliyun_ui=Tkinter.Tk()
		self.aliyun_ui.title("欢迎登录")
		self.aliyun_ui.geometry("440x440")
		self.aliyun_ui.resizable(0,0)
		self.aliyun_ui.configure(bg='PeachPuff')
	
		self.aliyun_user=Tkinter.StringVar()     #textvariable将变量与Entry绑定
		self.aliyun_pw=Tkinter.StringVar()
		Tkinter.Label(self.aliyun_ui,text='欢迎登录阿里云邮箱',font=("宋体",20),width=44,height=5,bg='PeachPuff').pack(side='top')
		Tkinter.Label(self.aliyun_ui,text='邮箱地址:',font=('宋体',12),bg='PeachPuff').place(x=85,y=150)
		self.aliyun_user=Tkinter.Entry(self.aliyun_ui,textvariable=self.aliyun_user)
		self.aliyun_user.place(x=160,y=150)
		Tkinter.Label(self.aliyun_ui,text='密码 :',font=('宋体',12),bg='PeachPuff').place(x=85,y=190)
		self.aliyun_pw=Tkinter.Entry(self.aliyun_ui,show='*',textvariable=self.aliyun_pw)
		self.aliyun_pw.place(x=160,y=190)
		Tkinter.Button(self.aliyun_ui,text='确定',font=('宋体',12),bg='PeachPuff',width=10,height=2,command=self.ali_check).place(x=95,y=250)
		Tkinter.Button(self.aliyun_ui,text='取消',font=('宋体',12),bg='PeachPuff',width=10,height=2,command=self.aliyun_refresh).place(x=210,y=250)
		Tkinter.Button(self.aliyun_ui,text='上一步',font=('宋体',12),bg='PeachPuff',width=10,height=2,command=self.aliyun_ui.destroy).place(x=340,y=380)
		#阿里云直接使用账号密码登录，无需使用授权码
		'''text = Tkinter.Text(self.aliyun_ui,font=('宋体',12),height=2,width=12,bg='PeachPuff')   #添加一个超链接
	
		text.pack(side='left',anchor='se')
		text.insert(Tkinter.INSERT,'什么是授权码？')
		text.tag_add("link", '1.0', '1.19')          #指定tag名为link，从第一行的第0个到第一行第19列
		text.tag_config('link', foreground='blue', underline=True)   #为tag附加背景属性
		#绑定事件一定要传入event
		def show_hand_cursor(event):
		    text.config(cursor='arrow')
		def show_xterm_cursor(event):
		    text.config(cursor='xterm')
		def click(event):
		    webbrowser.open('https://help.mail.163.com/faq.do?m=list&categoryID=197')
		#鼠标指向
		text.tag_bind('link', '<Enter>', show_hand_cursor)
		#鼠标离开
		text.tag_bind('link', '<Leave>', show_xterm_cursor)
		#左键点击
		text.tag_bind('link', '<Button-1>', click)
		'''

		self.aliyun_ui.mainloop()


	def else_refresh(self):
		self.else_ui.destroy()
		self.else_login()


	def else_check(self):
		self.else_ui.withdraw()         #隐藏上一层窗口
		self.else_check=Tkinter.Tk()
		self.else_check.title("登录检查")
		self.else_check.geometry("240x240")
		self.else_check.configure(bg="LightGoldenrodYellow")
		self.else_check.resizable(0,0)     #固定窗口
		try:
			self.user=self.else_user.get() #从登录文本框中获得邮箱账户
			self.passwd=self.else_pw.get() #获得密码
			self.smtp_server="smtp." + self.user[self.user.index('@')+1:]
			self.pop_server="pop." + self.user[self.user.index('@')+1:]
		except:
			Tkinter.Label(self.else_check,text='please check your input',font=('宋体',14),bg='LightGoldenrodYellow').pack()

		try:
			self.server= smtplib.SMTP()   #获得SMTP对象
			self.server.connect(self.smtp_server,25)
			Tkinter.Label(self.else_check,text='connect success',font=('宋体',14),bg='LightGoldenrodYellow').pack()
		except Exception as e:
			print 'ERROR->' +str(e)
			Tkinter.Label(self.else_check,text='connect error',font=('宋体',14),bg='LightGoldenrodYellow').pack()

		try:
			self.server.login(self.user,self.passwd)
			self.server.quit()
			Tkinter.Label(self.else_check,text='登录成功',font=('宋体',14),bg='LightGoldenrodYellow').pack()
			Tkinter.Button(self.else_check,text='确定',font=('宋体',12),bg='LightGoldenrodYellow',height=2,width=10,command=self.mail_window).pack()
		except Exception as e:
			print 'login error' +str(e)
			Tkinter.Label(self.else_check,text='请检查你的邮箱账户或密码',font=('宋体',14),bg='LightGoldenrodYellow').pack()


	def else_login(self):
		self.root.withdraw()
		self.else_ui=Tkinter.Tk()
		self.else_ui.title("欢迎登录")
		self.else_ui.geometry("440x440")
		self.else_ui.resizable(0,0)
		self.else_ui.configure(bg='LightGoldenrodYellow')
	
		self.else_user=Tkinter.StringVar()     #textvariable将变量与Entry绑定
		self.else_pw=Tkinter.StringVar()
		Tkinter.Label(self.else_ui,text='欢迎登录你的专属邮箱',font=("宋体",20),width=44,height=5,bg='LightGoldenrodYellow').pack(side='top')
		Tkinter.Label(self.else_ui,text='邮箱地址:',font=('宋体',12),bg='LightGoldenrodYellow').place(x=85,y=150)
		self.else_user=Tkinter.Entry(self.else_ui,textvariable=self.else_user)
		self.else_user.place(x=160,y=150)
		Tkinter.Label(self.else_ui,text='密码 :',font=('宋体',12),bg='LightGoldenrodYellow').place(x=85,y=190)
		self.else_pw=Tkinter.Entry(self.else_ui,show='*',textvariable=self.else_pw)
		self.else_pw.place(x=160,y=190)
		Tkinter.Button(self.else_ui,text='确定',font=('宋体',12),bg='LightGoldenrodYellow',width=10,height=2,command=self.else_check).place(x=95,y=250)
		Tkinter.Button(self.else_ui,text='取消',font=('宋体',12),bg='LightGoldenrodYellow',width=10,height=2,command=self.else_refresh).place(x=210,y=250)
		Tkinter.Button(self.else_ui,text='上一步',font=('宋体',12),bg='LightGoldenrodYellow',width=10,height=2,command=self.else_ui.destroy).place(x=340,y=380)






	def main(self):
		self.root.title("welcome")
		self.root.geometry("440x440")
		self.root.resizable(0,0)          #固定窗口
		self.root.configure(bg='white')

		def resize(w_box,h_box,pil_image):                #调整图片不会随着按钮大小而发生变化
			w,h=pil_image.size
			f1=1.0*w_box/w
			f2=1.0*h_box/h
			factor=min([f1,f2])
			width=int(w*factor)
			height=int(h*factor)
			return pil_image.resize((width,height),Image.ANTIALIAS)

		w_box=100
		h_box=100
		qq_open=Image.open('../image/qq.jpg')
		qq_open_resize=resize(w_box,h_box,qq_open)
		button_qq=ImageTk.PhotoImage(qq_open_resize)
		w163_open=Image.open('../image/163.jpg')
		w163_open_resize=resize(w_box,h_box,w163_open)
		button_163=ImageTk.PhotoImage(w163_open_resize)
		aliyun_open=Image.open('../image/aliyun.jpg')
		aliyun_open_resize=resize(w_box,h_box,aliyun_open)
		button_aliyun=ImageTk.PhotoImage(aliyun_open_resize)
		else_open=Image.open('../image/else.jpg')
		else_open_resize=resize(w_box,h_box,else_open)
		button_else=ImageTk.PhotoImage(else_open_resize)

		Tkinter.Button(self.root,text='腾讯邮箱',font=("宋体",12),image=button_qq,width=440,height=90,bg='white',command=self.qq_login).pack()
		Tkinter.Button(self.root,text='网易邮箱',font=("宋体",12),image=button_163,width=440,height=90,bg='white',command=self.w163_login).pack()
		Tkinter.Button(self.root,text='阿里云邮箱',font=("宋体",12),image=button_aliyun,width=440,height=90,bg='white',command=self.aliyun_login).pack()
		Tkinter.Button(self.root,text='其他邮箱',font=("宋体",12),image=button_else,width=440,height=90,bg='white',command=self.else_login).pack()
		Tkinter.Button(self.root,text='退出',font=("宋体",12),bg='LightCyan',width=10,height=2,command=self.root.destroy).pack(side='right')
		self.root.mainloop()

if __name__=='__main__':
	Email_System().main()