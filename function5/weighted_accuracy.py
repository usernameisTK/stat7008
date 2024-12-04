import numpy as np

prediction = ['AA', 'AA', 'A', 'A', 'A', 'AA', 'A', 'A', 'A', 'A', 'AA', 'AAA', 'BBB', 'AA', 'A'
, 'AAA', 'A', 'BBB', 'A', 'AA', 'A', 'BBB', 'A', 'AA', 'BBB', 'BBB', 'AA']
prediction = np.array(prediction)

true = ['A', 'BB', 'AA', 'A', 'AA', 'AA', 'AA', 'BBB', 'BBB', 'A', 'BBB', 'AAA', 'BB', 'A'
, 'AA', 'AAA', 'A', 'BBB', 'AA', 'A', 'AA', 'BBB', 'AAA', 'AA', 'AA', 'BBB', 'AA']
true = np.array(true)



def weighted_accuracy(y_true, y_pred):
    if len(y_true) != len(y_pred):
        print('Error: Input length is not equal')
    else:
        # 定义映射字典
        mapping = {
            'AAA': 1,
            'AA': 2,
            'A': 3,
            'BBB': 4,
            'BB': 5,
            'B': 6,
            'CCC': 7
        }

        # 将预测和真实值转化为对应的数字
        prediction_numeric = np.array([mapping.get(item, 0) for item in prediction])  # 未匹配到的项将被转化为 0
        true_numeric = np.array([mapping.get(item, 0) for item in true])

        result = 0 # result表示正确的数量

        for i in range(len(prediction_numeric)):
            weighted = [1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

            # 假设正确的时候，result+=1; 不正确的时候，相差一个级数的时候也补偿0.5（或其他数字）;q其余的都设置成0
            result += weighted[abs(prediction_numeric[i] - true_numeric[i])]

        weighted_acc = result / len(prediction_numeric)

        return weighted_acc

print(weighted_accuracy(true, prediction))



