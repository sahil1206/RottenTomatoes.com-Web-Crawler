# Creator: Sahil Jain (sahil206@kgpian.iitkgp.ac.in)
# Roll No: 20CS60R64
# Description: Web Crawler

#HEADER FILES
import ply.lex as lex
import ply.yacc as yacc
import unicodedata 
import sys
import os
import task1 as t1

# GLOBAL VARIABLES 
result = {}
producer = []
director = []
writer=[]
cast = []
collection = "NA"

# Lexical Analyzer starts Here
tokens = [
	'NAME_OPEN',
	'NAME_CLOSE',
	'StoryS',
	'StoryE',
	'DIV',
	'OLS',
	'RTS',
	'RTE',
	'CS',
	'PS',
	'LINK',
	'ANCHOR',
	'DS',
	'WS',
	'SpanTitle',
	'SPAN',
	'SpanClass',
	'BR',
	'ALL'
	]

# TOKEN DEFINITION
t_NAME_OPEN					=	r'''<title>'''
t_NAME_CLOSE				=	r'''</title>'''
t_DIV						= 	r'''</div>'''
t_ANCHOR					=	r'''</a>[,\s]*'''
t_SPAN 						=	r'''</span>[\s]*'''
t_BR						=	r'''<br/>[\s]*'''
t_RTS                       =   r'''<time\ datetime="P[\w\d\ ]+M">[\s]+'''
t_RTE                       =   r'''</time>'''
t_StoryS					=	r'''<meta\ name="description"\ content='''
t_StoryE					=	r'''>[\s]+<link'''
t_CS 						=   r'''<div\ class="meta-label\ subtle"\ data-qa="movie-info-item-label">Box[\d\w ()]+:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">'''
t_PS						=   r'''Producer:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">[\s]+'''
t_WS						=   r'''Writer:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">[\s]+'''
t_OLS 						= 	r'''Original\ Language:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">'''
t_LINK						= 	r'''<a\ href="/celebrity/[\d\w()\-\ _ "=]+>'''
t_DS						=   r'''Director:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">[\s]+'''
t_SpanTitle					=	r'''<span\ title=[\d\w()\-\ _ "=]+>[\s]+'''
t_SpanClass					=	r'''<span\ class="characters\ subtle\ smaller"\ title=[\d\w()\-\ _ "=]+>[\s]+'''
t_ALL						= 	r'''[\d\w() -.'\"()\s\$]+'''



def t_error(t):
	#print("Illegal character '%s'" % t.value[0])
	t.lexer.skip(1)

def p_start(p):
	'''Start : S1
			| S2
			| S3
			| S4
			| S5
			| S6
			| S7
			| S8
			| S9
			'''

def p_movie_name(p):
	#'Start : NAME_OPEN CONTENT NAME_CLOSE'
	'S1 : NAME_OPEN ALL NAME_CLOSE'
	movie_name_parsed = p[2]
	result['Movie Name'] = movie_name_parsed.strip("- Rotten Tomatoes")
	#print("MOVIE NAME: " + movie_name_parsed.strip("- Rotten Tomatoes"))

def p_story(p):
	'S2 : StoryS ALL StoryE'
	storyline = str(p[2])
	result['storyline'] = storyline.strip('\"')
	#print("storyline = "+storyline)

def p_Original_language(p):
	#'Start : NAME_OPEN CONTENT NAME_CLOSE'
	'S3 : OLS ALL DIV'
	Ol = p[2]
	result['Original_language'] = Ol.strip().rstrip("\n")
	#print("ol = "+(Ol.rstrip("\n")))

def p_runtime(p):
	'S4 : RTS ALL RTE'
	runtime = p[2]
	result['Runtime'] = runtime.strip().rstrip("\n")
	#print("Runtime = "+(runtime))

def p_collection(p):
	'S5 : CS ALL DIV'
	collection_r = p[2]
	if len(collection_r)!=0:
		global collection
		collection = collection_r
	#print("BOX OFFICE COLLECTION: " + (collection))

