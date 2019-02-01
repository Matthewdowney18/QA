import os
import random
import json
import re

from bs4 import BeautifulSoup

def make_datasets(dataset, filename, train_val_ratio, version):
    dataset_len = len(dataset)
    train_dataset_len = int(dataset_len*train_val_ratio)
    train_dataset = {"version":version}
    val_dataset = {"version":version}
    random.shuffle(dataset)
    train_dataset["data"] = dataset[:train_dataset_len]
    val_dataset["data"] = dataset[train_dataset_len:]

    train_filename = "{}/train_{}.json".format(filename, version)
    val_filename = "{}/dev_{}.json".format(filename, version)

    os.mkdir(filename)

    with open(train_filename, 'w') as fp:
        json.dump(train_dataset, fp)

    with open(val_filename, 'w') as fp:
        json.dump(val_dataset, fp)

def clean_string(string):
    patterns = [['\n', ''], ['\s{2,}','']]
    new_string = string
    for pattern in patterns:
        new_string = re.sub(pattern[0], pattern[1], new_string)
    #new_string = string.split('\n')[1][7:]
    return new_string

def get_answers(answers, id, type):
    result = []
    for answer in answers:
        answer_dict = {}
        answer_dict['id'] = "{}_{}".format(id, answer['id'])
        #answer_dict['text'] = clean_string(answer.text)
        answer_dict['text'] = ""
        if type == "Unanswerable":
            answer_dict["answer_start"] = -1
        else:
            answer_dict["answer_start"] = 0
        result.append(answer_dict)
    return result

def get_qas(text, id):
    qas = []
    for question in text:
        question_dict = {}
        question_dict["id"] = "{}_{}".format(id, str(question["id"]))
        question_dict["type"] = question["type"]
        question_dict["question"] = clean_string(str(question.next_element))

        answers = question.find_all('a')

        if question_dict["type"] == "Unanswerable":
            question_dict["is_impossible"] = True
            question_dict["plausible_answers"] = get_answers(answers[:3],
                question_dict["id"], question_dict["type"])
            question_dict["answers"] = []

        else:
            question_dict["is_impossible"] = False
            question_dict["plausible_answers"] = get_answers(answers[1:3],
                question_dict["id"], question_dict["type"])
            question_dict["answers"] = get_answers([answers[0]],
                 question_dict["id"], question_dict["type"])

        qas.append(question_dict)
    return qas


def get_paragraph(text, id):
    paragraph = {}
    paragraph["qas"] = get_qas(text.find_all("q"), id)
    paragraph["context"] = clean_string(text.find("text_body").text)
    return paragraph

def xml2list(texts):
    dataset = []
    for text in texts:
        text_data = {}
        text_data["text_id"] = text['id']
        text_data["author"] = clean_string(text.find("author").text)
        text_data["title"] = clean_string(text.find("title").text)
        text_data["url"] = clean_string(text.find("url").text)
        text_data["paragraphs"] = [get_paragraph(text, text_data["text_id"])]
        dataset.append(text_data)
    return dataset

def main():
    project_file = os.getcwd()
    version = '2'
    xml_dataset = "{}/fiction.xml".format(project_file)
    output_dir = "{}/fiction_reformatted_{}".format(project_file, version)

    handle = open(xml_dataset, 'r')
    soup = BeautifulSoup(handle,'lxml')

    texts = soup.find_all('text')
    dataset = xml2list(texts)

    make_datasets(dataset, output_dir, 0, version)



if __name__ == '__main__':
    main()