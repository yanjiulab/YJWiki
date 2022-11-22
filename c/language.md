# 语言特性

## 程序结构

C 是一种面向过程的结构化编程语言，Pascal 之父说程序=算法+数据结构，在 C 语言中，程序可以看成由一系列的外部对象构成，外部对象包括：

- 外部变量：在函数外面定义的变量，可以被多个函数使用。
- 函数：由于 C 语言不允许在函数中定义函数，因此函数本身就是外部的。

默认情况下，外部变量和函数拥有如下性质：通过同一个名字对外部变量的所有引用，实际上都是引用同一个对象。也称为外部链接性质。

### 作用域规则

名字的作用域是指：程序中可以使用该名字的区域。

外部变量和函数的作用域为：

- 从声明处开始
- 到其所在的待编译文件末尾结束。

函数内部的变量是该函数的私有变量，或者称之为局部变量，其作用域为该函数。

### 外部变量

外部变量可以在全局范围内访问，因此外部变量可以作为函数之间交互的桥梁，可以简化函数参数表设计。但需要注意这种方式不能被滥用，因为这导致各个函数具有太多数据关联。

外部变量的声明与定义是完全不同的：

- 变量声明用于说明变量的属性（主要是类型）
- 变量定义除此之外将会引起存储器的内存分配。

外部变量定义如下，这两条语句将会引起存储分配，并且可作为该源文件中其余部分的声明。 

```c
int sp;
double val[MAXVAL];
```

外部变量声明如下，如果要在外部变量定义前就使用该文件，或者变量的使用和定义不在同一个源文件中，则必须使用 `extern` 关键字。 

```c
extern int sp;
extern double val[];
```

在一个源程序的所有文件中，**外部变量只能在某个文件中被定义一次**，而其他文件通过 `extern` 声明来访问它（定义该变量的文件也可以包含该变量的 `extern` 声明）。

外部变量的初始化只能出现在定义中，未初始化的外部变量默认值为 0。

### 局部变量

与外部变量相对的，局部变量是在函数内定义的变量，包括两种变量：

- 自动变量：仅在函数调用时存在，函数执行完毕退出时消失。大多数局部变量，通常都是自动变量。
- 静态局部变量：通过 `static` 关键字限制的局部变量，不随函数调用而存亡，而是一直存在。

### 静态变量

静态对象是指通过 `static` 限制的外部对象，包括静态变量和静态函数，其**作用域被限制在被编译源文件中**。通过 `static` 限制对象可以达到隐藏外部对象的目的。

静态变量/静态函数与外部变量/函数类似，但名字仅能在当前源文件访问，不会污染全局命名空间，通过静态变量或静态函数，将调用者不关心的外部对象隐藏到文件内部，可以达到模块化编程的效果。

局部变量也可以用 `static` 关键字修饰，其效果是：该变量只能在某个特定函数中使用，但却一直占据存储空间，不随函数的调用退出而产生消失。 

### 变量类型总结

各种类型的变量对比如下。

|     变量类型      | 定义位置 | 声明修饰符 | 初始值 |   作用域   |     生存期     |
| :---------------: | :------: | :--------: | :----: | :--------: | :------------: |
| 外部变量/全局变量 | 函数外部 |  `extern`  |   0    |    全局    |    一直存在    |
|     静态变量      | 函数外部 |  `static`  |   0    | 所在源文件 |    一直存在    |
|     自动变量      | 函数内部 |     无     |  随机  |  所在函数  | 随函数调用存亡 |
|   静态局部变量    | 函数内部 |  `static`  |   0    |  所在函数  |    一直存在    |

### 头文件组织

对于许多高级程序语言来说，整个程序范围太大，而函数范围太小，因此使用模块或包的概念表示一类变量和函数的集合，从而便于组织程序架构。例如 Java 中的类和包，Python 中的模块和包等概念。 

然而，C 语言并没有这些概念，并且由于 C 支持分离编译，程序员可以将一个程序的各个部分分散到不同的源文件中编译，然后链接到一起。这使得编写大型程序更加难以控制，借助于 `static` 静态对象机制，可以实现基于文件的模块化编程，但是当某个源文件内容过多时，又会使得开发不便。

因此，C 语言并没有一种万能的模块化编程范式，程序架构的依赖于开发者控制，需要开发者精心的组织头文件。一般而言，可以按照如下方式组织头文件：