def p_producer(p):
	'S6 : PS pname DIV'
	#print(p[3])

def p_pname(p):
	'''pname : LINK ALL ANCHOR pname
			| LINK ALL ANCHOR'''
	temp = p[2]
	producer.append(temp)

def p_director(p):
	'S7 : DS dname DIV'
	#print(p[3])

def p_dname(p):
	'''dname : LINK ALL ANCHOR dname
			| LINK ALL ANCHOR'''	
	temp = p[2]
	director.append(temp)	

def p_writer(p):
	'S8 : WS writerName DIV'
	#print(p[3])

def p_writerName(p):
	'''writerName : LINK ALL ANCHOR writerName
			| LINK ALL ANCHOR'''
	temp = p[2]
	writer.append(temp)

def p_cast(p):
	'S9 : SpanTitle ALL SPAN ANCHOR SpanClass BR ALL'
	cast_name = p[2].strip()
	role = p[7].strip()
	concated = cast_name + " as " + role
	cast.append(concated) 


def p_error(p):
	pass

#Function to convert all latin alphabets to english ..
def strip_accents(text):
    return ''.join(char for char in unicodedata.normalize('NFKD', text) if unicodedata.category(char) != 'Mn')

def log_entry(genre,movie_name,field_name,value):
    f = open("log_file", 'a+')
    entry = str(genre) + "\t" + str(movie_name) + "\t" + str(field_name) + "\t" + str(value) + "\n"
    f.write(entry)
    f.close    

def read_html(movie_name):
	myfile = open(movie_name, 'r')
	data = myfile.read()
	#print(data)
	data = strip_accents(data)
	lexer = lex.lex()
	parser = yacc.yacc()
	parser.parse(data)
	print("Parsing Done!")

def main():
	t1.main()
	movie_name = t1.m_name
	genre = t1.genre
	read_html(movie_name)
	#print(result)
	#print(producer)
	#print(director)
	#print(writer)
	#print(cast)
	print("What info of "+movie_name+" you want to know?")
	print("Movie Name\nDirectors\nWriters\nProducers\nOriginal Language\nCast\nStoryline\nBox Office Collection\nRuntime")
	print("\"stop\" to exit--\n")
	# to take input from user 
	while(True):
		uinput = input("Enter Field from Above List or Stop to exit -\n")
		uinput = uinput.lower()

		if uinput == 'movie name':
			print(result['Movie Name'])
			log_entry(movie_name,genre,'Movie Name',result['Movie Name'])
			print("\n")

		elif uinput == 'original language':
			print(result['Original_language'])
			log_entry(movie_name,genre,'Original Language',result['Original_language'])
			print("\n")

		elif uinput == 'box office collection':
			print(collection)
			log_entry(movie_name,genre,'Collection',collection)
			
		elif uinput == 'storyline':
			print(result['storyline'])
			log_entry(movie_name,genre,'storyline',result['storyline'])
			
		elif uinput == 'directors':
			for i in range(len(director)):
				print(director[i])
				log_entry(movie_name,genre,'Director',director[i])
			
		elif uinput == 'writers':
			for i in range(len(writer)):
				print(writer[i])
				log_entry(movie_name,genre,'writers',writer[i])
		
		elif uinput == 'producers':
			for i in range(len(producer)):
				print(producer[i])
				log_entry(movie_name,genre,'Producer',producer[i])

		elif uinput == 'cast':
			for i in range(len(cast)):
				print(cast[i])
				log_entry(movie_name,genre,'Cast',cast[i])
		elif uinput == 'stop':
			print("Okay! Thank you!")
			response = input("Do you want to Scrap another movie? (Y/N)")
			if response =="Y":
				t1.main()
			elif response =="N":
				print("Exiting...")
				break	
			else:
				print("Incorrect Chooice!")
		
		else:
			print("Oops! Input Field didn't Match, Enter field from given list!\n")	

if __name__ == "__main__":
	main()
