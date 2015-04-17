import sqlite3
from lxml import etree, objectify
import re

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



conn = sqlite3.connect("songs.sqlite")
conn.text_factory = str
c = conn.cursor()

c.execute("SELECT lyrics from songs")


xmllist = c.fetchall()


italics = "add"

for xmlindex in xrange(len(xmllist)):
	try:
		song_xml = objectify.fromstring(xmllist[xmlindex][0][38:])
	except etree.XMLSyntaxError:
		exit("error")

	verses = song_xml.lyrics.verse
	newverses = []
	for i in xrange(len(verses)):

		attribs = verses[i].attrib
		text = verses[i].text
		if attribs["type"]=="c":
			if italics == "add":
				text = add_italic_tags(text)
			elif italics == "remove":
				text = trim_italic_tags(text)
		verse = etree.Element('verse', **attribs)
		verse.text = etree.CDATA(text)
		newverses.append(verse)
		
	song_xml.lyrics.verse = newverses


	generatedxml = etree.tostring(song_xml, encoding='UTF-8', xml_declaration=True)

	c.execute("UPDATE songs SET lyrics=? WHERE id=?;", [generatedxml, xmlindex+1])
	conn.commit()



conn.close()
