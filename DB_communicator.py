def get_high(name):
    result = 0
    DataBase = open("DataBase.txt", "r")
    lines = DataBase.readlines()
    for line in lines:
        line = line.split()
        if line[0] == name and int(line[1]) > result:
            result = int(line[1])
    return result


def make_a_record(name, score):
    line = f"{name} {str(score)}" + '\n'
    DataBase = open("DataBase.txt", "a+")
    DataBase.write(line)


def get_all():
    DataBase = open("DataBase.txt", "r")
    return DataBase.readlines()


if __name__ == '__main__':
    DataBase = open("DataBase.txt", "r")
    lines = DataBase.readlines()
    make_a_record("Roba", 3770)
    print(get_high("Greg"))
    for line in lines:
        print(line)
