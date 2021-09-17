import requests
try:
    input = raw_input
except NameError:
    pass

# Global values
base = "http://crypto.praetorian.com/{}"
email = input("Enter your email address: ")
auth_token = None

# Used for authentication


def token(email):
    global auth_token
    if not auth_token:
        url = base.format("api-token-auth/")
        resp = requests.post(url, data={"email": email})
        auth_token = {"Authorization": "JWT " + resp.json()['token']}
        resp.close()
    return auth_token

# Fetch the challenge and hint for level n

print(token(email))

def fetch(n):
    url = base.format("challenge/{}/".format(n))
    resp = requests.get(url, headers=token(email))
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json()['detail'])
    return resp.json()

# Submit a guess for level n


def solve(n, guess):
    url = base.format("challenge/{}/".format(n))
    data = {"guess": guess}
    resp = requests.post(url, headers=token(email), data=data)
    resp.close()
    if resp.status_code != 200:
        raise Exception(resp.json()['detail'])
    return resp.json()

# Fetch level 1

level = 1
hashes = {}
data = fetch(level)
print (data)

# Level 1 is a caesar cipher and gives you the password

guess = data['challenge']

# edit guess by changing it 3 letters right.

newString = ''

for x in guess:
    stringAsInt = ord(x)
    # lowercase letter wrap around
    if(stringAsInt >= 97 and stringAsInt <= 122):
        stringAsInt += 3
        if(stringAsInt > 122):
            difference = stringAsInt - 122
            stringAsInt = 96 + difference
    elif(stringAsInt >= 65 and stringAsInt <= 90):
        stringAsInt += 3
        if(stringAsInt > 90):
            difference = stringAsInt - 90
            stringAsInt = 64 + difference
    newString += chr(stringAsInt)


# If we obtained a hash add it to the dict
if 'hash' in h:
    hashes[level] = h['hash']


# Display all current hash
for k, v in hashes.items():
    print("Level {}: {}".format(k, v))
