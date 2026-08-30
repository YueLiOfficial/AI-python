from sklearn.datasets import load_iris
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score


def dm01():
    iris_data = load_iris()

    # print(iris_data.keys())

    print(iris_data.feature_names)
    # print(iris_data.data)
    # print(iris_data.DESCR)
    # print(iris_data.target)
    # print(iris_data.target_names)
    # print(iris_data.filename)

def dm02():
    iris_data = load_iris()

    iris_df = pd.DataFrame(data=iris_data.data, columns=iris_data.feature_names)

    iris_df["label"] = iris_data.target

    # print(iris_df.head(5))
    # print(iris_df.isna().sum())

    # hue: 用不同颜色显示， fit_reg: 拟合回归线
    sns.lmplot(iris_df, x="sepal length (cm)", y="sepal width (cm)", hue="label", fit_reg=False)
    plt.title("iris data")
    plt.show()

def dm03():
    iris_data = load_iris()

    x_train, x_test, y_train, y_test = train_test_split(
        iris_data.data,
        iris_data.target,
        test_size=0.2,
        random_state=22
    )

    print(f"训练集x: {len(x_train)}")
    print(f"训练集y: {len(y_train)}")
    print(f"测试集x: {len(x_test)}")
    print(f"测试集y: {len(y_test)}")

def dm04():
    iris_data = load_iris()

    x_train, x_test, y_train, y_test = train_test_split(
        iris_data.data,
        iris_data.target,
        test_size=0.2,
        random_state=42
    )

    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    param_grid = {
        "n_neighbors": range(1, 15),
        "weights": ["uniform", "distance"],
        "p": [1, 2]
    }

    model = KNeighborsClassifier()

    grid = GridSearchCV(
        model,
        param_grid,
        cv=5
    )

    grid.fit(x_train, y_train)

    # print(grid.best_params_)
    # print(grid.best_score_)

    best_model = grid.best_estimator_

    y_predict = best_model.predict(x_test)
    
    # model.fit(x_train, y_train)

    # my_score = model.score(x_test, y_test)
    # print(my_score)

    # y_predict = model.predict(x_test)
    print(accuracy_score(y_test, y_predict))



def test():
    X = [
    [150, 7.0],
    [160, 7.2],
    [145, 6.8],
    [155, 7.1],
    [170, 7.5],

    [200, 8.0],
    [210, 8.2],
    [190, 7.8],
    [205, 8.1],
    [195, 7.9],

    [100, 5.5],
    [110, 5.7],
    [95, 5.3],
    [105, 5.6],
    [115, 5.8]
    ]

    y = [
        0, 0, 0, 0, 0,
        1, 1, 1, 1, 1,
        2, 2, 2, 2, 2
    ]

    data_df = pd.DataFrame(data=X, columns=["weight", "size"])
    data_df["label"] = y

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    transfer = StandardScaler()
    x_train = transfer.fit_transform(x_train)
    x_test = transfer.transform(x_test)

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(x_train, y_train)

    y_predict = model.predict(x_test)
    print(accuracy_score(y_test, y_predict))

    new_fruit = [[158, 7.1]]
    new_fruit = transfer.transform(new_fruit)
    fruit = model.predict(new_fruit)
    fruit_proba = model.predict_proba(new_fruit)
    print(fruit_proba)
    fruit_names = ["苹果", "橙子", "柠檬"]
    print(fruit_names[fruit[0]])


if __name__ == "__main__":
    # dm01()

    # dm02()

    # dm03()

    # dm04()

    test()
