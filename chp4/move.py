import shutil
import os
path = '/home/caicai/scrapebole/chp4/data/img/date.jobbole.com'
dirpath = '/home/caicai/scrapebole/chp4/data/img'
files = os.listdir(path)
for file in files:
    afile = path + '/' + file
    f = os.listdir(afile)
    if len(f)==2:
        ajpg = f[1]
        os.chdir(afile)
        shutil.copy(afile + '/'+ ajpg, dirpath)