from apyori import apriori

transactions = [
    ['beer', 'nuts'],
    ['beer', 'cheese'],
]
results = list(apriori(transactions))
for obj in results:
	print obj