- 对于中等规模的程序：最好只用一个头文件存放程序中各部分共享的对象。
- 较大规模的程序：每个 `.c` 文件对应一个 `.h` 文件，每一对作为一个逻辑上的模块对内对外提供接口。

## 基本数据类型

C 语言标准层面没有明确定义基本数据类型的大小，只能确定 `sizeof(char) <= sizeof(short) <= sizeof(int) <= sizeof(long) <= sizeof(long long)`。具体某种类型的大小与编译器和系统有关，具体来说和实现采用的**数据模型**有关，

![image-20221110174548349](language.assets/image-20221110174548349.png)

对于目前 64 位操作系统而言，以下两种模型使用广泛：
- **LLP64**: Microsoft Windows (x86-64 and IA-64) using Visual C++; and MinGW
- **LP64**: Most Unix and Unix-like systems, e.g., Solaris, Linux, BSD, macOS. Windows when using Cygwin; z/OS

使用代码测试一下，本机为 Linux：

```
#include <stdio.h>

int main()
{
    printf("char: %ld, short: %ld, int: %ld, long: %ld, long long: %ld, void *: %ld\n",
        sizeof(char), sizeof(short), sizeof(int), sizeof(long), sizeof(long long), sizeof(void *));
    return 0;
}
// output:
// char: 1, short: 2, int: 4, long: 8, long long: 8, void *: 8
```

>  当数据类型的位数重要时,请使用 `stdint.h` 中定义的固定长度类型 (fixed-size types)，例如 `int8_t`、`uint32_t` 等，或使用 `sizeof()` 计算位数。

## 函数

函数封装了程序的实现细节，通过函数调用，代码更加易用清晰。

C 语言中所有函数参数都是通过**值传递**的。传递给被调用函数的参数值存放在临时变量中，而不是存放于原来的变量。

需要注意，值传递与能否改变原始参数的值是无关的，因此，在 C 语言中：

- 一般变量参数：不能修改原始参数值，只能修改该变量临时创建的私有副本的值。

- 指针变量参数：通过变量的地址，间接修改原始参数值。指针本身仍然会复制。

- 数组参数：数组名作参数，实际传递的是数组起始元素地址，效果等同指针变量，数组本身不会被复制。

## C 预处理器

文件包含

```c
#include <filename>
#include "filename"
```

宏定义

```c
#define IDENTIFIER TEXT
#define IDENTIFIER(OPT) TEXT
#undef IDENTIFIER
```

条件编译

TODO

OS 特定编译功能

TODO

## 数组

### 数组初始化
1. **局部**数组未初始化时，其值为随机值。
2. **全局**或**静态**数组未初始化时，其值为 `NUL` 或 0。

应当养成每次都初始化数组的好习惯。当**数组初始化之后，会将未初始化的位置设置为 `NUL` 或 0**，利用这个规则，我们可以通过初始化数组第一个元素从而快速将数组初始化为 0 或 `NUL`。

通过代码，验证上述结论。

```c
#include <stdio.h>
#include <string.h>

void dump_int(int* str);
void dump_char(char* str);

int arr_g[5];

int main()
{
    static int arr_s[5];
    int arr1[5];
    int arr2[5] = { 0 };
    char arr3[5];
    char arr4[5] = "abc";

    dump_int(arr_g); //(int) 0 0 0 0 0
    dump_int(arr_s); //(int) 0 0 0 0 0
    dump_int(arr1); // (int)  0 0 1346658496 21995 407207840
    dump_int(arr2); // (int)  0 0 0 0 0
    dump_char(arr3); // (char)  NUL NUL -32 -124 t
    dump_char(arr4); // (char) a b c NUL NUL
    
    return 0;
}

void dump_int(int* str)
{
    printf("(int) ");
    for (int n = 0; n < 5; ++n) {
        printf("%d ", *(str + n));
    }
    printf("\n");
}

void dump_char(char* str)
{
    printf("(char) ");
    for (int n = 0; n < 5; ++n) {
        if (str[n] < 0 || str[n] > 127) {
            printf("%d ", str[n]);
        } else if (str[n] == 0) {
            printf("NUL ");
        } else {
            printf("%c ", str[n]);
        }
    }
    printf("\n");
}
```

