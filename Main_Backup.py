import nltk
import MySQLdb


def find_adverbs(sent):
	adv =[]
	text = nltk.word_tokenize(sent)
	tagged_words = nltk.pos_tag(text)
	for word in tagged_words:
		if (word[1] == 'RB') | (word[1] == 'RBR') | (word[1] == 'RBS'):
			adv.append(word[0])
	return adv

def find_adjectives(sent):
	adj =[]
	text = nltk.word_tokenize(sent)
	tagged_words = nltk.pos_tag(text)
	for word in tagged_words:
		if (word[1] == 'JJ') | (word[1] == 'JJR') | (word[1] == 'JJS'):
			adj.append(word[0])
	return adj

	

# Create a connection object and create a cursor
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="Sentiments")
Cursor = Con.cursor()

# Make SQL string and execute it
sql = "SELECT * FROM Polarity"
Cursor.execute(sql)

# Fetch all results from the cursor into a sequence and close the connection
results = Cursor.fetchall()
Con.close()

tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')

fin = open("Input.txt","r")
input_string = fin.read()
fin.close()

sents = tokenizer.tokenize(input_string)

sentence_collection = []
for items in sents:
	sentence_collection.append(nltk.word_tokenize(items))

#	Collection of sentences and words ::
#print sentence_collection[3][3]
	

for sent in sents:
	sent = sent.strip('\n')
	print sent
	curr_val = 0	
	#Dealing with adverbs
	list_of_adverbs = find_adverbs(sent)
	
	for adv in list_of_adverbs:
		for item in results:
			if (item[0].lower() == adv.lower()):
				curr_val = curr_val + (item[1] * item[2])
		
		print "Adverb : " , adv 

	# Dealing with adjectives
	list_of_adjectives = find_adjectives(sent)
	
	for adv in list_of_adjectives:
		for item in results:
			if (item[0].lower() == adv.lower()):
				curr_val = curr_val + (item[1] * item[2])
		
		print "Adjective : " , adv 
	
	print "Weightage: " , curr_val

	print


