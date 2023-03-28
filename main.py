import json

# how to get an index of a number inside a list?
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

def panda_print():
    import pandas as pd
    df = pd.read_json('data/transcript_data.jsonl', lines=True)
    print(df)


if __name__ == '__main__':
    # price_sum()
    # length()
    panda_print()
