from parsivar import FindStems
import pickle
import re
stopwords = [
"و",
"از",
"در",
"برای",
"چون"
]

DEBUG_MODE = False
my_stemmer = FindStems()

postlist = {}
with open('InformationRetrieval/objs.pkl', 'rb') as f:
    postlist = pickle.load(f)


def search_term(term):  # returns list
#     if term in STOP_WORDS:
#         term = "$$$"
    if term in postlist.keys():
        return postlist[term].keys()
    else:
        return False


def search_phrase(phrase):  # phrase is a list of words .  returns set
    print("im in")
    print(phrase)
    answers = []
    for word in phrase:
        if word not in postlist.keys():
            return False

    # for i in len(phrase):
        # if phrase[i] in STOP_WORDS:
        #     phrase[i] = "$$$"

    word_doc_list = [set(postlist[word].keys()) for word in phrase]

    alldocs = word_doc_list[0]
    # print(alldocs)
    for se in word_doc_list:
        alldocs.intersection_update(se)
    # print(alldocs)
    # now alldocs is set of documents which contain all words in the given phrase
    if alldocs:
        for doc in alldocs:
            pointers = [0] * len(phrase)
            possible_docs = [postlist[word][doc] for word in phrase]
            # print(doc,possible_docs)
            while pointers[0] < len(possible_docs[0]):
                for p in range(1, len(phrase)):
                    # print("fff")
                    # print(pointers[p])
                    while (pointers[p] < len(possible_docs[p])) and (
                            possible_docs[p][pointers[p]] < possible_docs[0][pointers[0]] + p):
                        pointers[p] += 1
                    if pointers[p] == len(possible_docs[p]):
                        break
                    if possible_docs[p][pointers[p]] > possible_docs[0][pointers[0]] + p:
                        break
                else:
                    # answers.append((doc, possible_docs[p][pointers[p]]))  # doc id and position of phrase
                    answers.append(doc)  # doc id and position of phrase
                    # print("found:", doc, possible_docs[p][pointers[p]])
                pointers[0] += 1

        # print(answers)
        return answers
    else:
        return False


class Query():
    def __init__(self, query):
        self.query = query

        # find NOT phrases !"abc xyz" and remove them
        self.neg_phrases = re.findall('!\"(.*?)\"', self.query)
        for nph in self.neg_phrases:
            self.query = self.query.replace('!\"' + nph + '\"', "")

        # find phrases "abc xyz" and remove them
        self.phrases = re.findall('\"(.*?)\"', self.query)
        for ph in self.phrases:
            self.query = self.query.replace('\"' + ph + '\"', "")

        # find NOT terms !abc and remove them
        self.negations = re.findall('\B!\w+', self.query)
        for ng in self.negations:
            self.query = self.query.replace(ng, "")
            # print(ng)

        self.terms = self.query.split()

        if DEBUG_MODE:
            print(query)
            print("results of parsing")
            print(self.neg_phrases)
            print(self.phrases)
            print(self.negations)
            print(self.terms)

        self.terms = [my_stemmer.convert_to_stem(x) for x in self.terms]

        self.phrases_stemmed = []
        for p in self.phrases:
            ps = []
            for i in p.split():
                ps.append(my_stemmer.convert_to_stem(i))
            self.phrases_stemmed.append(ps)
        self.phrases = self.phrases_stemmed

        self.neg_phrases_stemmed = []
        for np in self.neg_phrases:
            nps = []
            for i in np.split():
                nps.append(my_stemmer.convert_to_stem(i))
            self.neg_phrases_stemmed.append(nps)
        self.neg_phrases = self.neg_phrases_stemmed

        # stem words in negations and remove the '!'
        self.negations = [my_stemmer.convert_to_stem(word[1:]) for word in self.negations]
        if DEBUG_MODE:
            print("results of stemming")
            print(self.neg_phrases)
            print(self.phrases)
            print(self.negations)
            print(self.terms)

    def final_results(self):
        # print(self.neg_phrases)
        # universal set
        _f = set([i for i in range(1, 2000)])

        t_results = []
        for t in self.terms:
            st = search_term(t)
            if st:
                t_results.append(set(st))

        p_results = []
        for p in self.phrases:
            sp = search_phrase(p)
            if sp:
                p_results.append(set(sp))

        # nothing found
        if (not t_results) and (not p_results):
            return []

        np_results = []
        for np in self.neg_phrases:
            sp = search_phrase(np)
            if sp:
                np_results.append(set(sp))

        n_results = []
        for n in self.negations:
            st = search_term(n)
            if st:
                n_results.append(set(st))

        for x in t_results:
            _f.intersection_update(x)
        for x in p_results:
            _f.intersection_update(x)
        for n in n_results:
            _f.difference_update(n)
        for n in np_results:
            _f.difference_update(n)

        print(f"Final Resault:{_f}")
        # return [1]

        return list([x-2 for x in _f])


if __name__ == "__main__":
    print(my_stemmer.convert_to_stem("است"))
    input_str = input("query:")
    q1 = Query(input_str)
    q1.final_results()
    # print(search_term(my_stemmer.convert_to_stem(input_str)))
