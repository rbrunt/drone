import sqlite3
from lxml import etree, objectify
import tags, db

italics = "add"

def main():
	#Make a backup!
	db.backup_db()
	conn = sqlite3.connect(db.get_songs_db_path())
	conn.text_factory = str
	c = conn.cursor()

	c.execute("SELECT lyrics from songs")


	xmllist = c.fetchall()

	for xmlindex in xrange(len(xmllist)):
		try:
			song_xml = objectify.fromstring(xmllist[xmlindex][0][38:]) # Cut the first 38 characters (xml preamble) off.
		except etree.XMLSyntaxError:
			exit("error")

		verses = song_xml.lyrics.verse
		newverses = []
		for i in xrange(len(verses)):

			attribs = verses[i].attrib
			text = verses[i].text
			if attribs["type"]=="c":
				if italics == "add":
					text = tags.add_italic_tags(text)
				elif italics == "remove":
					text = tags.trim_italic_tags(text)
			verse = etree.Element('verse', **attribs)
			verse.text = etree.CDATA(text)
			newverses.append(verse)
			
		song_xml.lyrics.verse = newverses


		generatedxml = etree.tostring(song_xml, encoding='UTF-8', xml_declaration=True)

		c.execute("UPDATE songs SET lyrics=? WHERE id=?;", [generatedxml, xmlindex+1])
		conn.commit()



	conn.close()
