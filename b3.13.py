class HTML:
	def __init__(self,output=None):
		self.output=output
		self.children=[]
	def __enter__(self):
		return self	
	def __exit__(self, *args, **kwargs):	
		if self.output is not None:
			with open(self.output,"w") as fp:
				fp.write(str(self))	
		else:
		    print(self)

	def __str__	(self):
		html="<html>\n"
		for child in self.children:
			html+=str(child)
		html+="\n</html>"	

		return html	

	def __iadd__ (self,other):
		self.children.append(other)
		return self
			

		
class Tag:
	def __init__(self, tag, toplevel=False,id=None, is_single=False, klass=None,*args, **kwargs):
		self.tag = tag
		self.text = ""
		self.attributes = {}

		self.toplevel = toplevel
		self.is_single = is_single
		self.children = []
		if klass is not None:
			for kl in klass:
				self.attributes["class"] = " ".join(klass)
		if id is not None:
			self.attributes["id"]="".join(id)		
		for attr, value in kwargs.items():
			if "_" in attr:
				attr = attr.replace("_", "-")
				self.attributes[attr] = value  
			else:
				self.attributes[attr] = value	
	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		if self.toplevel:
			print("<%s>" % self.tag)
			for child in self.children:
				print(child)

			print("</%s>" % self.tag)

	def __str__(self):
		attrs = []
		for attribute, value in self.attributes.items():
			attrs.append('%s="%s"' % (attribute, value))
		attrs = " ".join(attrs)

		if self.children:
			opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
			internal = "%s" % self.text
			for child in self.children:
				internal += str(child)
			ending = "</%s>\n" % self.tag
			return opening + internal + ending
		else:
			if self.is_single:
				return "<{tag} {attrs}/>\n".format(tag=self.tag, attrs=attrs)

			else:
				return "<{tag} {attrs}>{text}</{tag}>\n".format(tag=self.tag, attrs=attrs, text=self.text)
	
	def __iadd__(self, other):
		self.children.append(other)
		return self	          


class TopLevelTag:
	def __init__(self,tag):
		self.children=[]
		self.tag = tag

	def __str__(self):
		  html="<%s>\n" % self.tag
		  for child in self.children:
			  html+=str(child)
		  html+="\n</%s>\n" % self.tag
		  return html 
	def __iadd__(self, other):
		self.children.append(other)
		return self	       
	def __enter__(self):
		return self
	def __exit__(self, *args, **kwargs):
		pass	
   
 
if __name__ == "__main__":
	with HTML(output=None) as doc:
		with TopLevelTag("head") as head:
			with Tag("title") as title:
				title.text = "hello"
				head += title
			doc += head

		with TopLevelTag("body") as body:
			with Tag("h1", klass=("main-text",)) as h1:
				h1.text = "Test"
				body += h1

			with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
				with Tag("p") as paragraph:
					paragraph.text = "another test"
					div += paragraph

				with Tag("img", is_single=True, src="/icon.png", data_image="responsive") as img:
					div += img

				body += div

			doc += body
