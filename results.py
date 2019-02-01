import argparse
import json

def get_targets(dataset_filename):
    with open(dataset_filename, "r", encoding='utf-8') as reader:
        dataset = json.load(reader)

    targets = {}
    for text in dataset["data"]:
        for question in text["paragraphs"]:

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--nbest_filename", default=None, required=True)
    parser.add_argument("--dataset_filename", default=None, required=True)

    args = parser.parse_args()



    targets = get_targets(args.dataset_filename)

    with open(args.nbest_filename, "r", encoding='utf-8') as reader:
        predictions = json.load(reader)



if __name__=='__main__':
    main()
