import hdfs
from hdfs import InsecureClient


client = InsecureClient('http://218.146.20.50:9870', user='main')

with client.read('features') as reader:
    features = reader.read()