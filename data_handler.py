import csv
import time

# def read_csv(filename):
#     with open(filename, "r", encoding="utf-8") as file:
#         read = csv.reader(file)
#         # header = next(read, None)
#         # if header != None:
#         return [row for row in read]
#
#
# def write_csv(filename, new_data):
#     with open(filename, "w", newline='', encoding="utf-8") as file:
#         write = csv.writer(file)
#         for row in new_data:
#             # if any(row):
#             write.writerow(row)

def get_field_names_from_csv(filename):
    with open(filename, encoding="utf-8") as file:
        read_csv = csv.DictReader(file)
        return read_csv.fieldnames

def read_csv(filename):
    with open(filename, encoding="utf-8") as file:
        read_csv = csv.DictReader(file)
        list_of_dict = []
        for row in read_csv:
            list_of_dict.append(row)
        return list_of_dict


def write_csv(filename, new_data):
    fields_name = get_field_names_from_csv(filename)
    # print(new_data)
    with open(filename, "w", newline='', encoding="utf-8") as file:
        write_csv = csv.DictWriter(file, fieldnames=fields_name)
        write_csv.writeheader()
        write_csv.writerows(new_data)


def append_question_csv_row(filename, row):
    rows = read_csv(filename)
    maximum_row = max(rows, key=lambda r: r["id"])
    row["id"] = int(maximum_row["id"]) + 1
    with open(filename, 'a', newline='', encoding="utf-8") as file:
        write_csv = csv.DictWriter(file, fieldnames=row.keys())
        write_csv.writerow(row)


def append_csv_row(filename, data):
    file_data = read_csv(filename)
    if 'question' in filename:
        new_data = {
            'id': len(file_data) + 1,
            'submission_time': int(time.time()),
            'view_number': 0,
            'vote_number': 0,
            'title': data['title'],
            'message': data['message'],
            'image': data['image'],
        }
    elif 'answer' in filename:
        new_data = {
            'id': len(file_data) + 1,
            'submission_time': int(time.time()),
            'vote_number': 0,
            'question_id': data['question_id'],
            'message': data['message'],
            'image': 0,
        }
    file_data.append(new_data)
    write_csv(filename, file_data)


def pick_id(id, file):
    list_of_id = read_csv(file)
    for row in list_of_id:
        if row['id'] == id:
            return row

def view_number(filename, data):
    file_data = read_csv(filename)
    for question in file_data:
        if question == data:
            question['view_number'] = int(question['view_number']) + 1
    write_csv(filename, file_data)

def delete_question(filename, data):
    file_data = read_csv(filename)
    file_data.remove(data)
    write_csv(filename, file_data)


def delete_answers_to_question(filename, question_id):
    file_data = read_csv(filename)
    updated_data = [answer for answer in file_data if answer['question_id'] != question_id]
    write_csv(filename, updated_data)


def vote_changer(filename, data, decision):
    file_data = read_csv(filename)
    for dictionary in file_data:
        if dictionary == data and decision == True:
            dictionary['vote_number'] = int(dictionary['vote_number']) + 1
            write_csv(filename, file_data)
        elif dictionary == data and decision == False:
            dictionary['vote_number'] = int(dictionary['vote_number']) - 1
            write_csv(filename, file_data)

def edit_data(filename, web_data, data):
    file_data = read_csv(filename)
    data_index = file_data.index(data)
    for key in web_data.keys():
        if key in file_data[data_index].keys():
            file_data[data_index][key] = web_data[key]
    write_csv(filename, file_data)

# def pick_in_q_in_a(id, file):
#     list_of_id = read_csv(file)
#     for row in list_of_id:
#         if row['question_id'] == id:
#             return row