import tweepy
import random
import operator

consumer_key = 'XxX'
consumer_secret = 'XxX'

access_token = 'XxX'
access_token_secret = 'XxX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


# tweets_list = []
#
# results = api.search(q='nba', lang='en',count=100)
# print(len(results))
#
# for result in results:
#     tweets_list += [result.text]
#
# print(len(tweets_list))

query_word = 'Celtics'

max_tweets = 2000
searched_tweets = []
last_id = -1
while len(searched_tweets) < max_tweets:
    count = max_tweets - len(searched_tweets)
    try:
        new_tweets = api.search(q=query_word, count=count, max_id=str(last_id - 1))
        if not new_tweets:
            break
        searched_tweets.extend(new_tweets)
        last_id = new_tweets[-1].id
    except tweepy.TweepError as e:
        # depending on TweepError.code, one may want to retry or wait
        # to keep things simple, we will give up on an error
        break

tweets_list = []
for result in searched_tweets:
    str = result.text
    if str not in tweets_list:
        tweets_list += [str]

print(len(tweets_list))

list_to_pop = []
for i in range (len(tweets_list)-1, -1, -1):
    tweets_list[i] = tweets_list[i].split(' ')
    if tweets_list[i][0]=='RT':
        list_to_pop += [i]

for i in list_to_pop:
    tweets_list.pop(i)

tweet_for_first_word = random.randint(0,4)
#tweet = [tweets_list[tweet_for_first_word][0]]

fw_dict = {}
for i in range (len(tweets_list)):
    if tweets_list[i][0] not in fw_dict:
        fw_dict[tweets_list[i][0]] = 1
    else :
        fw_dict[tweets_list[i][0]] += 1
fw_dict_sorted = sorted(fw_dict, key=fw_dict.get, reverse=True)[:5]
tweet = [fw_dict_sorted[tweet_for_first_word]]
tweet_markov_2 = [fw_dict_sorted[tweet_for_first_word]]
print(tweet)

added_word = ''
word_number = 0
tweet_length = len(fw_dict_sorted[tweet_for_first_word])
while added_word!='white_space' and (tweet_length+len(query_word)+1)<140:
    dict = {}
    dict_2 = {}
    for i in range(len(tweets_list)):
        if tweet_markov_2[word_number] in tweets_list[i]:
            index = tweets_list[i].index(tweet_markov_2[word_number])
            if tweets_list[i][index-1]==tweet_markov_2[word_number-1]:
                print(tweets_list[i])
                if index == len(tweets_list[i]) - 1:
                    if 'white_space' not in dict_2:
                        dict_2['white_space'] = 1
                    else:
                        dict_2['white_space'] += 1
                else:
                    word = tweets_list[i][index + 1]
                    if word not in dict_2:
                        dict_2[word] = 1
                    else:
                        dict_2[word] += 1
            #print(tweets_list[i])
            #print(tweet[word_number])
            #print('index index', index)
            #print(len(tweets_list[i]))
            if index == len(tweets_list[i])-1:
                if 'white_space' not in dict:
                    dict['white_space'] = 1
                else:zc
                    dict['white_space'] += 1
            else:
                word = tweets_list[i][index+1]
                if word not in dict:
                    dict[word] = 1
                else:
                    dict[word] += 1
    print('dict-2 : ', dict_2)

#    print(dict)
    added_word = max(dict, key=dict.get)
    while added_word in tweet and len(dict)!=1:
        dict.pop(added_word)
        added_word = max(dict, key=dict.get)

    tweet_length += len(added_word)
    tweet_length += 1
#    print(added_word)
    if (tweet_length+len(query_word)+len(added_word)+1)<140:
        tweet += [added_word]
        word_number += 1
        if len(dict_2) != 0:
            added_word_2 = max(dict_2, key=dict_2.get)
        else:
            added_word_2 = max(dict, key=dict.get)
        tweet_markov_2 += [added_word_2]

    print(tweet_markov_2)

print(tweet)

if tweet[-1] == 'white_space':
    tweet.pop(len(tweet)-1)

tweet_str = ''

for word in tweet_markov_2:
    tweet_str += word
    tweet_str += ' '

tweet_str += '#'
tweet_str += query_word
print(tweet_str)
#api.update_status(status=tweet_str)

print('alternative tweet : ', tweet_markov_2, '!')