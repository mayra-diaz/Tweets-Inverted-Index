from Util import Util
import os, glob
import shutil
import json
import csv
import linecache
import atexit

class InvertedIndex():

  """
  ----------- CONSTRUCTOR - DESTRUCTOR -----------
  """
  def __init__(self):
    self.BLOCK_SIZE = 100
    self.util = Util()
    self.index_blocks_directory = './index_blocks/'
    self.temp_directory = './temp/'

    self.id_document_file = './data/id_documents.csv'
    self.metadata_file = './data/metadata.json'

    self.base_document_name = './tweets/tweets_data_'
    self.base_block_name = self.index_blocks_directory + 'block_'

    self.metadata = {}
    self.current_index = {}
    
    self.read_metadata()
    self.create_id_document_file()
    atexit.register(self.cleanup)

  def cleanup(self):
      self.write_metadata()

  """
  ----------- METADATA -----------
  """
  def read_metadata(self):
    if os.path.exists('./'+self.metadata_file):
      with open(self.metadata_file, 'r') as file:
        self.metadata = json.load(file)
    else:
      f = open(self.metadata_file, 'x')
      f.close()
      self.metadata = {'number_of_tweets': 0, 'number_of_documents': 0, 'number_of_blocks': 0}

  def write_metadata(self):
    with open(self.metadata_file, 'w') as file:
      file.write(json.dumps(self.metadata))

  """
  ----------- BASIC -----------
  """
  def get_number_of_tweets(self):
    return self.metadata['number_of_tweets']
  
  def get_number_of_documents(self):
    return self.metadata['number_of_documents']

  def get_number_of_blocks(self):
    return self.metadata['number_of_blocks']
  
  def clear_current_index(self):
    self.current_index = {}

  """
  ----------- TWEETS AND DOCUMENTS -----------
  """
  def create_id_document_file(self):
    if not os.path.exists('./'+self.id_document_file):
      f = open(self.id_document_file, 'x')
      f.close()
      return False

  def write_id_document(self, tweet_id, document_name):
    with open(self.id_document_file, 'a') as file:
      file.write(f'{tweet_id},{document_name}\n')

  def get_tweet_file(self, position):
    info = linecache.getline(self.id_document_file, position).split(',')
    return info[0], info[1]

  def bs_tweet_file(self, id):
    low = 0
    high = self.get_number_of_tweets()
    while low <= high:
      mid = (high + low) // 2
      mid_id, document_name = self.get_tweet_file(mid)
      if mid_id == id:
        return mid
      elif mid_id < id:
        low = mid + 1
      else:
        high = mid - 1
    return mid

  def get_tweets(self, ids):
    documents = dict()
    for id in ids:
      position = self.bs_tweet_file(id)
      id, file = self.get_tweet_file(position)
      if not file in documents:
        documents[file] = [id]
      else:
        documents[file].append(position)
    
    tweets = []
    for file, ids in documents.items():
       with open(file) as tweets_file:
        json = json.load(tweets_file)
        for id in ids:
          tweets.append(json(id))
    return tweets

  def add_tweets(self, tweets, file_name):
    current = []
    with open(self.id_document_file, 'r') as docs:
      current = []
      for i in docs:
          current.append(i.split(','))
          current[-1][1] = current[-1][1][:-1]
      i = 1
      for id in tweets:
        current.insert(self.bs_tweet_file(id)+1, [str(id),file_name])
        i += 1
    with open(self.id_document_file, 'w') as docs:
      write = csv.writer(docs)
      write.writerows(current)

  """
  ----------- SCORING -----------
  """
  def setAllWeights(self):
    for token in self.current_index:
      for doc in token['docs']:
        self.current_index[token]['docs'][doc]['w'] = self.weight_td_idf(token, doc)

  def weight_td_idf(self, token, doc):
    return self.util.weight_td_idf(self.current_index[token]['docs'][doc], self.current_index[token]['df'], self.get_number_of_tweets())


  """
  ----------- ADD DOCUMENTS -----------
  """
  def clean_file(self, file_name, final_file_name):
    tweets = dict()
    result = dict()
    with open(file_name) as tweets_file:
      json_file = json.load(tweets_file)
      for tweet in json_file:
        final_tweet = dict()
        final_tweet["user_name"] = tweet["user_name"]
        final_tweet["body"] = tweet["text"]
        final_tweet["date"] = tweet["date"]
        result[tweet["id"]] = final_tweet
        tweets.append(tweet['id'])
    with open("clean_tweets/"+final_file_name, 'w') as file:
      file.write(json.dumps(result))
    self.add_tweets(tweets, final_file_name)
    return result
  
  def add(self, document_files):
    if isinstance(document_files, str):
      dir = document_files
      document_files = []
      for filepath in glob.iglob(dir+'*'):
        document_files.append(filepath)

    self.current_index = {}
    self.move_to_temp(document_files)
    self.metadata['number_of_documents'] += 1
    for filepath in glob.iglob(self.temp_directory+'*'):
      self.add_document(filepath)
    self.verify_current_index()
    self.util.clear_dir(self.temp_directory)
    self.merge_index_blocks()

  def move_to_temp(self, document_files):
    for i in range(len(document_files)):
      name = str(i)+'.json'
      starts_at = 0
      temp = document_files[i].find('/')
      while temp != -1:
        starts_at = temp
        temp = document_files[i].find('/')
      os.rename(document_files[i], document_files[i][:starts_at+1]+name)
      shutil.move(document_files[i][:starts_at+1]+name,self.temp_directory+name)

  """
  ----------- BSI -----------
  """
  def add_document(self, document_file_name):
    tweets = self.clean_file(document_file_name, self.base_doc_name+str(self.get_number_of_documents()))
    self.get_number_of_documents += 1
    for id, tweet in tweets.items():
      tokens = self.util.pre_process(tweet['body'])
      self.add_tweet_tokens(id, tokens)

  def add_tweet_tokens(self, tweet_id, tokens):
    for token in tokens:
      if len(self.current_index) == self.BLOCK_SIZE:
        self.write_block()
        self.clear_current_index()
      if token in self.current_index:
        self.current_index[token]['tf'] += 1
        if tweet_id in self.current_index[token]['tweets']:
          self.current_index[token]['tweets'][tweet_id] += 1
        else:
          self.current_index[token]['tweets'][tweet_id] = 1
          self.current_index[token]['df'] += 1
      else:
        self.current_index[token] = {'tf': 1, 'tweets': {tweet_id: 1}, 'df': 1}

  def verify_current_index(self):
    if len(self.current_index) > 0:
      self.write_block
    self.clear_current_index()

  def write_block(self, start=0, end=-1):
    if end == -1:
      end = len(self.current_index)
    file = open(self.base_block_name+str(self.get_number_of_blocks())+'.json', 'x')
    self.metadata['number_of_blocks'] += 1
    file.write(json.dumps(self.current_index[start:end]))
    file.close()

  def merge_index_blocks(self):
    for filepath in glob.iglob(self.index_blocks_directory+'*'):
      with open(filepath, 'r') as file:
        temp = json.load(file)
        self.current_index.update(temp)
    self.util.clear_dir(self.index_blocks_directory)
    self.current_index = dict(sorted(self.current_index.items(), key=lambda x: x[0], reverse=False))
    start = 0
    end = self.BLOCK_SIZE
    self.metadata['number_of_blocks'] = 0
    while end <= len(self.current_index):
      self.write_block(start, end)
      start += self.BLOCK_SIZE
      end += self.BLOCK_SIZE
    if start < len(self.current_index):
      self.write_block(start)
    self.clear_current_index()


  """
  ----------- HANDLER NEEDS -----------
  """

  def get_token_df(self, token):
    return self.self.current_index[token]['df']

  def get_index_interseccion_with_query():
    pass