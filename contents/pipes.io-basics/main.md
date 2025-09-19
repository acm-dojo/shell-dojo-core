
在上一节中我们简要介绍了 shell 的命令行相关用法; 在上节首提到, shell 编程中的精髓有两点：一点是它奠定了脚本语言的基础，并实现了交互式命令；另一点就是管道(pipe)。

在本节中, 我们将会学习什么是管道.

---

管道的作用正如其名，就是将不同程序的输入和输出“连接”在一起，从而简化了许许多多重复繁杂的工作。

正如 Unix/Linux 哲学中反复强调的 Everything is a File, 输入和输出都是以文件的形式, 也就是某种 I/O 流的形式. 所以你可以选择任意连接不同程序的输入和输出, 比如我要将程序 A 的输出变成程序 B 的输入, 用管道的方式写出来就是 `A | B` 的形式. 我们可以理解为: 将 A 的输出实时复制到 B 的输入.

---

## cat

之前我们讲到了可以使用文本编辑器打开一个文件，并查看它的内容. 然而呢，如果仅仅只是要看一眼文件的内容，其实不必大动干戈，而且有很多命令可以帮我们完成这件事情.

打印文件内容，无非就是将文件输出到终端上；最常用的命令是 `cat`.

`cat` 不是猫, cat 是 `concatenate files and print on the standard output` 的缩写, 中文翻译 “将多个文件拼接并传到到标准输出”，不过暂时我们可以理解成 “将文件内容输出到屏幕上” (cast a file to screen).

你可以这么使用:

```
# 查看单个文件内容
cat file1.txt

# 拼接文件内容
cat file1.txt file2.txt > combined.txt
```

---

## grep

当文件较短的时候, 直接用 `cat` 就能看清楚文件内容了. 但是如果文件很长, 比如系统日志, 你可能就需要一些更高级的工具来帮你过滤和查找你想要的信息.

我们可以使用 `nano` 这种文本编辑器来打开文件, 然后用搜索功能查找关键词, 但是这种办法是交互式的，也就是说没有办法“自动化”. 所以我们就需要一个 “自动” 查询关键词的命令, 也就是命令 `grep`。

---

`grep` 的名字来源于上古时期的文本编辑器 `ed` 中的命令 `g/re/p` (globally search a regular expression and print). 所以它的工作就是查找匹配所有满足条件的行并把它们打印出来. 语法是先加待搜索的单词, 再跟上文件名，比如:

```bash
$ cat file.txt
Hello World!
Hello grep!
Hello cat!
$ grep "grep" file.txt
Hello grep!
```

---

`grep` 还有一些常用的选项, 比如:

```
# 查找文件中包含 "error" 的行
grep "error" logfile.txt

# 忽略大小写匹配
grep -i "error" logfile.txt

# 反向匹配：只显示不包含 "error" 的行 (在 log 排查的时候非常有用! 🎉)
grep -v "error" logfile.txt

# 搜索多个关键词 (用 | 分隔)
grep -E "error|fail" logfile.txt

# 显示行号 (-n 的位置无所谓)
grep -n "error" logfile.txt
```

其实 `grep` 本身与重定向没有太大的关系; 但是它能够起到的模式匹配与筛选作用是无可替代的. 它的作用等我们学习了重定向和管道之后, 就能发挥得淋漓尽致了.

> 在字符串搜索上, Shell 有个更加强大的工具 `awk` 和 `sed`, 但是使用方式比较复杂. 日常使用不妨使用 `python`. :P
