## 指令和可执行文件 (Executable)

你是否在 Linux 上编译过代码? 它的输出是一个二进制文件, 在这里我们称之为程序 (Binary) 或可执行文件 (Executable). 你可以通过在终端中输入程序的名称来运行它. 例如, 如果你编译了一个名为 `hello` 的程序, 你可以通过输入 `./hello` 来运行它.

```bash
$ g++ hello.cpp -o hello
$ ls
hello.cpp hello
$ ./hello
Hello, World!
```

---

事实上: 在 Linux 中, 许多常用的命令行工具 (如 `ls`, `cat`, `echo` 等) 都是可执行文件. 你可以通过 `which` 命令来查看它们的路径:

```bash
$ which cat
/usr/bin/cat
```

于是, 你也可以通过输入完整路径来运行它们: `/usr/bin/cat file` 和直接输入 `cat file` 是一样的.


> 还有一个指令 `whereis`. 它会搜索更多的路径, 并返回一系列 "可能有用" 的相关文件. 这当你希望寻找多版本指令 (比如 `python3` ) 的时候特别有用.

---

# PATH 环境变量

于是, 你满怀期待地输入 `hello` 来运行你的程序, 但是 shell 却告诉你 `command not found`. 这是为什么呢?

在 Linux 中, 当你输入一个命令时, shell 会在一系列预定义的目录中查找该命令对应的可执行文件. 这些目录存储在一个名为 `PATH` 的环境变量中. 你可以通过以下命令查看当前的 `PATH`:

```bash
echo $PATH
```

> PATH 前的 `$` 符号表示你想要获取该变量的值. 在 Linux 中, 你可以用 `VAR=value` 来设置变量, 用 `$VAR` 来获取变量的值.

---

如果你的程序所在的目录不在 `PATH` 中, shell 就找不到它, 因此会提示 `command not found`. 你可以通过修改 `PATH` 来解决这个问题.

```bash
export PATH=/path/to/your/program:$PATH
```

关于环境变量, 我们会在本章的最后一个挑战中做更详细的介绍.