from tabulate import tabulate


def get_table(data):
    head = ["Id", "Название", "Тема", "Сложность", "Кол. решивших"]
    return tabulate(data, headers=head, tablefmt="grid")