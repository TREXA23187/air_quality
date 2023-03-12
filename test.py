from sklearn import datasets
import numpy as np
from sklearn.neural_network import MLPClassifier

np.random.seed(0)
iris = datasets.load_iris()
iris_x = iris.data
iris_y = iris.target
indices = np.random.permutation(len(iris_x))
# 训练数据集
iris_x_train = iris_x[indices[:-10]]
iris_y_train = iris_y[indices[:-10]]
# 测试训练集
iris_x_test = iris_x[indices[-10:]]
iris_y_test = iris_y[indices[-10:]]

# 建立神经网络模型
clf = MLPClassifier(solver='lbfgs', alpha=1e-5,
                    hidden_layer_sizes=(10, 10, 10), random_state=1)
# 调用fit函数就可以进行模型训练，一般的调用模型函数的训练方法都是fit()
clf.fit(iris_x_train, iris_y_train)  # 训练
iris_y_predict = clf.predict(iris_x_test)  # 预测
# score=clf.score(iris_x_test,iris_y_test,sample_weight=None)
# print('Accuracy:',score)

print('iris_y_predict = ')
print(iris_y_predict)
print('iris_y_test = ')
print(iris_y_test)
# print(iris_x_train.shape)
# print(iris_y_train.ravel().shape)
# 模型就这样训练好了，而后我们可以调用多种函数来获取训练好的参数
# 比如获取准确率
print('训练集的准确率是：', clf.score(iris_x_test, iris_y_test.ravel()))
# 比如输出当前的代价值
print('训练集的代价值是：', clf.loss_)
# 比如输出每个0的权重
print('训练集的权重值是：', clf.coefs_)
