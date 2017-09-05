import os
import graphviz
import numpy as np
import random
import matplotlib.pyplot as plt
import chrome_case1 as case1
import chrome_case2 as case2

from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score
from sklearn import svm
from sklearn import tree
from sklearn.cluster import KMeans
from sklearn.metrics import average_precision_score
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report


def random_color():
    color_red = random.randint(16, 255)
    color_blue = random.randint(16, 255)
    color_green = random.randint(16, 255)
    return '#' + str(hex(color_red)[2:]) + str(hex(color_green)[2:]) + str(hex(color_blue)[2:])


def draw(scores_set, types, catagory):
    fig, ax = plt.subplots(1, 5)
    fig.canvas.set_window_title('Evaluation')

    colors = [random_color() for i in xrange(len(types))]

    for index, scores in enumerate(scores_set):
        for pos in xrange(0, len(scores)):
            ax[index].bar(pos, scores[pos], align='center', alpha=0.4, color=colors[pos])

        ax[index].legend(types, loc='upper left')
        print catagory, index
        ax[index].set_title(catagory[index])
        ax[index].set_ylim(0, 1.05)
        ax[index].grid(True)

        # ax[1].bar(pos, average_precision_rate, align='center', alpha=0.4, color=random_color())
        # ax[1].set_title("Average Precision Rate")
        # ax[1].legend(source, loc='upper left')
        # ax[1].set_ylim(0.0, 1.2)
        # ax[1].grid(True)
        #
        # ax[2].bar(pos, f1_measures, align='center', alpha=0.4, color=random_color())
        # ax[2].set_title("F1 Measure")
        # ax[2].legend(source, loc='upper left')
        # ax[2].set_ylim(0.0, 1.2)
        # ax[2].grid(True)
        #
        # pos = np.arange(1, len(classification_rate) + 1)
        # ax[3].bar(pos, classification_rate, align='center', alpha=0.4, color=random_color())
        # ax[3].set_title("Classification Rate")
        # ax[3].legend(source, loc='upper left')
        # ax[3].set_ylim(0.0, 1.2)
        # ax[3].set_xlim(0.0, 3)
        # ax[3].grid(True)

    plt.show()

if __name__ == '__main__':
    data_path = 'backup/'
    # data_set_path = 'data_set2'
    data_set_path = 'data_set'
    rule_path = 'easyprivacy.txt'
    class_name = ['tracking', 'non-tracking']
    # feature_name = case1.init_label().keys()
    feature_name = case2.init_label().keys()
    scores_type = ['accuracy', 'f1', 'precision', 'recall', 'average_precision']
    feature_name.remove('label')
    # files = []
    # for dirpath, dirs, filesname in os.walk(data_path):
    #     files.extend(filesname)
    #     break
    #
    # rules = case2.load_rule(rule_path)
    #
    # for file in files:
    #     name, ext = os.path.splitext(file)
    #     if ext != '.json':
    #         continue
    #     case1.analyse_json(data_path + file, data_set_path)
    #     case2.analyse_json(data_path + file, data_set_path, rules)

    targets, features = case2.load_data(data_set_path)
    C = 1
    models = (
        # SVC family
        svm.SVC(kernel='linear', C=C),
        svm.LinearSVC(C=C),
        svm.SVC(kernel='rbf', gamma=0.7, C=C),
        svm.SVC(kernel='poly', degree=3, C=C),
        # decision trees family
        tree.DecisionTreeClassifier(),
        RandomForestClassifier(n_estimators=50),
        AdaBoostClassifier(n_estimators=300),
        MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(4, ))
    )
    # models = (clf.fit(features, targets) for clf in models)
    # clf = svm.SVC(kernel='linear', C=1)

    titles = ['SVC with linear kernel',
              'Linear SVC',
              'SVC with RBF kernel',
              'SVC with polynomial kernel',
              'DecisionTree',
              # 'K-means Cluster',
              'Random Forest',
              'AdaBoost',
              'Neural Network'
              ]

    evaluation_scores = []
    for ind, score_type in enumerate(scores_type):
        res = []
        for ind, clf in enumerate(models):
            temp = cross_val_score(clf, features, targets, scoring=score_type)
            print score_type
            print temp
            print temp.mean()
            res.append(temp.mean())

        evaluation_scores.append(res)

    # plt.ion()
    draw(evaluation_scores, titles, scores_type)

    # scores = (cross_val_score(clf, features, targets, scoring=scores_type) for clf in models)
    # for ind, score in enumerate(scores):
    #     print titles[ind]
    #     print score
    #     print score.mean()

    # precision = (average_precision_score())

    # importances = (for clf in models)
    # clf = clf.fit(features, targets)
    # scores = cross_val_score(clf, features, targets)
    #
    # print scores.mean()
    # print scores

    # decision trees
    # clf2 = tree.DecisionTreeClassifier()
    # clf2 = clf2.fit(features, targets)
    # dot_data = tree.export_graphviz(clf2, out_file=None, filled=True, rounded=True, \
    #                                 special_characters=True, class_names=class_name, feature_names=feature_name)
    # graph = graphviz.Source(dot_data)
    # graph.render('lala')
    # graph

    # K-means
    # avg = 0.0
    # times = 100
    # for i in xrange(times):
    #     clf3 = KMeans(n_clusters=2)
    #     res = clf3.fit(features)
    #
    #     cnt = 0
    #     for ind, element in enumerate(res.labels_):
    #         if element == targets[ind]:
    #             cnt += 1
    #     avg += float(cnt) / float(len(res.labels_))
    #     print cnt, len(res.labels_)
    #
    # print avg / times
    # print cross_val_score(clf3, features, targets, scoring='accuracy')





