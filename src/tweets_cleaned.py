import re, sys, pdb

regex = re.compile('"((Sun|Mon|Tue|Thu|Wed|Fri|Sat) [A-Za-z0-9\s:\+]*)".*"text":"(.*)"')
input_filepath = sys.argv[1]
output_filepath = sys.argv[2]

clean_tweets = []
with open(input_filepath) as tweets:
	count = 0
	for raw_tweet in tweets:
		if "source" in raw_tweet:
			source_word_idx = raw_tweet.index(',"source"')
			trimmed_tweet = raw_tweet[0:source_word_idx]
			matches = regex.search(trimmed_tweet)

			if matches != None:
				timestamp = matches.group(1)
				content = str(matches.group(3))

				if "\\u" in content:
					count += 1
				content = content.replace("\\\\", "{doublebackz}") #could be done better
				unicode_removed_string = content.decode("unicode_escape").encode("ascii", "ignore")
				clean_tweet = re.sub(r"\\",'', unicode_removed_string)
				clean_tweet = clean_tweet.replace("{doublebackz}",'\\')
				clean_tweet = re.sub(r"\s",' ', clean_tweet)
				clean_tweets.append(clean_tweet+" (timestamp: "+timestamp+")")

with open(output_filepath, "w") as output:
	for tweet in clean_tweets:
		output.write(tweet.strip())
		output.write("\n")
	output.write("\n")
	output.write(str(count)+" tweets contained unicode.")
