class Value:
    """
    Adding ADDITION, SUBTRACTION, DIVISION, MULTIPLICATION
    """

    def __init__(self, data):
        self.data = data

    def __add__(self, other):
        return Value(self.data + other.data)

    def __truediv__(self, other):
        return Value(self.data / other.data)

    def __mul__(self, other):
        return Value(self.data * other.data)

    def __sub__(self, other):
        return Value(self.data - other.data)

    def __repr__(self):
        return f"Value(data={self.data})"


def tax_cal_bonus(x):
    x = x / 12.0
    tax_rates = [
        (3000, 0.03, 0),
        (12000, 0.1, 210),
        (25000, 0.2, 1410),
        (35000, 0.25, 2660),
        (55000, 0.3, 4410),
        (80000, 0.35, 7160),
        (float("inf"), 0.45, 15160),
    ]

    tax = 0.0
    for i in range(len(tax_rates)):
        if x <= tax_rates[i][0]:
            tax += x * tax_rates[i][1]
            break
        else:
            if x <= tax_rates[i + 1][0]:
                tax += x * 12 * tax_rates[i + 1][1] - tax_rates[i + 1][2]
                break
            else:
                continue
                # tax += (tax_rates[i + 1][0] - tax_rates[i][0]) * tax_rates[i + 1][1]

    return tax


def tax_cal_base(x):
    tax_rates = [
        (36000, 0.03, 0),
        (144000, 0.1, 2520),
        (300000, 0.2, 16920),
        (420000, 0.25, 31920),
        (660000, 0.3, 52920),
        (960000, 0.35, 85920),
        (float("inf"), 0.45, 181920),
    ]

    tax = 0.0
    for i in range(len(tax_rates)):
        if x <= tax_rates[i][0]:
            tax += x * tax_rates[i][1]
            break
        else:
            if x <= tax_rates[i + 1][0]:
                tax += x * tax_rates[i + 1][1] - tax_rates[i + 1][2]
                break
            else:
                continue
            # tax += tax_rates[i][0] - tax_rates[i + 1][2]

    return tax


def f(x, income):
    year_bonus = income - x
    tax_base = tax_cal_base(x)
    tax_bonus = tax_cal_bonus(year_bonus)
    return tax_base + tax_bonus


def opt_salary_balance_ml(
    shebao_gjj_month, special_deduction_year, year_bonus=None, income_range=[]
):
    # use to balance corporate income tax
    for income in range(income_range[0], income_range[1], 1000):
        remain_incom = income - shebao_gjj_month * 12 - special_deduction_year
        # if year_bonus is None:
        base = remain_incom - year_bonus
        tax_all = f(base, remain_incom)
        print(
            {
                "all_income": income,
                "base_salart": base,
                "year_bonus": year_bonus,
                "tax_all": tax_all,
                "tax_rate": tax_all / income,
            }
        )


def f(x, income):
    year_bonus = income - x
    tax_base = tax_cal_base(x)
    tax_bonus = tax_cal_bonus(year_bonus)
    return tax_base + tax_bonus


def optimize_f(income, x_min, x_max, num_steps=1000):
    min_value = float("inf")
    min_x = None

    step_size = (x_max - x_min) / num_steps

    for i in range(num_steps + 1):
        x = x_min + i * step_size
        value = f(x, income)

        if value < min_value:
            min_value = value
            min_x = x

    return min_x


# 示例使用的是遍历算法，可以根据具体情况选择其他更高效的优化算法

# 调用示例
income = 1000000  # 你需要提供具体的收入(扣除社保公积金与专项扣除后的总年薪)
x_min = 0  # x的最小值(基本工资)
x_max = 1000000  # x的最大值(基本工资)
min_x = optimize_f(income, x_min, x_max)

print(
    f"The minimum value of f is achieved at x-base-salay = {min_x}",
    f"bonus: {income-min_x}",
)


