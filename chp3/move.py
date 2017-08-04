#/home/caicai/scrapebole/chp3/data/img/date.jobbole.com
import os
import shutil
path = '/home/caicai/scrapebole/chp3/data/img/date.jobbole.com'
files = os.listdir(path)
for file in files:
    afile = path + '/' + file
    f = os.listdir(afile)
    if len(f)==2:
        ajpg = f[1]
        os.chdir(afile)
        shutil.copy(afile + '/'+ ajpg, path)