import random
import atexit
import functools
from collections import deque
from flask import Flask, escape, request

# Simple fingerprint endpoint.
# Can generate 877,000 unique fingerprints

def save_used():
    f = open('used', 'w', encoding='utf-8')
    f.write('\n'.join(used))
    f.close()

atexit.register(save_used)

with open('wordlists/nouns', 'r', encoding='utf-8') as f:
    nouns = [word.rstrip('\n') for word in f]
with open('wordlists/adjectives', 'r', encoding='utf-8') as f:
    adjectives = [word.rstrip('\n') for word in f]

used = set()
with open('used', 'r+', encoding='utf-8') as f:
    for l in f:
        used.add(l.rstrip('\n'))
        
fingerprints = []

# generate fingerprints
for adj in adjectives:
    for noun1 in nouns:
        fingerprint = f'{adj}-{noun1}'
        if fingerprint not in used:
            fingerprints.append(f'{adj}-{noun1}')

# randomize order
random.shuffle(fingerprints)
fingerprints = deque(fingerprints)

# start flask server
app = Flask(__name__)

@app.route('/next')
def get_next():
    fingerprint = fingerprints.pop()
    used.add(fingerprint)
    return fingerprint

if __name__ == '__main__':
    app.run()

