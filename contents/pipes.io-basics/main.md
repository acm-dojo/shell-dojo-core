
在上一节中我们简要介绍了 shell 的命令行相关用法; 在上节首提到, shell 编程中的精髓有两点：一点是它奠定了脚本语言的基础，并实现了交互式命令；另一点就是管道(pipe)。

在本节中, 我们将会学习什么是管道.

---

管道的作用正如其名，就是将不同程序的输入和输出“连接”在一起，从而简化了许许多多重复繁杂的工作。

正如 Unix/Linux 哲学中反复强调的 Everything is a File, 输入和输出都是以文件的形式, 也就是某种 I/O 流的形式. 所以你可以选择任意连接不同程序的输入和输出, 比如我要将程序 A 的输出变成程序 B 的输入, 用管道的方式写出来就是 `A | B` 的形式.

---

比如之前我们讲到了可以使用文本编辑器打开一个文件，并查看它的内容。然而呢，如果仅仅只是要看一眼文件的内容，其实不必大动干戈，而且有很多命令可以帮我们完成这件事情。

打印文件内容，无非就是将文件输出到终端上；最常用的命令是 `cat`。

`cat` 不是猫, cat 是 `concatenate files and print on the standard output` 的缩写, 中文翻译\“输入输出重定向”，不过暂时我们可以理解成“将文件内容输出到屏幕上”(cast a file to screen).

你可以这么使用:

```
# 查看单个文件内容
cat file1.txt

# 拼接文件内容
cat file1.txt file2.txt > combined.txt

# 显示合并后的文件内容(-n : 加上行号)
cat -n combined.txt
```

---

再来举一个例子.

我们来说一些实际的事情。看过系统日志的同学们应该知道，那种日志……实在是太长了。如果我只想看特定的几种分类（指通过关键单词可以分类的情况），该怎么办呢？

首先做一些准备工作：

```
logic:~$ dmesg > syslog
logic:~$ less syslog
[    0.000000] microcode: CPU0 microcode updated early to revision 0x1b, date = 2014-05-29
[    0.000000] Initializing cgroup subsys cpuset
[    0.000000] Initializing cgroup subsys cpu
[    0.000000] Initializing cgroup subsys cpuacct
:
```

---

这个时候倒是可以先键入 / 然后再打要搜索的单词，比如 Bluetooth ：

```
[    4.419788] usb 3-1.3: Product: Bluetooth USB Host Controller
[    4.419790] usb 3-1.3: Manufacturer: Atheros Communications
[    4.419792] usb 3-1.3: SerialNumber: Alaska Day 2006
```

但是这种办法是交互式的，也就是说没有办法“自动化”。所以我们就需要一个“自动”的命令, 也就是命令 `grep`。

---

logic 的名字来源于上古时期的文本编辑器 ed 中的命令 g/re/p (globally search a regular expression and print)。所以它的工作就是查找匹配所有满足条件的行并把它们打印出来。语法是先加待搜索的单词，再跟上文件名，比如：

```
wang:~$ grep Bluetooth syslog 
[    4.419788] usb 3-1.3: Product: Bluetooth USB Host Controller
[   15.518235] Bluetooth: Core ver 2.20
[   15.518261] Bluetooth: HCI device and connection manager initialized
[   15.518266] Bluetooth: HCI socket layer initialized
...
```

---

简单来说, `grep` 命令用来从一堆文本中快速找到你想要的信息. 其格式是 `grep [选项] "关键词" 文件/目录`, 常见用法有:

```
# 查找文件中包含 "error" 的行
grep "error" logfile.txt

# 忽略大小写匹配
grep -i "error" logfile.txt

# 反向匹配：只显示不包含 "error" 的行
grep -v "error" logfile.txt

# 搜索多个关键词（用 | 分隔）
grep -E "error|fail" logfile.txt
```

其实 `grep` 本身与重定向没有太大的关系; 但是它能够起到的模式匹配与筛选作用是无可替代的.

---

现在, 你需要完成的任务是: