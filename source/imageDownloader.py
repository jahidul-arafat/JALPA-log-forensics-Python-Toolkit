from __future__ import division
import os
import re
import sys
import urllib

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

def url_sort_key(url):
    patternImageName=r'-(\w+)-(\w+)\.\w+' #to match 'a-baaa.jpg'
    match=re.search(patternImageName,url)
    if match:
        return match.group(2) #baaa
    else:
        return url


def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  #filename="animal_code.google.com"
  #here, hostName=code.google.com
  # +++your code here+++
  #Step-1: extract the hostName from the filename
  underbar=filename.index("_")
  hostName=filename[underbar+1:]#code.google.com

  #Step-2: open the file and read all its lines and store in a list
  f=open(filename)
  allLines=f.readlines()
  f.close()

  #Step-3:
  #example: line 1, this doesnt contain our desired puzzle image
  '''
  10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /baz/css/fish.css HTTP/1.1"
  302 5694 "-" "googlebot-mscrawl-moma (enterprise; bar-XYZ;
  foo123@google.com,foo123@google.com,foo123@google.com,foo123@google.com)"
  '''

  #example: line 2 which contains our desired puzzle image
  '''
    10.254.254.138 - - [06/Aug/2007:00:09:49 -0700]
    "GET /edu/languages/google-python-class/images/puzzle/a-baag.jpg HTTP/1.0" 302 3940
    "-" "googlebot-mscrawl-moma"
  '''
  #Create a url dictionary to keep all the valid urls with a Value=1
  url_dict={}
  patternPuzzleUrl=r'"GET (\S+)'
  for line in allLines:
    match=re.search(patternPuzzleUrl,line)
    if match:
        obtainedPath=match.group(1) #/edu/languages/google-python-class/images/puzzle/a-baag.jpg
        if "puzzle" in obtainedPath:
            #store it in the following format
            #{'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaa.jpg': 1}
            url_dict["http://"+hostName+obtainedPath]=1

  #if you want to see url_dict.keys() you may find a list not sorted like below:
  '''
    ['http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baag.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babc.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baae.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baba.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babg.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaj.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baab.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babi.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaf.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baad.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babe.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baah.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babb.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babh.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baai.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babj.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babf.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-babd.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baac.jpg',
 'http://code.google.com/edu/languages/google-python-class/images/puzzle/a-baaa.jpg']
  '''
  #So, you need to sort it using the words [a-babc.jpg,a-baae.jpg,...,a-baaa.jpg]
  #So, create a key for sorted() function
  return sorted(url_dict.keys(),key=url_sort_key)

def download_images(img_urlListFromReadUrlFunc, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  # +++your code here+++
  #If the destination directory does not exists, create it
  #if not os.path.exists(dest_dir):
        #os.makedirs(dest_dir)
  #Create an index.html in the directory
  index=file(os.path.join(dest_dir,"index.html"),'w')
  index.write("<html><body>\n")
  imgCounter=0
  for img_url in img_urlListFromReadUrlFunc:
    localimgName="img%d"%imgCounter
    print "Retreiving...", img_url
    urllib.urlretrieve(img_url,os.path.join(dest_dir,localimgName))
    #urllib.urlretrieve(onlineSourceFromWhereToDownload,destinationWhereToStoreAfterDownloading)
    index.write('<img src="%s">'%localimgName)
    imgCounter+=1
  index.write("\n</body></html>\n")
  index.close()

def numberOfImageFileRetrieved(dirName):
    path, dirs, files = next(os.walk(dirName))
    #print len(files)-1
    return len(files)-1

def main():
    pass

if __name__ == '__main__':
  main()