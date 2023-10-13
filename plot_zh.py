from matplotlib.font_manager import FontProperties
import seaborn as sns

sns.set(font=["sans-serif"])
sns.set_style("whitegrid", {"font.sans-serif": ["Heiti TC"]})
cities_counter = [
    ("好棒", 285),
    ("給我", 225),
    ("不要", 163),
    ("細柔", 136),
    ("吃飯", 130),
    ("小小", 124),
    ("深圳", 88),
    ("温州", 67),
    ("小知", 66),
    ("大之", 45),
]
sns.set_color_codes("pastel")
sns.barplot(
    x=[k for k, _ in cities_counter[:10]], y=[v for _, v in cities_counter[:10]]
)


alpha = 0.5
tolerance = 1e-5

# Perform Stochastic Gradient Descent
epochs = 1
decay = 0.99
batch_size = 10
iterations = 0
while True:
    order = np.random.permutation(len(train_x))
    train_x = train_x[order]
    train_y = train_y[order]
    b = 0
    while b < len(train_x):
        tx = train_x[b : b + batch_size]
        ty = train_y[b : b + batch_size]
        gradient = get_gradient(w, tx, ty)[0]
        error = get_gradient(w, train_x, train_y)[1]
        w -= alpha * gradient
        iterations += 1
        b += batch_size

    # Keep track of our performance
    if epochs % 100 == 0:
        new_error = get_gradient(w, train_x, train_y)[1]
        print("Epoch: %d - Error: %.4f" % (epochs, new_error))

        # Stopping Condition
        if abs(new_error - error) < tolerance:
            print("Converged.")
            break

    alpha = alpha * (decay ** int(epochs / 1000))
    epochs += 1

print("w =", w)
print("Test Cost =", get_gradient(w, test_x, test_y)[1])
print("Total iterations =", iterations)

import matplotlib.pyplot as plt
from matplotlib.font_manager import _rebuild

# plt.rcParams['font.sans-serif']=['Songti SC']
plt.rcParams["font.sans-serif"] = ["Heiti TC"]


plt.rcParams["axes.unicode_minus"] = False

y_model = np.polyval(w[::-1], np.linspace(0, 1, 100))
plt.plot(np.linspace(0, 1, 100), y_model, c="g", label="模型")
plt.scatter(train_x[:, 1], train_y, c="b", label="训练数据集")
plt.scatter(test_x[:, 1], test_y, c="r", label="测试数据集")
plt.grid()
plt.legend(loc="best")
plt.xlabel("X")
plt.ylabel("Y")
plt.xlim(0, 1)
plt.savefig("reg.png")
plt.show()

# 查看支持哪些字体
from matplotlib import font_manager

ttf_lists = font_manager.fontManager.ttflist
for font in ttf_lists:
    print(font)
