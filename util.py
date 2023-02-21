def add_new_id(table):
    new_id = [1]
    for row in table:
        new_id.append(int(row[0]))
    new_id = max(new_id) + 1
    return str(new_id)


def find_line(table, question_id, id_number):
    line = 0
    if line < len(table)-1 and table[line][id_number] != str(question_id):
        line += 1
    return table[line]


