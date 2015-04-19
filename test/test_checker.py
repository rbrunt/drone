import nose
import drone.tags as tags

def test_get_wrapping_tags():
	assert tags.get_wrapping_tags("{it}Test{/it}") == "it"
	assert tags.get_wrapping_tags("{st}{it}Test{/it}{/st}") == "st"

def test_generic_tag_wrap():
	assert tags.check_generic_tag_wrap("{it}Test{/it}") == True
	assert tags.check_generic_tag_wrap("{it}Mismatched Tags{/st}") == False
	assert tags.check_generic_tag_wrap("{st}Test\nAnother Line\n And another.\n[--]\nThat was a break{/st}") == True
	assert tags.check_generic_tag_wrap("Test") == False
	assert tags.check_generic_tag_wrap("{st}{it}Double Tags{/it}{/st}") == True

def test_tag_wrap():
	assert tags.check_tag_wrap("it","{it}Testing{/it}") == True
	assert tags.check_tag_wrap("it","{it}Testing\nTag Wrapping{/it}") == True
	assert tags.check_tag_wrap("it","{it}Testing\nTag Wrapping{/it} ") == True
	assert tags.check_tag_wrap("st","{it}Testing\nTag Wrapping{/it} ") == False
	assert tags.check_tag_wrap("st","{it}{st}Testing{/st}{/it}") == True


def test_add_tags():
	assert tags.add_tags("it","Testing") == "{it}Testing{/it}"
	assert tags.add_tags("it","Testing ") == "{it}Testing{/it}"
	assert tags.add_tags("st","Testing\nTag Wrapping") == "{st}Testing\nTag Wrapping{/st}"
	assert tags.add_tags("it","{it}Testing{/it}") == "{it}Testing{/it}"
	assert tags.add_tags("st","{it}Testing{/it}") == "{st}{it}Testing{/it}{/st}"
