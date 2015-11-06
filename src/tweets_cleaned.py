import re, sys

class CleanTweet(object):
	def __init__(self, inputfile="dummyInput", outputfile="dummyOutput"):
		self.regex = re.compile('"((Sun|Mon|Tue|Thu|Wed|Fri|Sat) [A-Za-z0-9\s:\+]*)".*"text":"(.*)"')
		self.input_filepath = inputfile
		self.output_filepath = outputfile
		self.count = 0

	def get_clean_tweet(self, raw_tweet):
		content = raw_tweet.replace("\\\\", "{doublebackz}") #could be done better
		unicode_removed_string = content.decode("unicode_escape").encode("ascii", "ignore")
		clean_tweet = re.sub(r"\\",'', unicode_removed_string)
		clean_tweet = clean_tweet.replace("{doublebackz}",'\\')
		return re.sub(r"\s",' ', clean_tweet)

	def process_tweets(self):
		clean_tweets = []
		with open(self.input_filepath, "r+") as tweets:
			for raw_tweet in tweets:
				if "source" in raw_tweet:
					source_word_idx = raw_tweet.index(',"source"')
					trimmed_tweet = raw_tweet[0:source_word_idx]
					matches = self.regex.search(trimmed_tweet)

					if matches != None:
						timestamp = matches.group(1)
						content = str(matches.group(3))

						if "\\u" in content:
							self.count += 1

						clean_tweet = self.get_clean_tweet(content)
						clean_tweets.append(clean_tweet+" (timestamp: "+timestamp+")")
		return clean_tweets

	def write_tweets(self, clean_tweets):
		with open(self.output_filepath, "w+") as output:
			for tweet in clean_tweets:
				output.write(tweet.strip())
				output.write("\n")
			output.write("\n")
			output.write(str(self.count)+" tweets contained unicode.")

	def get_count_of_unicode_tweets(self):
		return self.count

if __name__ == "__main__":
	clean_tweet = CleanTweet(sys.argv[1], sys.argv[2])
	clean_tweets = clean_tweet.process_tweets()
	clean_tweet.write_tweets(clean_tweets)