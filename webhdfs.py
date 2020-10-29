import re
import json
import logging
import zlib
import requests
from http.client import HTTPConnection, IncompleteRead
from urllib.parse import urlparse
from pywebhdfs.webhdfs import PyWebHdfsClient
from hdfs import InsecureClient

logging.basicConfig(level=logging.DEBUG, datefmt='%m/%d/%Y %I:%M:%S %p',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='webhdfs')
WEBHDFS_CONTEXT_ROOT = "/webhdfs/v1/user/hadoopuser/"

MAGIC_BITS = 16
ZLIB_WBITS = MAGIC_BITS+zlib.MAX_WBITS

class _NameNodeHTTPClient():
    def __init__(self, http_method, url_path, namenode_host, namenode_port, hdfs_username, headers={}):
        url_path += '&user.name=' + hdfs_username
        self.httpclient = HTTPConnection(namenode_host, namenode_port, timeout=600)
        self.httpclient.request(http_method, url_path, headers=headers)

    def __enter__(self):
        response = self.httpclient.getresponse()
        logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
        return response

    def __exit__(self, type, value, traceback):
        self.httpclient.close()

class WebHDFS(object):
    """ Class for accessing HDFS via WebHDFS
        To enable WebHDFS in your Hadoop Installation add the following configuration
        to your hdfs_site.xml (requires Hadoop >0.20.205.0):
        <property>
             <name>dfs.webhdfs.enabled</name>
             <value>true</value>
        </property>
        see: https://issues.apache.org/jira/secure/attachment/12500090/WebHdfsAPI20111020.pdf
    """


    def __init__(self, namenode_host, namenode_port, hdfs_username):
        self.namenode_host = namenode_host
        self.namenode_port = namenode_port
        self.username = hdfs_username

    def parse_url(self, url):
        (scheme, netloc, path, params, query, frag) = urlparse(url)

        # Verify hostnames are valid and parse a port spec (if any)
        match = re.match('([a-zA-Z0-9\-\.]+):?([0-9]{2,5})?', netloc)

        if match:
            (host, port) = match.groups()
        else:
            raise Exception('Invalid host and/or port: %s' % netloc)

        return host, int(port), path.strip('/'), query

    def copyfromlocal(self, source_path, target_path, replication=1, overwrite=True):
        url_path = WEBHDFS_CONTEXT_ROOT + target_path + '?op=CREATE&overwrite=' + 'true' if overwrite else 'false'

        with _NameNodeHTTPClient('PUT', url_path, self.namenode_host, self.namenode_port, self.username) as response:
            logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
            redirect_location = response.msg["location"]
            logger.debug("HTTP Location: %s" % redirect_location)
            (redirect_host, redirect_port, redirect_path, query) = self.parse_url(redirect_location)

            # Bug in WebHDFS 0.20.205 => requires param otherwise a NullPointerException is thrown
            redirect_path = redirect_path + "?" + query + "&replication=" + str(replication)

            logger.debug("Redirect: host: %s, port: %s, path: %s " % (redirect_host, redirect_port, redirect_path))
            fileUploadClient = HTTPConnection(redirect_host, redirect_port, timeout=600)

            # This requires currently Python 2.6 or higher
            fileUploadClient.request('PUT', redirect_path, open(source_path, "r").read(), headers={})
            response = fileUploadClient.getresponse()
            logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
            fileUploadClient.close()
        return json.loads(response.read())

    def mkdir(self, path):
        url_path = WEBHDFS_CONTEXT_ROOT + path + '?op=MKDIRS'
        logger.debug("Create directory: " + url_path)
        with _NameNodeHTTPClient('PUT', url_path, self.namenode_host, self.namenode_port,
                                 self.username) as response:
            logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
            return json.loads(response.read())

    def listdir(self, path, wildcard=[]):  # add wildcard list to filter by dates
        url_path = WEBHDFS_CONTEXT_ROOT + path + '?op=LISTSTATUS'
        logger.debug("List directory: " + url_path)
        file_name = path.split('/')[-1:][0]
        with _NameNodeHTTPClient('GET', url_path, self.namenode_host, self.namenode_port, self.username) as response:
            logger.debug("HTTP Response: %d, %s" % (response.status, response.reason))
            data_dict = json.loads(response.read())
            logger.debug("Data: " + str(data_dict))

            files = []
            for i in data_dict["FileStatuses"]["FileStatus"]:
                if len(wildcard) > 0:
                    if [w for w in wildcard if w in i["pathSuffix"]]:
                        logger.debug(i["type"] + ": " + i["pathSuffix"])
                        files.append((i["pathSuffix"] or file_name, i["length"], i["type"]))
                else:
                    logger.debug(i["type"] + ": " + i["pathSuffix"])
                    files.append((i["pathSuffix"] or file_name, i["length"], i["type"]))

        return files



def upload_to_hdfs(ip,user):
    hadoop = InsecureClient(ip, user)
    hadoop.upload('','test.txt')


if __name__ == "__main__":
    #webhdfs = WebHDFS("218.146.20.50", 9870, "hadoopuser")
    #webhdfs.mkdir('testdirectory')
    #webhdfs.listdir('')
    #hdfs.create_file(my_file,my_data)

    upload_to_hdfs('http://218.146.20.50:9870', 'hadoopuser')
    #webhdfs.copyfromlocal('test.txt','testd/test.txt')




