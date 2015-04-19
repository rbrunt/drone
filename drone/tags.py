import re


def check_generic_tag_wrap(text):
	#return re.match(r"(^\{\w+\}).*(\{/\w+\}$)", text.strip(), re.DOTALL) != None
	return re.match(r"(^\{(\w+)\}).*(\{/(\2)\}$)", text.strip(), re.DOTALL) != None # Require that the tags are the same...

def get_wrapping_tags(text):
	match =  re.match(r"(^\{(\w+)\}).*(\{/(\2)\}$)", text.strip(), re.DOTALL)
	return match.group(2)

def check_tag_wrap(tag, text):
	"""Checks to see if the give OpenLP tags wrap the verse or not"""
	text = text.strip()
	return text.startswith("{{{tag}}}".format(tag=tag)) and text.endswith("{{/{tag}}}".format(tag=tag))

def add_tags(tag, text):
	if not check_tag_wrap(tag, text):
		return "{{{tag}}}".format(tag=tag) + text.strip() + "{{/{tag}}}".format(tag=tag)
	else:
		return text

def check_italic_tags_present(text):
	"""Checks to see if the verse is wrapped in italics tags."""
	return text[0:4]=="{it}" and text[-5:]=="{/it}"

def trim_italic_tags(text):
	"""Remove italic tags from beginning and end of verse"""
	if check_italic_tags_present(text):
		#only intersted in changing the first and last lines, otherwise we might interfere with other formatting tags!
		text = re.sub(r"(^{it})", "", text)
		text = re.sub(r"({ */it}$)", "", text)
	return text
	
def add_italic_tags(text):
	"""Add wrapping italic tags to verse"""
	if not check_italic_tags_present(text):
		text = "{it}" + text
		text = text + "{/it}"
	return text