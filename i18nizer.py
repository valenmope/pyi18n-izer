import urllib
from bs4 import BeautifulSoup
import sys

for arg in sys.argv: 
	print arg

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]


#input_file = open('/home/valentin/development/cheerfy/frontend.cheerz.co/frontend/templates/index.html', 'r+')
input_file = open(input_file_name, 'r+')

html = input_file.read()
input_file.close()

html_cleaned = html.replace('{%', '<script>')
html_cleaned = html_cleaned.replace('%}', '</script>')

soup = BeautifulSoup(html_cleaned, "html.parser")

# kill all script and style elements
for script in soup(["script", "style"]):
  script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)



prefix = raw_input('Properties text prefix [xxx.yyy.zzz]: ')

replacement_set = {}
replacement_list = []
key_set = text.split('\n')
for entry in key_set:
  skip = False
  if entry in replacement_set:
    option = raw_input('Your entry:\n\t\t' + entry.encode('utf-8').strip() + '\n\tAlready stored with key: ' + replacement_set.get(entry).encode('utf-8') + '\n\tDo you want to keep same entry [1] or create a new one [2]? ')
    skip = True if option == 1 else False
  if not skip:
    key_id = raw_input('Your entry:\n\t\t' + entry.encode('utf-8').strip() + '\n\tInsert key id ' + ('[xxx.yyy.zzz]' if len(prefix) == 0 else '[' + prefix.encode('utf-8') + ']') + ' - (d) to discard: ')  	
    if key_id != 'd':
      replacement_set[entry] = key_id.encode('utf-8').strip()
      replacement_list.append(entry)

translation_content = ''
for entry in replacement_list:
  replacement_text = "{% trans '" + (prefix.encode('utf-8') + '.' if len(prefix) > 0 else '') + replacement_set.get(entry).encode('utf-8') + "' %}"
  html = html.replace(entry.encode('utf-8'), replacement_text)
  translation_content += 'msgid "' + replacement_set.get(entry).encode('utf-8') + '"\nmsgstr "' + entry.encode('utf-8').strip() + '"\n'

#1) empty input file
input_file = open(input_file_name, 'w').close()

#2) update input file with new content
input_file = open(input_file_name, 'w')
input_file.write(html)
input_file.flush()
input_file.close()

#3) update output file with new records
output_file = open(output_file_name, 'a')
output_file.write(translation_content)
output_file.flush()
output_file.close()