#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: GBK -*-

"""
Decision Tree Classification Example.
"""
from __future__ import print_function

from pyspark import SparkContext
from pyspark.mllib.tree import DecisionTree, DecisionTreeModel
from pyspark.mllib.util import MLUtils

if __name__ == "__main__":

    sc = SparkContext(appName="PythonDecisionTreeClassificationExample")

    # 加载和解析数据文件为RDD
    dataPath = "/home/zhb/Desktop/work/DecisionTreeShareProject/app/sample_libsvm_data.txt"
    print(dataPath)

    data = MLUtils.loadLibSVMFile(sc,dataPath)
    # 将数据集分割为训练数据集和测试数据集
    (trainingData,testData) = data.randomSplit([0.7,0.3])
    print("train data count: " + str(trainingData.count()))
    print("test data count : " + str(testData.count()))

    # 训练决策树分类器
    # categoricalFeaturesInfo 为空，表示所有的特征均为连续值
    model = DecisionTree.trainClassifier(trainingData, numClasses=2, categoricalFeaturesInfo={},
                                         impurity='gini', maxDepth=5, maxBins=32)

    # 测试数据集上预测
    predictions = model.predict(testData.map(lambda x: x.features))
    # 打包真实值与预测值
    labelsAndPredictions = testData.map(lambda lp: lp.label).zip(predictions)
    # 统计预测错误的样本的频率
    testErr = labelsAndPredictions.filter(lambda (v, p): v != p).count() / float(testData.count())
    print('Decision Tree Test Error = %5.3f%%'%(testErr*100))
    print("Decision Tree Learned classifiction tree model : ")
    print(model.toDebugString())

    # 保存和加载训练好的模型
    modelPath = "/home/zhb/Desktop/work/DecisionTreeShareProject/app/myDecisionTreeClassificationModel"
    model.save(sc, modelPath)
    sameModel = DecisionTreeModel.load(sc, modelPath)
