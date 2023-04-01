import csv
import re

#регуляерное выражение для поиска номеров телефонов
pattern = r"(\+?7|8)\s?\(?(\d{3})\)?[ -]?(\d{3})-?(\d{2})-?(\d{2})( )?\(?(доб\.)? ?(\d{4})?\)?"
#регуляерное выражение для замены на требуемый формат
subst = r"+7(\2)\3-\4-\5\6\7\8"

def separate_name(row):
    ''' правильное заполнение полей firstname, lastname, surname'''
    name = ' '.join(row[:3]).split()
    row[0] = name[0]
    row[1] = name[1]
    if len(name) > 2:
        row[2] = name[2]

def repaired_list(lst) -> list:
    ''' форматирование номеров телефонов, заполнение всех пустых полей и удаление дубликатов'''
    for contact in lst:
        for duplicate in lst:
            if contact[0] + contact[1] == duplicate[0] + duplicate[1]:
                for i in range(2,7):
                    if contact[i] == '' and duplicate[i] != '':
                        contact[i] = duplicate[i]
        contact[5] = re.sub(pattern, subst, contact[5])
    new_lst = []
    for el in lst:
        if not el in new_lst:
            new_lst.append(el)
    return new_lst

def main():
    ''' чтение данных из файла, правка списка в адресной книге и запись его в новый файл'''
    with open(r'phonebook_raw.csv', 'r', encoding='utf-8') as fin:
        rows = list(csv.reader(fin, delimiter=',', quotechar='"'))
    for row in rows[1:]:
        separate_name(row)
    with open(r'phonebook.csv', 'w', encoding='utf-8') as fout:
        datawriter = csv.writer(fout, delimiter=',')
        datawriter.writerows(sorted(repaired_list(rows)))

if __name__ == '__main__':
    main()