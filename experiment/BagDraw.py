import bagpy
from bagpy import bagreader
import os


b = bagreader('/home/nurlando/experiment/31_allvibro.bag')



print(b.topic_table)

csvfiles = []
for t in b.topics:
    data = b.message_by_topic(t)
    print(type(data))
    print(data)
    csvfiles.append(data)