def tax_cal_base(x):
    if x <= 36000:
        tax = 0.0
    elif x > 36000 and x <= 144000:
        tax = 36000 * 0.03 + (x - 36000) * 0.1
    elif x > 144000 and x <= 300000:
        tax = 36000 * 0.03 + (144000 - 36000) * 0.1 + (x - 144000) * 0.2
    elif x > 300000 and x <= 420000:
        tax = (
            36000 * 0.03
            + (144000 - 36000) * 0.1
            + (300000 - 144000) * 0.2
            + (x - 300000) * 0.25
        )
    elif x > 420000 and x <= 660000:
        tax = (
            36000 * 0.03
            + (144000 - 36000) * 0.1
            + (300000 - 144000) * 0.2
            + (420000 - 300000) * 0.25
            + (x - 420000) * 0.3
        )
    elif x > 660000 and x <= 960000:
        tax = (
            36000 * 0.03
            + (144000 - 36000) * 0.1
            + (300000 - 144000) * 0.2
            + (420000 - 300000) * 0.25
            + (660000 - 420000) * 0.3
            + (x - 660000) * 0.35
        )
    else:
        tax = (
            36000 * 0.03
            + (144000 - 36000) * 0.1
            + (300000 - 144000) * 0.2
            + (420000 - 300000) * 0.25
            + (660000 - 420000) * 0.3
            + (960000 - 660000) * 0.35
            + (x - 960000) * 0.45
        )
    return tax


### 修改后可用：


def tax_cal_bonus(x):
    x = x / 12.0
    tax_rates = [
        (3000, 0.03, 0),
        (12000, 0.1, 210),
        (25000, 0.2, 1410),
        (35000, 0.25, 2660),
        (55000, 0.3, 4410),
        (80000, 0.35, 7160),
        (float("inf"), 0.45, 15160),
    ]

    tax = 0.0
    for i in range(len(tax_rates)):
        if x <= tax_rates[i][0]:
            tax += x * 12 * tax_rates[i][1]
            break
        else:
            if x <= tax_rates[i + 1][0]:
                tax += x * 12 * tax_rates[i + 1][1] - tax_rates[i + 1][2]
                break
            else:
                continue
                # tax += (tax_rates[i + 1][0] - tax_rates[i][0]) * tax_rates[i + 1][1]

    return tax


def tax_cal_base(x):
    tax_rates = [
        (36000, 0.03, 0),
        (144000, 0.1, 2520),
        (300000, 0.2, 16920),
        (420000, 0.25, 31920),
        (660000, 0.3, 52920),
        (960000, 0.35, 85920),
        (float("inf"), 0.45, 181920),
    ]

    tax = 0.0
    for i in range(len(tax_rates)):
        if x <= tax_rates[i][0]:
            tax += x * tax_rates[i][1]
            break
        else:
            if x <= tax_rates[i + 1][0]:
                tax += x * tax_rates[i + 1][1] - tax_rates[i + 1][2]
                break
            else:
                continue
            # tax += tax_rates[i][0] - tax_rates[i + 1][2]

    return tax


def f(x, income):
    year_bonus = income - x
    tax_base = tax_cal_base(x)
    tax_bonus = tax_cal_bonus(year_bonus)
    return tax_base + tax_bonus


def f(x, income):
    year_bonus = income - x
    tax_base = tax_cal_base(x)
    tax_bonus = tax_cal_bonus(year_bonus)
    return tax_base + tax_bonus


def optimize_f(income, x_min, x_max, num_steps=1000):
    min_value = float("inf")
    min_x = None

    step_size = (x_max - x_min) / num_steps

    for i in range(num_steps + 1):
        x = x_min + i * step_size
        value = f(x, income)

        if value < min_value:
            min_value = value
            min_x = x

    return min_x


# 示例使用的是遍历算法，可以根据具体情况选择其他更高效的优化算法

# 调用示例
income = 270000  # 你需要提供具体的收入(扣除社保公积金与专项扣除后的总年薪)
income_kou = income - 639 * 12 - 42000 - 360 * 12 - 5000 * 12  # 5000*12：每月免税额
x_min = 0  # x的最小值(基本工资)
x_max = income_kou  # x的最大值(基本工资)
min_x = optimize_f(income_kou, x_min, x_max)
tax = f(min_x, income_kou)
bonus = income_kou - min_x
tax_bonus = tax_cal_bonus(bonus)
salay_tax = tax_cal_base(min_x)
# print(tax,bonus,tax_bonus)
# print(f"The minimum value of f is achieved at x-base-salay = {min_x}",f"bonus: {income-min_x}")
print(
    f" 最优应纳所得税额= {min_x}\n",
    f"年终奖: {income-min_x}\n",
    f"总个税额：{tax}\n",
    f"其中工资个税：{salay_tax}",
    f"年终奖应纳个税：{tax_bonus}\n",
    f"税率：{round((tax/income)*100,2)}%",
)
