import os
import chrome_case1 as case1
import chrome_case2 as case2

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report

if __name__ == '__main__':
    data_path = 'backup/'
    data_set_path = 'data_set'
    rule_path = 'easyprivacy.txt'

    files = []
    for dirpath, dirs, filesname in os.walk(data_path):
        files.extend(filesname)
        break

    rules = case2.load_rule(rule_path)

    for file in files:
        name, ext = os.path.splitext(file)
        if ext != '.json':
            continue
        case2.analyse_json(data_path + file, data_set_path, rules)

    targets, features = case2.load_data(data_set_path)




