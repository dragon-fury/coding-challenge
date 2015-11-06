import unittest, os
from average_degree import AverageDegree
from tweets_cleaned import CleanTweet

class TestCase(unittest.TestCase):
	def setUp(self):
		self.clean_tweet = CleanTweet()
		self.avg_deg = AverageDegree()
		self.base_dir = "/home/sesha/Interests/insightDataFella/coding-challenge/"

	def test_if_unicode_removed(self):
		tweet = "Spark \u009FSummit East this week! #Spark #Apache"
		clean_tweet = "Spark Summit East this week! #Spark #Apache"
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_if_unicode_spared(self):
		# Spare unicode between 0000 and 007F
		tweet = "Spark \u003cSummit East this week! #Spark #Apache"
		clean_tweet = "Spark <Summit East this week! #Spark #Apache"
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_if_double_backslash_handled(self):
		tweet = "This concert \\\\m/. Am enjoying!!"
		clean_tweet = "This concert \\m/. Am enjoying!!"
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_if_escape_url_handled(self):
		tweet = "PB https:\/\/t.co\/HOl34REL1a hello"
		clean_tweet = "PB https://t.co/HOl34REL1a hello"
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_if_escape_sequences_handled(self):
		tweet = "Should \n\nclean\t\rall of \"this\""
		clean_tweet = 'Should   clean  all of "this"'
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_if_empty(self):
		tweet = "\u3084\u3070\u3044\u7709\u6d88\u3048\u305f\uff01\u30d6\u30ea\u30fc\u30c1\u6642\u9593\u30df\u30b9\u3063\u305f\u308f\u2026"
		clean_tweet = ""
		self.failUnlessEqual(clean_tweet, self.clean_tweet.get_clean_tweet(tweet))

	def test_unicode_tweet_count(self):
		# Should have mocked. But did not.
		cleaned_tweet_list = ["Spark Summit East this week! #Spark #Apache (timestamp: Thu Oct 29 17:51:01 +0000 2015)", "Just saw a great post on Insight Data Engineering #Apache #Hadoop #Storm (timestamp: Thu Oct 29 17:51:30 +0000 2015)", "Doing great work #Apache (timestamp: Thu Oct 29 17:51:55 +0000 2015)", "Excellent post on #Flink and #Spark (timestamp: Thu Oct 29 17:51:56 +0000 2015)", "New and improved #HBase connector for #Spark (timestamp: Thu Oct 29 17:51:59 +0000 2015)", "New 2.7.1 version update for #Hadoop #Apache (timestamp: Thu Oct 29 17:52:05 +0000 2015)"]
		self.clean_tweet = CleanTweet(self.base_dir+"tweet_input/sample_tweets.txt", self.base_dir+"tweet_output/test_output.txt")
		cleaned_tweets = self.clean_tweet.process_tweets()
		self.failUnlessEqual(set(cleaned_tweet_list), set(cleaned_tweets))
		self.failUnlessEqual(4, self.clean_tweet.get_count_of_unicode_tweets())

	def test_average_degree_changes(self):
		self.avg_deg = AverageDegree(self.base_dir+"tweet_input/half_sample_tweets.txt", self.base_dir+"tweet_output/test_output.txt")
		self.avg_deg.process_tweets()
		self.failUnlessEqual(2.0, self.avg_deg.calculate_avg_degree())
		self.avg_deg = AverageDegree(self.base_dir+"tweet_input/sample_tweets.txt", self.base_dir+"tweet_output/test_output.txt")
		self.avg_deg.process_tweets()
		self.failUnlessEqual(1.67, self.avg_deg.calculate_avg_degree())

	def tearDown(self):
		self.clean_tweet = CleanTweet()
		self.avg_deg = AverageDegree()

if __name__ == '__main__':
    unittest.main()