
# see https://realpython.com/python-generate-qr-code/


# basic_qrcode.py

import segno

payload = "https://www.hpyc.org.uk/openday"
output = "openday"

qrcode = segno.make_qr(payload)
qrcode.save(output + ".png", scale=5,)
qrcode.save(output + "-red.png",  dark="darkred", scale=5,)
qrcode.save(output + "-blue.png",  dark="darkblue", scale=5,)