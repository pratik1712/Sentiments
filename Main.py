import nltk
import MySQLdb

# extracting adverbs from the sentences
def find_adverbs(tagged_words):
	adv =[]
	for index, word in enumerate(tagged_words):
		if (word[1] == 'RB') | (word[1] == 'RBR') | (word[1] == 'RBS'):
			value = []
			value.append(index)
			value.append(word[0])
			adv.append(value)
	return adv

# extracting adjectives from the sentences
def find_adjectives(tagged_words):
	adj =[]
	for index, word in enumerate(tagged_words):
		if (word[1] == 'JJ') | (word[1] == 'JJR') | (word[1] == 'JJS'):
			value = []
			value.append(index)
			value.append(word[0])
			adj.append(value)
	return adj

	

# Create a connection object and create a cursor
Con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="Sentiments")
Cursor = Con.cursor()

# Make SQL string and execute it
sql = "SELECT * FROM Polarity"
Cursor.execute(sql)

# Fetch all results from the cursor into a sequence and close the connection
# results contains the database entries for list of adjectives
results = Cursor.fetchall()
Con.close()

# input file
fin = open("Input.txt","r")
input_string = fin.read()
fin.close()

# spliting the paragraph to sentences
tokenizer=nltk.data.load('tokenizers/punkt/english.pickle')
sents = tokenizer.tokenize(input_string)

# creating a 2-D array [sentences][words] for eaiser access
sentence_collection = []
for items in sents:
	sentence_collection.append(nltk.word_tokenize(items.strip('\n')))


for sentence in sentence_collection:
	# tagging words with POS
	tagged_words = nltk.pos_tag(sentence)
	
	# extracing the list of adverbs and adjective and their position
	adverbs_list = find_adverbs(tagged_words)
	adjectives_list = find_adjectives(tagged_words)
	
	# for storing the weight of a sentence
	weightage = 0

	#print the original sentence
	print sentence	

	#looping all the adjectives for a sentence
	for adj in adjectives_list:
		print adj[1]

		# comparing with the database
		for entry in results:
			if (adj[1] ==	entry[0]):
				weightage = weightage + (entry[1] * entry[2])
		# checking for adverb in the vicinity
		for adv in adverbs_list:
			# if the adverb is next to previous to word add 1 
			# if there is a gap of a word in between add 0.5 to weight
			val_1_pos = [adj[0] - 1 , adj[0] + 1]
			val_2_pos = [adj[0] - 2 , adj[0] + 2]

			if adv[0] in val_1_pos:
				if weightage > 0:
					weightage = weightage + 1
				elif weightage < 0:
					weightage = weightage - 1		
			elif adv[0] in val_2_pos:
				if weightage > 0:
					weightage = weightage + 0.5
				elif weightage < 0:
					weightage = weightage - 0.5
	
	# the estimated weight of the sentence
	print weightage