### 多维数组

TODO

## 指针

### 指针与地址

我们知道，数据（例如数字 47）是存储在内存中的某个位置的，这个位置在内存中有一个地址（例如 `0x7fff0bfb602c`），然而这个名称对人类是不友好的，因此程序员使用变量（例如 `i`）来表示数据。也就是说，变量名和这个内存地址实际上是一回事，变量名通过**取址运算符 `＆` **便可以得到该内存地址。

```
int i = 47
&i == 0x7fff0bfb602c
```

指针是一种保存变量地址的变量。也就是说，指针变量的值（简称为指针）就是另一个变量的内存地址。指针的定义如下：

```c
int i = 47;
int *p = &i;
```

这并没有什么稀奇的，真正赋予 C 语言指针威力的是**解引用符 (dereference) `*`**，在该符号的帮助下，我们可以通过指针（内存地址）来取得那一小块内存的读写权限！，这是一项非常强大，同时也非常底层、非常容易导致混乱的功能。

```c
int i = 47;
int *p = &i;
printf("%d", *p);	// read
*p = 32;	// write
```

指针声明写为 `int* p` 、`int *p` 以及 `int * p`  都可以。但指针必须指向某种类型的数据，甚至 `void` 也是允许的，表示可以存放任意数据类型的指针，通常可以作为接口使用。但这种指针不能通过解引用获取变量值，必须先进行类型转换之后才可以解引用。

```c
void *p = &i;
printf("%d\n", *p);	// compile error
printf("%d\n", *(int *)p);	// ok, but need type conversion
```

需要注意，指针变量存储的地址通常由取址运算符得到，因为内存地址是一个非常“底层”的参数，与用户代码无关。但是将任意值赋值给指针变量是允许的（会发生类型转换），在这种情况下，通过解引用符号获取该内存地址的数据可能会得到“垃圾数据”，甚至几乎一定会由于地址不合法而引发段错误。其中原因涉及虚拟内存，不再详细说明。

指针可以进行加减运算（`++`、`--`、`+`、`-`），其加减的**单位为指向数据类型的大小**。取址运算符和解引用运算符优先级高于算术运算符，但从右向左结合。例如 `*p += 1` == `++*p` == `(*p)++` != `*p++`，如果不清楚优先级，加括号是最好的方式！

```c
int i = 47;
int* p = &i;
printf("%p\n", p);      // 0x7ffd5f7e8c2c
printf("%p\n", ++p);    // 0x7ffd5f7e8c30 
```

由于指针也是变量，因此可以赋值为另一个指针变量，此时两个指针变量的值相同，指向同一个变量。

因此，关于指针：

- **总是将指针初始化为 NULL 是一个好习惯**！
- 指针可以进行加减运算（`++`、`--`、`+`、`-`），其加减的**单位为指向数据类型的大小**。
- 指针与普通类型一样也可以存储在数组中，成为指针数组。
- 指针与普通类型一样也可以被另一个指针指向，构成**多级指针**。

### 指针与函数

指针可以作为函数的参数或者返回值。

- 指针可以作为参数传给函数，可以在调用函数时改变该实参的值。
- 指针可以作为函数返回值，**一般用于动态内存分配**时返回该堆指针，需要注意若该指针指向局部变量，则在函数退出时，该变量也不复存在，因此 `*p` 会得到“垃圾数据”。

### 指针与数组

```c
int arr[3] = { 0 };
int* pa = arr;
printf("%p\n", arr);    // 0x7fffd8f6e6d0
printf("%p\n", &arr);   // 0x7fffd8f6e6d0
printf("%p\n", pa);     // 0x7fffd8f6e6d0
printf("%p\n", &pa);    // 0x7fffd8f6e6c8
```



## 字符串

### 存储方式
C 语言使用**字符数组**来表示字符串，字符数组和字符串之间的区别在于**字符串以特殊字符 `\0 (NUL)` 结尾**。
```c
char array[5] = {'h', 'e', 'l', 'l', 'o'};
char str[6] = "hello";
char str1[6] = {'h', 'e', 'l', 'l', 'o', '\0'}; // equivalent to str
```

**字符指针**在某种程度上也可以表示字符串，这并不惊讶，因为字符数组名本身就是一个常指针。

