import math
import os


def chain_enum(e: int, n: int) -> list:
    '''генерирует порядковые номера для расположения единиц
    в цепочке, состоящей из e-единици и n-нулей'''
    n = e + n
    k = e 
    
    for i in range(math.comb(n, k)):
        b = 0
        s = 0
        t = 1
        chain = [0]
        while True:
            if t <= k:
                j = int(chain[t - 1]) + 1
            else:
                yield chain[1:]
                break
            while j < (n - k + t) and (s + math.comb(n - j, k - t)) < i + 1:
                s += math.comb(n - j, k - t)
                j += 1
            
            b = j
            t += 1
            chain.append(b)


def numb_of_errors(a: int, b: int, chain: list) -> int:
    '''Рассчитывает количество ошибок в цепочке 
    с единицами на порядковых номерах из chain, c нормативными границами a, b'''
    
    # Количество единиц внутри нормативных границ
    ones_in = 0 
    # Количество единиц вне нормативных границ
    ones_out = 0
        
    for i in chain:
        if a <= i <= b:
            ones_in += 1
    ones_out = len(chain) - ones_in
    err_count = ones_out + (b - a +1) - ones_in
    
    return err_count


def ledg_coefficiant(err_count, max_err_count) -> int:
    return 1 - (err_count / max_err_count)


def print_first_tab() -> None:
    string = '|' + r"{:^6}|" * len(err_count_list)
    sep = "\n" + '-'* 20 + ('+' + '-' * 6) * len(err_count_list) + '|' + '\n'
    
    with open('first_tab.txt', 'w', encoding='utf-8') as file:
        file.write("{:<20}".format("Ледж-коэффициент") + string.format(*ledg_list) + sep)
        file.write("{:<20}".format("Повторность") + string.format(*err_count_list))
    

def print_second_tab() -> None:
    string = '|' + r"{:^6}|" * len(err_count_list)
    sep = "\n" + '-'* 20 + ('+' + '-' * 6) * len(err_count_list) + '|' + '\n'
    
    
    with open('second_tab.txt', 'w', encoding='utf-8') as file:
        file.write("{:<20}".format("Ледж-коэффициент") + string.format(*ledg_list) + sep)
        file.write("{:<20}".format("Вероятность встречи") + string.format(*chance))


def is_borders_acceptable(borders: list, chain: str) -> bool:
    if len(borders) != 2:
        return False

    a, b = borders
    try: 
        int(a), int(b)
    except ValueError:
        return False
    a, b = int(a), int(b) 

    if a <= 0 or b <= 0:
        print("Границы должны быть положительными")
        return False
    elif b <= a:
        print("Левая граница должна быть меньше правой")
        return False
    elif b > len(chain):
        return False
    else:
        return True


def chain_correct(chain: str) -> bool:
    for elem in chain:
        if elem != '0' and elem != '1':
            return False
    return True


def amount_ones_zeros(chain: str) -> tuple:
    e = chain.count('1')
    n = chain.count('0')
    return e, n


def str_chain_to_list(chain: str) -> list:
    code_chain = []
    for i in range(len(chain)):
        if chain[i] == '1':
            code_chain.append(i+1)
    return code_chain


if __name__ == "__main__":
    chain = input("Введите цепочку из единиц и нулей\n")
    while not chain_correct(chain):
        chain = input("Введите цепочку из единиц и нулей\n").lstrip()
    
    # Задаём нормативные границы
    borders = []
    borders = input("Введите нормативные границы через пробел\n").split()
    while not is_borders_acceptable(borders, chain):
        borders = input("Введите нормативные границы через пробел\n").split()
    a, b = map(int, borders)

    # Количество единиц и нулей
    e, n = amount_ones_zeros(chain)
    chain = str_chain_to_list(chain)

    curr_chain_errs = numb_of_errors(a, b, chain)
    
    print("Количество ошибок в заданой цепочке:", curr_chain_errs)

    print('Производим расчёты.')
    max_err_count = 0
    err_count_dict = {}
    for chain in chain_enum(e, n):
        err_count = numb_of_errors(a, b, chain)
        if err_count > max_err_count: max_err_count = err_count
        if err_count in err_count_dict: 
            err_count_dict[err_count] += 1 
        else:
            err_count_dict[err_count] = 1 

    err_list = sorted(err_count_dict.keys(), reverse=True)
    err_count_list = [err_count_dict[x] for x in err_list]
    ledg_list = [round(ledg_coefficiant(x, max_err_count), 4)
                 for x in err_list]
    chance = [round(x / math.comb(e + n, e), 4) for x in err_count_list]

    print_first_tab()
    print_second_tab()
    print('Расчёты завершены.')

    curr_chain_ledg = ledg_coefficiant(curr_chain_errs, max_err_count)
    print("Ледж коэффициент для заданной цепочки: {:.4}".format(curr_chain_ledg ))
    ledg_num = ledg_list.index(round(curr_chain_ledg, 4))
    connection_proba = sum(chance[ledg_num:])
    print("С такой вероятностью связь ступенчатого типа отсутствует:", round(connection_proba, 4))
    os.system("pause")
    
