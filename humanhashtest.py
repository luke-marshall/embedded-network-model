import random
import string
import humanhash
from passlib.hash import sha256_crypt
import base64
random.seed(1000)
num_solar_participants =10
has_solar = []
counter = 0
for counter in range(num_solar_participants*2):
    if counter < num_solar_participants:
        has_solar.append(True)
    else:
        has_solar.append(False)
    counter += 1
# Jumble the list
random.shuffle(has_solar)
digest = string.join([str(chr(i+97)) if has_solar[i] else '0' for i in range(len(has_solar))],"")
digest = base64.b16encode(digest)
unique_id = humanhash.humanize(digest)

print( unique_id)