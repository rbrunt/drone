import sqlite3
from lxml import etree, objectify
import re

def check_italic_tags_present(lines):
	"""Checks to see if the verse is wrapped in italics tags."""
	return lines[0][0:4]=="{it}" and lines[-1][-5:]=="{/it}"

def trim_italic_tags(lines):
	"""Remove italic tags from beginning and end of verse"""
	if check_italic_tags_present(lines):
		#only intersted in changing the first and last lines, otherwise we might interfere with other formatting tags!
		lines[0] = re.sub(r"(^{it})", "", lines[0])
		lines[-1] = re.sub(r"({ */it}$)", "", lines[-1])
	return lines
	
def add_italic_tags(lines):
	"""Add wrapping italic tags to verse"""
	if not check_italic_tags_present(lines):
		lines[0] = "{it}" + lines[0]
		lines[-1] = lines[-1] + "{/it}"
	return lines



conn = sqlite3.connect("songs.sqlite")
c = conn.cursor()

c.execute("SELECT lyrics from songs")


xml = c.fetchone()[0]

#xmlfile = open("lyrics.xml", "w")
#xmlfile.write(xml.encode("UTF-8"))
#xmlfile.close()

try:
	song_xml = objectify.fromstring(xml[38:])
except etree.XMLSyntaxError:
	exit("error")

verses = song_xml.lyrics.verse
newverses = []
for i in xrange(len(verses)):

	attribs = verses[i].attrib
	text = verses[i].text
	if attribs["type"]=="c":
		lines = trim_italic_tags(text.split("\n"))
		text = "\n".join(lines)
	verse = etree.Element('verse', **attribs)
	verse.text = etree.CDATA(text)
	newverses.append(verse)
	
song_xml.lyrics.verse = newverses


generatedxml = etree.tostring(song_xml, encoding='UTF-8', xml_declaration=True)

conn.text_factory = str
c.execute("UPDATE songs SET lyrics=? WHERE id=4;", [generatedxml])
conn.commit()
#xmlfile = open("lyrics2.xml", "w")
#xmlfile.write(generatedxml)
#xmlfile.close()



conn.close()
