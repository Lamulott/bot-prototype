import csv


def get_notes(info: list) -> csv:
    for film in info:
        with open('new_films.csv', 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(
                film
            )


def read_notes():
    with open('new_films.csv', encoding='utf-8') as file:
        rows = csv.reader(file)  # создаем reader объект
        for row in rows:
            print(row)


if __name__ == '__main__':
    print('This is a csvReader')
    read_notes()
