
# see https://realpython.com/python-generate-qr-code/


# basic_qrcode.py

import segno

#payload = "https://sailing.myclub.run"
#output = "myclub"

payload = "https://hpyc.org.uk/openday"
output = "opendat"

qrcode = segno.make_qr(payload)
qrcode.save(output + ".png", scale=5,)
qrcode.save(output + "-red.png",  dark="darkred", scale=5,)
qrcode.save(output + "-blue.png",  dark="darkblue", scale=5,)
qrcode.save(output + "-purple.png",  dark="#9724DB", light="#aaaaaa", scale=5,)
qrcode.save(output + "-black.png",  dark="#000000", scale=5,)

#qrcode.save(output + "-alternatee.png",  dark="#3C24DB", light="#aaaaaa", scale=5,)

