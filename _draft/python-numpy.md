# 引言

NumPy 是使用 Python 进行科学计算的基本软件包。主要包括其强大的 N 维数组对象以及基于这些数据结构的数学计算工具包，包括线性代数、傅立叶变换和统计函数等。

NumPy 和 Python 列表对比：

NumPy Array|Standard Python Library
:---:|:---:
创建时固定大小|动态变化
元素类型必须相同|元素类型可以不同
大数据高级数学运算效率高|大数据高级数学运算效率低
许多科学计算包将其作为基础数据结构|许多科学计算包将其用于兼容性输入

# 多维数组 (ndarray)

NumPy 的主要对象是**齐次多维数组（简称数组）**，数组的所有元素**类型相同**，通过非负元组索引，其维度称为 axes。

## 基本属性

NumPy 的数组类为 ndarray，该类有几个比较重要的属性：

- ndarray.ndim：数组维度个数，使用整数表示。
- ndarray.shape：维度，使用整数元组表示每一维大小。例如 n 行 m 列二维数组的 shape 为 (n, m)
- ndarray.size：数组大小。等同于 shape 元素乘积。
- ndarray.dtype：数组元素类型。支持标准 Python 类型和一些拓展类型，例如 int32、int16、float64 等。
- ndarray.itemsize：数组元素字节数。等同于 ndarray.dtype.itemsize。
- ndarray.data：数组实际缓存区。一般通过下标访问数组而不用访问该原生类型。

```python
import numpy as np
a = np.arange(15).reshape(3, 5)
"""
[[ 0  1  2  3  4]   
 [ 5  6  7  8  9]   
 [10 11 12 13 14]]
"""
print(a.ndim)       # 2
print(a.shape)      # (3, 5)
print(a.size)       # 15
print(a.dtype)      # int32
print(a.itemsize)   # 4
print(a.data)       # <memory at 0x000001A62559E208>
print(a.dtype.name)
```

## 创建数组

如果已知数组元素，可以**通过 List 进行创建**。创建时可以选择元素类型。

```python
>>> import numpy as np
>>> a = np.array([2, 3, 4])
>>> a
array([2, 3, 4])
>>> b = np.array([(1.5, 2, 3), (4, 5, 6)])
>>> b
array([[1.5, 2. , 3. ],
       [4. , 5. , 6. ]])
>>> c = np.array([[1, 2], [3, 4]], dtype=complex)
>>> c
array([[1.+0.j, 2.+0.j],
       [3.+0.j, 4.+0.j]])
>>> 
```

通常，数组的元素最初是未知的，但是其大小是已知的。 因此 NumPy 提供了几个函数来创建**具有初始占位符内容的数组**。

```python
>>> np.zeros((3, 4))    # 默认为 float64
array([[0., 0., 0., 0.],
       [0., 0., 0., 0.],
       [0., 0., 0., 0.]])
>>> np.ones((2, 3, 4), dtype=np.int16)  # 指定类型
array([[[1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]],

       [[1, 1, 1, 1],
        [1, 1, 1, 1],
        [1, 1, 1, 1]]], dtype=int16)
>>> np.empty((2, 3))    # 未初始化，随机值
array([[1.5, 2. , 3. ],
       [4. , 5. , 6. ]])
```

可以使用 np.arange 函数创建**指定步长**的数组，类似于 range 函数。

```python
>>> np.arange(10, 30, 5)
array([10, 15, 20, 25])
>>> np.arange(0, 2, 0.3)    # 支持浮点数
array([0. , 0.3, 0.6, 0.9, 1.2, 1.5, 1.8])
```

由于浮点数精度原因，这样创建浮点数组元素个数可能和预期值不符合。因此可以使用 linspace 函数创建**指定个数**的数组。

```python
>>> np.linspace(0, 2, 9)
array([0.  , 0.25, 0.5 , 0.75, 1.  , 1.25, 1.5 , 1.75, 2.  ])
>>> x = np.linspace(0, 2*np.pi,100)
>>> f = np.sin(x)
```

## 打印数组

数组的打印直接通过 print() 函数即可。但如果数组个数较多，默认会省略中间值。但如果需要强制打印所有，可以设置如下。

```python
np.set_printoptions(threshold=sys.maxsize) 
```

## 基本运算

数组的代数运算是**逐元素**（elementwise）进行的，**运算结果由一个新数组保存**。

```python
>>> a = np.array( [20,30,40,50] )
>>> b = np.arange(4)
>>> a
array([20, 30, 40, 50])
>>> b
array([0, 1, 2, 3])
>>> a - b
array([20, 29, 38, 47])
>>> a + b
array([20, 31, 42, 53])
>>> a * 10
array([200, 300, 400, 500])
>>> b ** 2
array([0, 1, 4, 9])
>>> a * b
array([  0,  30,  80, 150])
>>> a < 35
array([ True,  True, False, False])
```

