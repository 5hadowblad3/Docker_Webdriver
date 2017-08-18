from chrome_case2 import *

if __name__ == '__main__':
    path = 'backup/'
    rules_location = 'easyprivacy.txt'
    rules = load_rule(rules_location)
    files = os.listdir(path)

    for file in files:
        print file
        name, ext = os.path.splitext(file)
        if ext is not '.json':
            continue
        analyse_json(file, 'test_data_set', rules)
