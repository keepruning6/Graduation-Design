# -*- coding:utf-8 -*-
import poplib
import datetime,time,sys,traceback
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

class Receive_Email():
	def __init__(self):
		'''
		self.email= email
		self.password= password
		self.pop3_server= pop3_server
		'''
		self.content=[]
		self.attach={}
	def decode_str(self,s):
		value,charset=decode_header(s)[0]   #
		if charset:
			value=value.decode(charset)
		return value


	def guess_charset(self,msg):    #获取msg编码
		charset = msg.get_charset()
		if charset is None:
			content_type =msg.get('Content-Type','').lower()
			pos = content_type.find('charset=')
			if pos >=0:
				charset=content_type[pos+8:].strip()
		return charset

	def email_header(self,msg,indent=0):
		header_list=[]
		if indent==0:
			for header in ['From','To','Subject']:
				value =msg.get(header,'')
				if value:
					if header=='Subject':
						subject =self.decode_str(value)
						header_list.append(subject)     #header_list[2]
					if header=='From':
						hdr,addr=parseaddr(value)
						name=self.decode_str(hdr)
						fro= u'%s <%s>' %(name,addr)
						header_list.append(fro)         #header_list[0]

					if header=='To':
						hdr,addr=parseaddr(value)
						name=self.decode_str(hdr)
						to_rece=u'%s %s' %(name,addr)
						header_list.append(to_rece)      #header_list[1]

		return header_list

	def email_time_size(self,msg):
		try:
		    date1 = time.strptime(msg.get("Date")[0:24], '%a, %d %b %Y %H:%M:%S') #获取时间并且格式化
		    date2 = time.strftime("%Y-%m-%d",date1)
		    return date2                               #邮件时间转化
		except Exception as e:
			pass
#			print str(e)





	def email_content(self,msg,flag=0):
		if flag==0:
			pass


		if (msg.is_multipart()):
			parts =msg.get_payload()
			for part in parts:
				self.email_content(part,flag+1)   #使用递归不断解析邮件
		else:
			content_type=msg.get_content_type()
			if content_type=='text/plain' or content_type=='text/html':
				content_part = msg.get_payload(decode=True)
				charset = self.guess_charset(msg)
				if charset:
					content_part = content_part.decode(charset)
					self.content.append(content_part)          #将每部分的正文内容添加
		return self.content                            




	def email_attachement(self,msg,flag=0):
		if flag==0:
			pass


		if (msg.is_multipart()):
			parts =msg.get_payload()
			for part in parts:
				self.email_attachement(part,flag+1)   #使用递归不断解析邮件
		else:
			content_type=msg.get_content_type()
			if content_type=='text/plain' or content_type=='text/html':
				pass
			else:
				for i in msg.walk():
					name =i.get_param("name")
					if name:
						name=self.decode_str(name)
		#				print "fujian",name
						data=i.get_payload(decode=True)
						data=self.decode_str(data)      #获取数据
		#				print data
						self.attach[name]=data
		return self.attach
if __name__=='__main__':
	pass
	'''
	rece=Receive_Email('2057764563@qq.com','lktqahdhmsufjgha','pop.qq.com')

	server = poplib.POP3(rece.pop3_server)
	server.set_debuglevel(1)
	print server.getwelcome().decode('utf-8')

	server.user(rece.email)
	server.pass_(rece.password)

	print 'Messages:%s.Size:%s' %server.stat()

	resp,mails,octects= server.list()

	print mails

	index = len(mails)
	while index>=1:
		try:
			resp,lines,octects=server.retr(index)
			msg_content = b'\r\n'.join(lines).decode('utf-8')
			msg =Parser().parsestr(msg_content)
			print index
			header_list=rece.email_header(msg,0)
			print header_list[2]
			tim=rece.email_time_size(msg)
			print tim
			content=rece.email_content(msg)
#			for i in range(0,len(content)):
#				print content[i]
			attachment=rece.email_attachement(msg)
			for key in attachment:
				print key+':'+attachment[key]
		except Exception as e:
			print e
		index=index-1
	server.quit()
	'''