如果需要运算**矩阵乘**，使用 `@` 运算符或 dot 函数。

```python
>>> A = np.array([[1, 1],
...               [0, 1]])
>>> B = np.array([[2, 0],
...               [3, 4]])
>>> A * B
array([[2, 0],
       [0, 4]])
>>> A @ B
array([[5, 4],
       [3, 4]])
>>> A.dot(B)
array([[5, 4],
       [3, 4]])
>>> B @ A
array([[2, 2],
       [3, 7]])
>>> B.dot(A)
array([[2, 2],
       [3, 7]])
```

带有赋值符的复合运算符，例如 `+=` 和 `*=` 运算是原地修改数组，而不是创建一个新的数组作为结果。

```python
>>> a += b
>>> a
array([20, 31, 42, 53])
```

还有一些一元运算符是以函数的形式出现的。例如求和等。

## 通用函数

NumPy 提供了熟悉的数学函数，例如 sin，cos 和 exp。 在 NumPy 中，这些称为**通用函数**（ufunc），这些函数在数组上**逐元素**操作，生成数组作为输出。常用的有:

```python
>>> B = np.arange(3)
>>> B
array([0, 1, 2])
>>> np.exp(B)
array([1.        , 2.71828183, 7.3890561 ])
>>> np.sqrt(B)
array([0.        , 1.        , 1.41421356])
>>> np.min(B)
0
>>> np.max(B)
2
>>> np.cumsum(B)
array([0, 1, 3])
>>> np.log(B)
<stdin>:1: RuntimeWarning: divide by zero encountered in log
array([      -inf, 0.        , 0.69314718])
```

>See also:  
all, any, apply_along_axis, argmax, argmin, argsort, average, bincount, ceil, clip, conj, corrcoef, cov, cross, cumprod, cumsum, diff, dot, floor, inner, invert, lexsort, max, maximum, mean, median, min, minimum, nonzero, outer, prod, re, round, sort, std, sum, trace, transpose, var, vdot, vectorize, where

## 索引、切片、迭代

**一维数组**可以如 List 一样进行索引（indexing）、切片（slicing）、迭代（iterating）操作。

**多维数组**可以逐个维度进行索引和切片，以元组形式给出，并用逗号分隔。其中 `:` 表示该维度所有元素，连续的 `:` 可以替换为 `...`。

```python
>>> b
array([[ 0,  1,  2,  3],
       [10, 11, 12, 13],
       [20, 21, 22, 23],
       [30, 31, 32, 33],
       [40, 41, 42, 43]])
>>> b[1]
array([10, 11, 12, 13])
>>> b[2, 3]
23
>>> b[0:5, 1]
array([ 1, 11, 21, 31, 41])
>>> b[:,1]
array([ 1, 11, 21, 31, 41])
>>> b[1:3,:]
array([[10, 11, 12, 13],
       [20, 21, 22, 23]])
>>> b[-1,:]
array([40, 41, 42, 43])
>>> b[1,...]
array([10, 11, 12, 13])
>>> b[...,2]
array([ 2, 12, 22, 32, 42])
```

多维数组**迭代是逐维度**进行的。如果需要迭代数组的每一个元素，可以使用 flat 属性。

```python
>>> for x in b:
...     print(x)
... 
[0 1 2 3]
[10 11 12 13]
[20 21 22 23]
[30 31 32 33]
[40 41 42 43]

>>> for x in b.flat:
...     print(x)
... 
0
1
2
3
...
40
41
42
43
```

## 整形操作

### 改变形状

```python
>>> a = np.floor(10*rg.random((3,4)))
>>> a
array([[5., 9., 1., 9.],
       [3., 4., 8., 4.],
       [5., 0., 7., 5.]])
>>> a.ravel()   # returns the array, flattened
array([5., 9., 1., 9., 3., 4., 8., 4., 5., 0., 7., 5.])
>>> a.reshape(6,2)  # returns the array with a modified shape
array([[5., 9.],
       [1., 9.],
       [3., 4.],
       [8., 4.],
       [5., 0.],
       [7., 5.]])
>>> a.T     # returns the array, transposed
array([[5., 3., 5.],
       [9., 4., 0.],
       [1., 8., 7.],
       [9., 4., 5.]])
>>> a.T.shape
(4, 3)
>>> a.shape
(3, 4)
>>> a.resize(2,6)   # modifies the array itself
>>> a
array([[5., 9., 1., 9., 3., 4.],
       [8., 4., 5., 0., 7., 5.]])
>>> a.reshape(3,-1)     # -1 means automatically calculated
array([[5., 9., 1., 9.],
       [3., 4., 8., 4.],
       [5., 0., 7., 5.]])
```

### 重组数组

几个数组可以堆叠重组到一起。

