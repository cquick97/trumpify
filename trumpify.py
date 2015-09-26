#!/usr/bin/env python2.7

import nltk, gensim, pattern

def make_model():
	data = []
	errors = 0

	punctuation = """!@#$%^&*(){}[]:;"',.<>/?"""

	with open("speech3.txt", "r") as speech:
		for line in speech:
			try:
				sentences = nltk.sent_tokenize(line.encode("UTF-8"))
				for sentence in sentences:
					tokenized_sentence = nltk.word_tokenize(sentence)
					edited_sentence = []
					for word in tokenized_sentence:
						if word not in nltk.corpus.stopwords.words("english") and word not in punctuation:
							edited_sentence += [pattern.en.singularize(word)]
					data += [edited_sentence]

			except UnicodeDecodeError:
				errors += 1
				print(line)
	print(len(data))
	model = gensim.models.word2vec.Word2Vec(data, size=50)
	return model


def trumpify(input_sentence, model, verbose=False, pos_to_search_for=["NN", "JJ"]):
	final_output = ""

	punctuation = """!@#$%^&*(){}[]:;"',.<>/?"""

	hard_coded_dict = {"women": "terrorists", "mexican" : "illegal", "mexicans": "illegals", "china": "the enemy", 
					"obama": "a muslim", "bible": "Art of the Deal", "book": "bible",
					"favorite": "own", "hawaii": "kenya"}

	for word, pos in pattern.en.tag(input_sentence):
		if verbose == True:
			print word

		singular_form = pattern.en.singularize(word.lower())
		singular = singular_form == word

		if word.lower() in hard_coded_dict:
			final_output += hard_coded_dict[word.lower()] + " "
		
		elif pos[:2] in pos_to_search_for:
			try:
				sim = model.most_similar(positive=[singular_form])
				changed = False

				for top_word, cosin_sim in sim:
					new_word, new_pos = pattern.en.tag(top_word)[0]
					if new_pos == pos:
						if verbose == True:
							print "changed: ", word, top_word, pos
						if singular == True:
							final_output += new_word + " "
						else: #needs to be pluralized
							final_output += pattern.en.pluralize(new_word, pos=pos) + " "
						changed = True
						break #this doesn't seem to work

				#if we make it to here, we must add the word to the string
				if changed == False: #needed to do this to get it to work if the word was not found in sim
					final_output += word + " "
			except KeyError: #if it is not in the model, then go here
				if verbose == True:
					print word, " not found in corpus"
				if word not in punctuation:
					final_output += word + " "
				elif "'" in word:
					final_output = final_output[:-1]
					final_output += word + " "
				else:
					final_output = final_output[:-1]
					final_output += word + " "
		else:
			if verbose == True:
				print word, "not the proper pos", pos

			if "'" in word:
				final_output = final_output[:-1]
				final_output += word + " "
			elif word not in punctuation:
				final_output += word + " "
			else:
				final_output = final_output[:-1]
				final_output += word + " "
	if verbose == True:
		print "input: ", input_sentence
		print "output: ", final_output
	return final_output

if __name__ == '__main__':
	model = make_model()
	while True:
		trumpify(str(raw_input("Input a sentence: ")), model, verbose=True)



#print errors, data



