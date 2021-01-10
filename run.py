import matplotlib.pyplot as plt
from matplotlib.image import BboxImage
from matplotlib.transforms import Bbox, TransformedBbox

import numpy as np
import math

import requests, os, time, sys
from bs4 import BeautifulSoup
import pandas as pd

def insta_info(account_name):
    html = requests.get('https://www.instagram.com/%s/'%(account_name)) 
    soup = BeautifulSoup(html.text, "html.parser")
    data = soup.find_all('meta', attrs={'property':'og:description'})
    print(data)
    text = data[0].get('content').split()
    user = '%s %s %s' % (text[-3], text[-2], text[-1])
    followers = text[0]
    if followers[-1] == 'k':
        followers = int(float(followers[:-1].encode('UTF-8')) * 1000)
    elif len(followers)>3:
        followers = int(float((followers[:-4]+followers[-3:]).encode('UTF-8')))
    else:
        followers = int(float(followers.encode('UTF-8')))
    following = text[2]
    if following[-1] == 'k':
        following = int(float(following[:-1].encode('UTF-8')) * 1000)
    elif len(following)>3:
        following = int(float((following[:-4]+following[-3:]).encode('UTF-8')))
    else:
        following = int(float(following.encode('UTF-8')))
    return followers,following

def plotImage(xData, yData, im):
    for x, y in zip(xData, yData):
        bb = Bbox.from_bounds(x,y,1,1)  
        bb2 = TransformedBbox(bb,ax.transData)
        bbox_image = BboxImage(bb2,
                            norm = None,
                            origin=None,
                            clip_on=False)

        bbox_image.set_data(im)
        ax.add_artist(bbox_image)

head = plt.imread("head.png")

fl,f=insta_info("ImyDoesMed")

x_=[.6*n for n in range(round(fl/(math.ceil(np.sqrt(fl)))+1))]
y_=[.7*n for n in range(0,(math.ceil(np.sqrt(fl))+1))]
c=0
n,m=0,len(y_)-1
x=[]
y=[]
while c<fl:
    if n==len(x_):
        n=0
        m-=1
    o=0.3 if m%2!=0 else 0
    x.append(x_[n]+o)
    y.append(y_[m])
    n+=1
    c+=1
dpi=300
fig = plt.figure(figsize=(max(x_)*112/dpi, max(y_)*69/dpi), dpi=dpi)
ax = fig.add_subplot(111)
plotImage(x,y,head)
fs=12
ax.text(0, 0, "Followers:%s"%fl, fontsize=fs,backgroundcolor="black",color="white")
ax.axis('off')
ax.set_xlim(0,max(x_))
ax.set_ylim(0,max(y_))

plt.savefig("out.png")