`char* str1` 和 `char str2[]` 都可以表示字符串，然而两者具有很大区别：

- `str1` 是一个指向 char 变量的指针变量，指向一个字符串常量（其位于常量区），指针变量的值可以改变，而字符串常量的值不能改变。
- `str2` 是一个指针常量，指向一个字符数组，指针常量值不可改变，但数组内容可以改变。

```c
int main()
{
    char* str1 = "hello";
    char str2[10] = "world";
    printf("str1: %s\n", str1); // hello
    printf("str2: %s\n", str2); // world

    //str1[0] = 'W'; // Segment Fault
    str2[0] = 'W'; // OK
    printf("str2: %s\n", str2); // World

    str1 = "hello c language"; // OK
    printf("str1: %s\n", str1); // hello c language
    str1 = str2; // OK
    printf("str1: %s\n", str1); // World
    //str2 = "hello"; // Error，expression must be a modifiable lvalue

    return 0;
}
```

同样，`str1` 和 `str2` 位于不同的内存区。显然，`str2` 位于栈，而 `str1` 同全局变量、堆内存一样位于堆中。 
```c
char str[10] = "C"; // address: 0x55a607eb1010
int main()
{
    char* str1 = "hello";   // address: 0x55a607eaf004
    char str2[10] = "world";  // address: 0x7ffc2940e042
    char* str3 = (char*) malloc(10); // address: 0x55a609b752a0
}
```

### string.h 头文件
通常字符串函数都位于 `string.h` 头文件中。该头文件引入了以下内容：
- 一个变量：`size_t` 表示无符号整数
- 一个宏：`NULL` 表示空字符串常量
- 若干函数：主要可以分为两类：
    1. 以 `mem` 开头的操作内存字节的函数
    2. 以 `str` 开头的操作字符的函数

| 函数名                 | 作用                                                         |
| ---------------------- | ------------------------------------------------------------ |
| `strlen(str)`          | 计算 str 长度，不包括 NUL 字符。                             |
| `strcat(dst, src)`     | 将 src 加到 dst 后面。                                       |
| `strcmp(fir, sec)`     | 相同为 0，否则返回第一个不匹配字符的 ASCII 值的差，即 fir - sec。 |
| `strcpy(dst, src)`     | 将 src 拷贝到 dst，遇到 NUL 字符停止。                       |
| `strncpy(dst, src, n)` | 将 src 的 n 字节拷贝到 dst。<br>如果 src 的前 n 字节不包括 NUL 字符，则 dst 将不会有 NUL 结束符！<br>如果 src 不足 n 字节，则剩余空间使用 NUL 字符补齐。 |
| `memcpy(dst, src, n)`  | 将 src 的 n 字节拷贝到 dst。                                 |
| `memset(s, c, n)`      | 将 s 的 n 字节设为 c。                                       |

具有相同后缀的两种函数功能相似，但稍有不同。其中 `mem` 系列函数将字符序列视为字节操作，而 `str` 系列函数将字符序列视为字符串操作。逻辑上而言 `mem` 系列表达的语义更加底层。

### 字符串拷贝
以 `memcpy` vs `strcpy` 作为例子。

```c
#include <stdio.h>
#include <string.h>

void dump(char* str);

int main()
{
    char s[5] = { 's', 'a', '\0', 'c', 'h' };

    char membuff[5] = { 0 };
    char strbuff[5] = { 0 };

    strcpy(strbuff, s);
    memcpy(membuff, s, 5);

    dump(membuff); // 73 61 00 63 68  sa ch
    dump(strbuff); // 73 61 00 00 00  sa

    return 0;
}

void dump(char* str)
{
    char* p = str;
    for (int n = 0; n < 5; ++n) {
        printf("%2.2x ", *p);
        ++p;
    }
    printf("\t");
    p = str;
    for (int n = 0; n < 5; ++n) {
        printf("%c", *p ? *p : ' ');
        ++p;
    }
    printf("\n");
}
```

在网络编程时，应当使用 `memcpy` 拷贝数据。

### 字符串格式化
除了 `memcpy` 和 `strcpy` 以及其系列函数外，`sprintf` 函数也常用于字符串拷贝，但该函数操作的源对象不限于字符串，源对象可以是字符串、也可以是任意基本类型的数据。因此 `sprintf` 主要是实现将其他数据类型转换为字符串功能。同时，由于该函数属于 `printf` 家族函数，因此也可以完成字符串拼接效果。

