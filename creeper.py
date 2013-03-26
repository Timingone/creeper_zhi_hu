#!/usr/bin python
import urllib, urllib2, cookielib, re, sys ,heapq

class zhihu(object):

	def __init__(self,email,password):
		self.email = email
		self.password = password
		self.domain = "www.zhihu.com"
		self.cj = cookielib.CookieJar()
		try:
			self.cj.revert("zhihu.cookie")
		except:
			None
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
		urllib2.install_opener(self.opener)

	def login(self):
		headers = {
			'Accept' :'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8' ,
			'Accept-Language':	'en-US,en;q=0.5' ,
			'Connection':	'keep-alive' ,
			'Cookie' : "_xsrf=36364b6f555c4f86a3c087ea34a4c277; __utma=155987696.1141709383.1361953906.1361953906.1361956716.2; __utmc=155987696; __utmz=155987696.1361956716.2.2.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=155987696.Not%20Logged%20In; __utmb=155987696.19.9.1361956978668",
			'Host':	'www.zhihu.com' ,
			'Referer':	'https://www.zhihu.com/login' ,
			'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:19.0) Gecko/20100101 Firefox/19.0' ,
		}
		info = {
			'_xsrf' : "36364b6f555c4f86a3c087ea34a4c277" ,
			'email' : self.email ,
			'next' : "/" ,
			'password' : self.password ,
			'rememberme' : "on"
		}

		req = urllib2.Request(
			"https://www.zhihu.com/login",
			urllib.urlencode(info),
			headers,
			"http://www.zhihu.com/"
		)

		r = self.opener.open(req)	

	def followees(self):
		req = "http://www.zhihu.com/people/yu-wei-21/followees"
		#r = self.opener.open(req)
		#data = r.read()
		#filename = "zhihu.fri"
		#fp = open(filename,"w+")
		#fp.write(data)	
		print "login ok"
		print "Get my followees"
		self.visited = []
		self.todo = []
		self.all = {}
		self.BFS(req)

	def BFS(self,url):
		heapq.heappush(self.todo,(0,url,"me"))
		while self.todo != [] :
			new = heapq.heappop(self.todo)
			print -new[0],new[2]
			url = new[1]
			if url.find("http://www.zhihu.com") == -1 :
				url = "http://www.zhihu.com" + url + "/followees"
			if url in self.visited :
				continue
			self.visited.append(url)
			self.all[new[2]] = -new[0]
			print url
			r = self.opener.open(url)
			data_page = r.read()
			followees = re.findall('(?<=h2).+?(?=h2)',data_page)
			followees_fo_count = re.findall("(?<=followers\" class=\"zg-link-gray-normal\">)\d+",data_page)
			data_followees = ""
			for i in followees :
				data_followees += i+'\n' 
			followees_name = re.findall('(?<=\>)[^"]+?(?=\<)',data_followees)
			followees_url = re.findall('(?<=href=").+?(?=")',data_followees)
			for i in range(len(followees_url)):
				# print followees_name[i],followees_fo_count[i]
				heapq.heappush(self.todo,(-int(followees_fo_count[i]),followees_url[i],followees_name[i]))
				#print i 
			# for i in followees_name:
			# 	print i 
			# while len(self.todo) > 0 :
			# 	print heapq.heappop(self.todo) 
			if len(self.visited) > 100:
				break
		print "todo list is empty."

if __name__ == "__main__":
	email = ""
	password = ""
	h = zhihu(email,password)
	h.login()
	h.followees()
	for i in h.all.keys():
		print i,h.all[i]
