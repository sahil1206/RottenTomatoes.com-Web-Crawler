# Creator: Sahil Jain (sahil206@kgpian.iitkgp.ac.in)
# Roll No: 20CS60R64
# Description: HTML Downloader

import urllib.request, urllib.error, urllib.parse
import re

URL_FILE="URL.txt"

def extract_content(url):
    response = urllib.request.urlopen(url)
    webContent = response.read()
    return webContent

def extract_name(line):
	line = line.strip()
	num,line = line.split(".",1)
	line = line.strip().replace(':','')
	return line
def list_movies(file_name):
	test_str = open(file_name, 'r').read()
	regex =  r"<a\shref=\"\/m\/([a-zA-Z0-9\-\/_]+)\"\sclass=\"unstyled articleLink\">[^\\n*]\s*([a-zA-Z0-9.,:\-\'()[^\s]+]*)"
	matches = re.finditer(regex, test_str, re.MULTILINE | re.IGNORECASE)
	movie_dict = {}
	for matchNum, match in enumerate(matches, start=1):
		print(match.group(2))
		movie_dict[match.group(2).lower()] = match.group(1)
	return movie_dict

def write_html(webcontent,file_name):
    f = open(file_name, 'wb')
    f.write(webcontent)
    f.close


def main():  
	#print("TASK 1 running!")  
	f=open(URL_FILE,'r')
	fr=f.readline()
	fr = f.readlines()
	print("Action &Adventure\nAnimation\nDrama\nComedy\nMystery & Suspense\nHorror\nSci-Fi\nDocumentary\nRomance\nClassics\n")
	global genre
	genre = input("Enter Genre from the list Above:")
	
	genre_lower = genre.lower()
	flag = 0
	for line in fr:
		if line[0:5] != 'https':
			name = extract_name(line)
			if name.lower() == genre_lower:
				flag = 1
			else:
				flag = 0
		else:
			if flag==1 :
				print(name)
				content =  extract_content(line)
				write_html(content,name)
				break


	movie_list = list_movies(genre)


	movie_name = input("\nEnter the name of movie to be retrieved from above list\n")
	global m_name
	m_name = movie_name 
	m_url = movie_list.get(movie_name.lower())
	if m_url:
		m_url = "https://www.rottentomatoes.com/m/" + m_url
		#print(m_url)
	else:
		print("Invalid movie name (hint: provide year also")

	m_content = extract_content(m_url)
	write_html(m_content,movie_name)


if __name__=="__main__":
	main()