```c
char path[100];
sprintf(path, "/proc/%d/uid_map", pid);
```

## 结构体

### 内存布局与字节对齐
结构体字节对齐的细节和具体的编译器实现相关，但一般来说遵循 3 个准则：
- 结构体变量的首地址能够被其最宽基本类型成员的大小(sizeof)所整除。
- 结构体每个成员相对结构体首地址的偏移量 offset 都是成员大小的整数倍，如有需要编译器会在成员之间加上填充字节。
- 结构体的总大小 sizeof 为结构体最宽基本成员大小的整数倍，如有需要编译器会在最末一个成员之后加上填充字节。

直接使用 `pragma pack` 预处理宏可以改变结构体的字节对齐方式：
- `#pragma pack(n)`：结构体将按照 n 个字节对齐，其取值为 1、2、4、8、16，默认是 8。
- `#pragma pack(1)`：结构体没有填充字节，实现空间“无缝存储”，这对跨平台传输数据来说是友好和兼容的。

如果只想改变个别结构体的字节对齐方式，可以使用 GCC 编译器指定结构体**类型属性 (Type Attribute)** 为 packed，即： `__attribute__((__packed__))`。

```c
struct padding {
    char c; //1
    short s; //2
    int i; //4
    double d; //8
};
// sizeof() is 16

struct nopadding {
    char c; //1
    short s; //2
    int i; //4
    double d; //8
} __attribute__((__packed__));
// sizeof() is 15
```

`__attribute__` 必须紧挨着 struct 关键字或者结构体 `}` 之后，否则将会报错或不起作用。 

## I/O 处理



## 可变参数

`<stdarg.h>`

## 错误处理

`<error.h>`

## 动态内存分配

|                             函数                             |                             解释                             |
| :----------------------------------------------------------: | :----------------------------------------------------------: |
|   [malloc](https://en.cppreference.com/w/c/memory/malloc)    |                     分配内存 (function)                      |
|   [calloc](https://en.cppreference.com/w/c/memory/calloc)    |               分配内存并初始化为 0 (function)                |
|  [realloc](https://en.cppreference.com/w/c/memory/realloc)   | 扩展分配的内存块，如果制定的字节数小于原来的字节则保持不变；如果大于原来的字节树则新内容为定义。 |
|     [free](https://en.cppreference.com/w/c/memory/free)      |                释放先前分配的内容 (function)                 |
| [aligned_alloc](https://en.cppreference.com/w/c/memory/aligned_alloc)(C11) |                  分配对齐的内存 (function)                   |

简而言之， `malloc` 和 `calloc` 函数的主要区别有两点：

1. `malloc` 函数分配**给定字节数**的未初始化数组。
2. `calloc` 函数接收两个参数，分别为**数组个数**和**类型字节数**，并且将内存初始化为零。

在 [Difference between malloc and calloc?](https://stackoverflow.com/questions/1538420/difference-between-malloc-and-calloc) 中提到的 [Why does calloc exist?](https://vorpus.org/blog/why-does-calloc-exist/) 这篇博客详细解释了 `malloc` 和 `calloc` 函数的真正的不同点。简而言之，推荐使用 `calloc` 函数。

因此标准写法如下：

```c
int* ptr;	// declare ptr, int* for example
ptr = calloc(MAXELEMS, sizeof(*ptr));

// almost equivalent to the calloc() call above
ptr = malloc(MAXELEMS * sizeof(*ptr));
memset(ptr, 0, MAXELEMS * sizeof(*ptr));
```

## 日期和时间工具

`<time.h>`

## 地理位置支持

`<locale.h>`

## 其他

### const 关键字

指定变量不可被当前线程/进程改变（但有可能被系统或其他线程/进程改变）。

### volatile 关键字

指定变量的值有可能会被系统或其他进程/线程改变，强制编译器每次从内存中取得该变量的值。

## 参考

- https://en.cppreference.com/w/c

- [Is an array name a pointer?](https://stackoverflow.com/questions/1641957/is-an-array-name-a-pointer)
- [How do I understand complicated function declarations?](https://stackoverflow.com/questions/1448849/how-do-i-understand-complicated-function-declarations)