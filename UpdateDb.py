import MySQLdb
import sys

fin = open("Positive_List.txt","r")
input_string_positive = fin.read()
fin.close()

fin = open("Negative_List.txt","r")
input_string_negative = fin.read()
fin.close()

positive_words = input_string_positive.split('\n')
negative_words = input_string_negative.split('\n')

con = MySQLdb.Connect(host="127.0.0.1", port=3306, user="root", passwd="password", db="Sentiments")
Cursor = con.cursor()

for word in positive_words:
	try:
		word = word.strip()
		if(len(word) > 0):
			sql = "INSERT INTO Polarity Values(%s,1,1)" 
			Cursor.execute(sql,word)
			con.commit()
			print "Done " , word
	except:
		con.rollback()
		print "Sorry " , word

for word in negative_words:
	try:
		word = word.strip()
		if(len(word) > 0):
			sql = "INSERT INTO Polarity Values(%s,-1,1)" 
			Cursor.execute(sql,word)
			con.commit()
			print "Done " , word
	except:
		con.rollback()
		print "Sorry " , word

con.close()
