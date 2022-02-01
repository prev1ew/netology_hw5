SEPARATOR = ' | '  # may be used somewhere else

def get_cook_book():
    cook_book = {}
    with open('recipes.txt') as f:
        current_value = []
        current_key = ''
        current_step = 0

        for line in f:
            stripped_line = line.strip()

            if not stripped_line and current_key:  # empty row
                cook_book[current_key] = current_value
                current_value = []
                current_key = ''
                current_step = 0
                continue

            if current_step == 0:
                current_key = stripped_line

            # elif current_step == 1:
            #     # количество ингредиентов, оно мне в тек момент не нужно поэтому тут пока ничего нет

            elif current_step == 2:
                # ингредиент (сеп) колво (сеп) юниты
                if not stripped_line:
                    current_step = 0
                    continue

                splitted_string = stripped_line.split(SEPARATOR)
                if len(splitted_string) >= 3:
                    ingredients = dict()
                    ingredients['ingredient_name'] = splitted_string[0]
                    ingredients['quantity'] = splitted_string[1]
                    ingredients['measure'] = splitted_string[2]
                    current_value.append(ingredients)
                    continue

            current_step += 1

    return cook_book


def get_shop_list_by_dishes(dishes, person_count):
    result = dict()
    cook_book = get_cook_book()
    list_of_dishes = cook_book.keys()
    for dish in dishes:
        if dish in list_of_dishes:
            current_item = cook_book[dish]
            for item in current_item:
                ingredient_name = item['ingredient_name']
                if ingredient_name in result.keys():
                    already_existed_record = result[ingredient_name]
                    already_existed_record['measure'] = item['measure']
                    already_existed_record['quantity'] += int(item['quantity']) * person_count
                    result[ingredient_name] = already_existed_record
                else:
                    description = dict()
                    description['measure'] = item['measure']
                    description['quantity'] = int(item['quantity']) * person_count
                    result[ingredient_name] = description
    return result


def merge_files(list_of_files, end_file):
    result = []
    files_and_count_of_rows = {}
    files_and_rows = {}
    for file in list_of_files:
        with open(file) as f:
            total_lines = sum(1 for line in f)
            files_and_count_of_rows[f.name] = total_lines

            file_rows = list()
            file_rows.append(f.name)
            file_rows.append(total_lines)

        # Так как мне нужен второй цикл - открываю заново, не знаю как сбросить поинтер в начало
        with open(file) as f:
            for line in f:
                file_rows.append(line.strip())

            file_rows.append('')
            files_and_rows[f.name] = file_rows

    sorted_list = sorted(files_and_count_of_rows.items(), key=lambda x: x[1])
    for k in sorted_list:
        current_item = files_and_rows[k[0]]
        for line in current_item:
            result.append(line)

    with open(end_file, 'w') as f:
        for line in result:
            f.write(str(line) + '\n')



print(get_cook_book())
print(get_shop_list_by_dishes(['Запеченный картофель', 'Запеченный картофель', 'Омлет'], 2))
merge_files(['test1', 'test2', 'test3'], 'res')






