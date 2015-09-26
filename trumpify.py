#!/usr/bin/env python2.7

import nltk, gensim, pattern

def make_model():
	data = []
	errors = 0

	with open("speech3.txt", "r") as speech:
		for line in speech:
			try:
				sentences = nltk.sent_tokenize(line.encode("UTF-8"))
				for sentence in sentences:
					tokenized_sentence = nltk.word_tokenize(sentence)
					final = []
					for word in tokenized_sentence:
						if word not in nltk.corpus.stopwords.words("english"):
							final += [word]
					data += [final]

			except UnicodeDecodeError:
				errors += 1
				print(line)
	print(len(data))
	model = gensim.models.word2vec.Word2Vec(data, size=50)
	return model


def trumpify(input_sentence, model, verbose=False, pos_to_search_for=["NN", "JJ"]):
	final_output = ""

	for word, pos in pattern.en.tag(input_sentence):
		
		if pos[:2] in pos_to_search_for:
			try:
				sim = model.most_similar(positive=[word, "bad"])
				changed = False

				for top_word, cosin_sim in sim:
					new_word, new_pos = pattern.en.tag(top_word)[0]
					if pos[:2] in pos_to_search_for:
						if verbose == True:
							print "changed: ", word, top_word, pos
						final_output += new_word + " "
						changed = True
						break #this doesn't seem to work

				#if we make it to here, we must add the word to the string
				if changed == False: #needed to do this to get it to work if the word was not found in sim
					final_output += word + " "
			except KeyError:
				if verbose == True:
					print word, " not found in corpus"
				final_output += word + " "
		else:
			if verbose == True:
				print word, "not the proper pos", pos
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



