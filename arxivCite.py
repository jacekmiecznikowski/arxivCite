import csv, pprint, random, time, progressbar

def authorScore (contender, publication):
	if any(author in contender for author in publication):
		return random.random()
	else:
		return 0
def catScore (contender, publication):
	contenderCategories = contender.split(";")
	publicationCategories = publication.split(";")
	if any(category in contenderCategories for category in publicationCategories):
		return random.random()
	else:
		return 0
def lucky(percent=1):
	return random.randrange(100) < percent

def randomPublications(start, end, count):
	if count == 0:
	    return []
	else:
	    return random.sample(range(start, end), count)

def isOlder(contender, publication):
	contender = time.strptime(contender, "%Y-%m-%d")
	publication = time.strptime(publication, "%Y-%m-%d")
	return publication < contender

dict_list = []
pprint.pprint("Reading publications.csv")
reader = csv.DictReader(open('publications.csv', 'r'), delimiter=',', quotechar='"', escapechar='\\')
for line in reader:
    dict_list.append(line)

pprint.pprint("Done.")
pprint.pprint("Reading authors.csv")
with open("authors.csv") as f:
    next(f)
    for row in csv.reader(f, delimiter=',', quotechar='"', escapechar='\\'):
        num, first_name, last_name = row
        dict_list[int(num)].setdefault("author", []).append(last_name + ", " + first_name)
pprint.pprint("Done.")

pprint.pprint("Sorting publications by date");
dict_list.sort(key=lambda d: time.strptime(d['date'], "%Y-%m-%d"))
pprint.pprint("Done");


contenders_count = int(0.05 * len(dict_list))
quotations_min = 5
quotations_max = 100
index = 0;
writer=csv.writer(open('citations.csv', 'w'), delimiter=',', quotechar='"', escapechar='\\')
writer.writerow(("src", "dst"))

bar = progressbar.ProgressBar(maxvalue=len(dict_list), redirect_stdout=True)
for publication in dict_list:
	count = index if contenders_count > index else contenders_count
	contenders_ids = randomPublications(0, index, count)
	contenders = []
	for contender_id in contenders_ids:
		contenders.append({"id": dict_list[contender_id]["id"]})
	for contender in contenders:
		contenderScore = catScore(dict_list[int(contender["id"])]['categories'], publication['categories'])  + 2*authorScore(dict_list[int(contender["id"])]['author'], publication['author'])
		contender["score"] = contenderScore
	contenders.sort(key=lambda d: d['score'], reverse=True)
	ccount = len(contenders)
	quotations_max = 250 if lucky() else 100
	qmin = quotations_min if quotations_min < ccount else 0
	qmax = quotations_max if quotations_max < ccount else ccount
	qcount = random.randint(qmin,qmax)
	quotations = contenders[0:qcount]
	for quote in quotations:
		writer.writerow((publication['id'], quote['id']))
	index+=1
	bar.update(index)

bar.finish()
