import re, sys, datetime
from tweets_cleaned import CleanTweet

class AverageDegree(object):
	def __init__(self, inputfile="dummyInput", outputfile="dummyOutput"):
		self.regex = re.compile('"((Sun|Mon|Tue|Thu|Wed|Fri|Sat) [A-Za-z0-9\s:\+]*)".*"text":"(.*)"')
		self.hashtag_regex = re.compile("#(\w+)")
		self.format_string = "%a %b %d %H:%M:%S +0000 %Y"
		self.time_key = {}
		self.adjacency_list = {}
		self.input_filepath = inputfile
		self.output_filepath = outputfile
		self.clean_tweet_object = CleanTweet()

	def remove_older_hashtags(self, timestamp):
		one_minute = datetime.timedelta(minutes=1)
		current_time = datetime.datetime.strptime(timestamp, self.format_string)
		timestamps = self.time_key.keys()
		ts_to_remove = filter(lambda old_ts: (current_time - datetime.datetime.strptime(old_ts, self.format_string)) > one_minute, timestamps)
		hashtags = []
		for ts in ts_to_remove:
			hashtags += self.time_key.pop(ts)
		unique_hashtags = set(hashtags)
		for hashtag in unique_hashtags:
			self.adjacency_list[hashtag] -= unique_hashtags

	def add_nodes(self, tweet, timestamp):
		raw_hashtags = self.hashtag_regex.findall(tweet)
		hashtags = map(lambda tag: tag.lower().strip(), raw_hashtags)

		self.remove_older_hashtags(timestamp)
		if timestamp not in self.time_key:
			self.time_key[timestamp] = []

		unique_hashtags = set(hashtags)

		if len(unique_hashtags) > 1:
			self.time_key[timestamp] += list(unique_hashtags)
			temp_hashtags = unique_hashtags.copy()
			for hashtag in unique_hashtags:
				if hashtag not in self.adjacency_list:
					self.adjacency_list[hashtag] = set([])
				temp_hashtags.remove(hashtag)
				self.adjacency_list[hashtag].update(temp_hashtags)
				temp_hashtags.add(hashtag)


	def calculate_avg_degree(self):
		avg_degree = 0
		no_of_nodes = len(self.adjacency_list.keys())
		if no_of_nodes != 0:
			for links in self.adjacency_list.values():
				avg_degree += len(links)

			avg_degree = round(avg_degree*1./no_of_nodes, 2)
		return avg_degree

	def process_tweets(self):
		output = open(self.output_filepath, "a+")

		with open(self.input_filepath) as tweets:
			for raw_tweet in tweets:
				if "source" in raw_tweet:
					source_word_idx = raw_tweet.index(',"source"')
					trimmed_tweet = raw_tweet[0:source_word_idx]
					matches = self.regex.search(trimmed_tweet)

					if matches != None:
						timestamp = matches.group(1)
						content = str(matches.group(3))

						clean_tweet = self.clean_tweet_object.get_clean_tweet(content)
						self.add_nodes(clean_tweet, timestamp)

				output.write(str(self.calculate_avg_degree()))
				output.write("\n")
		output.close()

if __name__ == "__main__":
	avg_degree = AverageDegree(sys.argv[1], sys.argv[2])
	avg_degree.process_tweets()