import re

# Precompile regex which will be used fairly extensively:
generic_tag_regex = re.compile(r"(^\{(\w+)\}).*(\{/(\2)\}$)", re.DOTALL)

def get_wrapping_tags(text):
	"""Get the name of the tags wrapping the text. Return None if there aren't any"""
	match =  re.match(generic_tag_regex, text.strip())
	if match != None:
		return match.group(2)
	else:
		return None

def check_generic_tag_wrap(text):
	"""Check if the text is wrapped by __matching__, but indeterminate, tags"""
	return get_wrapping_tags(text) != None

def check_tag_wrap(tag, text):
	"""Checks to see if the give OpenLP tags wrap the verse or not"""
	return get_wrapping_tags(text) == tag

def add_tags(tag, text):
	if not check_tag_wrap(tag, text):
		return "{{{tag}}}".format(tag=tag) + text.strip() + "{{/{tag}}}".format(tag=tag)
	else:
		return text


def check_italic_tags_present(text):
	"""Checks to see if the verse is wrapped in italics tags."""
	return check_tag_wrap("it", text)

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