```python
>>> a = np.floor(10*rg.random((2,2)))
>>> b = np.floor(10*rg.random((2,2)))
>>> a
array([[0., 5.],
       [4., 0.]])
>>> b
array([[6., 8.],
       [5., 2.]])
>>> np.vstack((a,b))
array([[0., 5.],
       [4., 0.],
       [6., 8.],
       [5., 2.]])
>>> np.hstack((a,b))
array([[0., 5., 6., 8.],
       [4., 0., 5., 2.]])
```

如果维度不同，堆叠效果不同。

```python
>>> from numpy import newaxis
>>> np.column_stack((a,b)) # with 2D arrays
array([[9., 7., 1., 9.],
[5., 2., 5., 1.]])
>>> a = np.array([4.,2.])
>>> b = np.array([3.,8.])
>>> np.column_stack((a,b)) # returns a 2D array
array([[4., 3.],
[2., 8.]])
>>> np.hstack((a,b)) # the result is different
array([4., 2., 3., 8.])
>>> a[:,newaxis] # view `a` as a 2D column vector
array([[4.],
[2.]])
>>> np.column_stack((a[:,newaxis],b[:,newaxis]))
array([[4., 3.],
[2., 8.]])
>>> np.hstack((a[:,newaxis],b[:,newaxis])) # the result is the same
array([[4., 3.],
[2., 8.]])
```

```python
>>> np.column_stack is np.hstack
False
>>> np.row_stack is np.vstack
True
```

### 分割数组

```python
>>> a = np.floor(10*rg.random((2,12)))
>>> 
>>> a
array([[3., 7., 3., 4., 1., 4., 2., 2., 7., 2., 4., 9.],
       [9., 7., 5., 2., 1., 9., 5., 1., 6., 7., 6., 9.]])
>>> np.hsplit(a, 3)
[array([[3., 7., 3., 4.],
       [9., 7., 5., 2.]]),
array([[1., 4., 2., 2.],
       [1., 9., 5., 1.]]), 
array([[7., 2., 4., 9.],
       [6., 7., 6., 9.]])]
>>> np.hsplit(a, (3,4))
[array([[3., 7., 3.],
       [9., 7., 5.]]),
array([[4.],
       [2.]]), 
array([[1., 4., 2., 2., 7., 2., 4., 9.],
       [1., 9., 5., 1., 6., 7., 6., 9.]])]
```

## 拷贝和视图

拷贝和视图 (Copies and Views) 也就是深拷贝和浅拷贝问题。

```python
>>> a = np.array([0, 1, 2, 3])
>>> a
array([0, 1, 2, 3])
>>> b = a   # no new object is created 
>>> b is a  # a and b are two names for the same ndarray object
True
b = a   
```

浅拷贝/视图数组与原数组**共享相同数据**，view 函数会创建一个新的数组对象。

```python
>>> c = a.view()    # c is a view of the data owned by a
>>> c is a
False
>>> c.base is a
True
>>> c.flags.owndata
False
>>> c = c.reshape((2, 2))
>>> a.shape     # a's shape doesn't change 
(4,)
>>> c
array([[0, 1],
       [2, 3]])
>>> c[1, 1] = 1000  # a's data changes
>>> a
array([   0,    1,    2, 1000])
>>> a[0:2]  
array([0, 1])
>>> a[0:2] = 10     # Slicing an array returns a view of it:
>>> a
array([  10,   10,    2, 1000])
```

深拷贝将会完全拷贝数组对象以及数据区。

```python
>>> d = a.copy()
>>> d
array([  10,   10,    2, 1000])
>>> d is a
False
>>> d.base is a
False
>>> d[0] = 5
>>> a
array([  10,   10,    2, 1000])
>>> b = a[1:3].copy()
>>> del a   # the memory of a can be released.
```

## API 总结

TODO

# 进阶技巧

TODO

## 广播 (Broadcasting)

## 数组创建 (Creation)

## 索引 (Advanced Indexing)

TODO

### 索引数组索引

### 布尔数组索引

### 字符串索引

## I/O

## 结构体数组 (Structured arrays)

# 例程 (Routines)

在官方例程中 [NumPy Routines](https://numpy.org/doc/1.19/reference/routines.html) 包含了众多功能和用法。主要有：

- Binary operations
- String operations
- Datetime Support Functions
- DFT
- Financial functions
- Linear algebra (numpy.linalg)
- Logic functions
- Mathematical functions
- Matrix library (numpy.matlib)
- Random sampling (numpy.random)
- Sorting, searching, and counting
- Statistics

其中常用的重要部分分类写出。

## 数学运算

在基本运算和通用函数章节，我们以及介绍了一些数学运算符和函数，本章根据数学运算分类总结 NumPy 中的相关内容。

TODO

# 参考

- [User Guide](https://numpy.org/doc/stable/numpy-user.pdf)
