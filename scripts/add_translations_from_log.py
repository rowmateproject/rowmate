# run the webapp with "npm run dev 2>&1 | tee log.txt" to collect missing translation keys
import polib
import re
potpath = 'api/setup/translations/base.pot'
logfilepath = 'app/log.txt'
pofile = polib.pofile(potpath)
with open(logfilepath, 'r') as f:
    for line in f.readlines():
        if 'keypath' in line:
            key = re.search("(?<=').+(?=')", line).group(0)
            pofile.append(polib.POEntry(msgid=key))

pofile.save(potpath)
