# 引言

# 安装使用

Pandas 可以通过 pip 直接安装。

```
pip install pandas
```

由于 Pandas 总是与 NumPy 结合使用，因此使用时首先导入 NumPy 和 Pandas 两个模块。

```python
import pandas as pd
import numpy as np
```

# 数据结构

Pandas 的主要数据结构是 Series（一维数据）与 DataFrame（二维数据），这两种数据结构足以处理金融、统计、社会科学、工程等领域里的大多数典型用例。

| 维数 |   名称    |                描述                |
| :--: | :-------: | :--------------------------------: |
|  1   |  Series   |        带标签的一维同构数组        |
|  2   | DataFrame | 带标签的，大小可变的，二维异构表格 |

“**数据对齐是 Pandas 的内在属性**”，除非显式指定，Pandas 不会断开标签和数据之间的连接。

> **注意**
>
> Pandas 用 `NaN`（Not a Number）表示**缺失数据**。

## 一维数据 Series

Series 是带标签的一维数组，可存储整数、浮点数、字符串、Python 对象等类型的数据。轴标签统称为**索引**。调用 `pd.Series` 函数即可创建 Series：

```python
s = pd.Series(data, index=index)
```

上述代码中，`data` 支持以下数据类型：

- Python 字典
- 一维数组（包括 NumPy 的 ndarray，Python 的 list 和 tuple）
- 标量值（如，5）

`index` 是轴标签列表。不同**数据**可分为以下几种情况：

`data` 是多维数组时，**index** 长度必须与 **data** 长度一致。没有指定 `index` 参数时，创建数值型索引，即 `[0, ..., len(data) - 1]`。

```python
s = pd.Series([1, 3, 5, np.nan, 6, 8])
```

`data` 是标量值时，必须提供索引。`Series` 按**索引**长度重复该标量值。

```python
s = pd.Series(5., index=['a', 'b', 'c', 'd', 'e'])
```

Series 可以用字典实例化，其中字典的 key 构成了索引。如果指定了索引，则索引中不在字典内的值为 nan。

```python
d = {'b': 1, 'a': 0, 'c': 2}
s = pd.Series(d)
```

## 二维数据 DataFrame

**DataFrame** 是由多种类型的列构成的二维标签数据结构，类似于 Excel 、SQL 表，或 Series 对象构成的字典。DataFrame 是最常用的 Pandas 对象，与 Series 一样，DataFrame 支持多种类型的输入数据：

- 一维 ndarray、列表、字典、Series 字典
- 二维 numpy.ndarray
- `Series`
- `DataFrame`

除了数据，还可以有选择地传递 **index**（行标签）和 **columns**（列标签）参数，**index** 和 **columns** 属性分别用于访问行、列标签：

```python
d = {'one': pd.Series([1., 2., 3.], index=['a', 'b', 'c']), 
     'two': pd.Series([1., 2., 3., 4.], index=['a', 'b', 'c', 'd'])}
df = pd.DataFrame(d)
```

# 数据查看

`DataFrame.to_numpy` 输出底层数据的 NumPy 对象。注意，DataFrame 的列由多种数据类型组成时，该操作耗费系统资源较大，这也是 Pandas 和 NumPy 的本质区别：**NumPy 数组只有一种数据类型，DataFrame 每列的数据类型各不相同**。调用 `DataFrame.to_numpy` 时，Pandas 查找支持 DataFrame 里所有数据类型的 NumPy 数据类型。还有一种数据类型是 `object`，可以把 DataFrame 列里的值强制转换为 Python 对象。

# 参考

- [Pandas user guide](https://pandas.pydata.org/docs/user_guide/index.html#user-guide)
- [十分钟入门Pandas | Pandas 中文](https://www.pypandas.cn/docs/getting_started/10min.html)
