import json


def price_sum():
    sum = 0
    with open('data/data.jsonl', 'r') as f:
        lines = f.readlines()
    for row in range(len(lines)):
        cont = json.loads(lines[row])
        sum += float(cont['cost'])
        print(cont['cost'], end=' ')
    print(sum)


def length():
    sum = 0
    with open('data/data.jsonl', 'r') as f:
        lines = f.readlines()
    for row in range(len(lines)):
        cont = json.loads(lines[row])
        sum += len(cont['transcript']) + len(cont['knowledge_base'])
    print(sum)

if __name__ == '__main__':
    # price_sum()
    length()
