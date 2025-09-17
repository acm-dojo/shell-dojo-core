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
$ which ls
/usr/bin/ls
```

于是, 你也可以通过输入完整路径来运行它们: `/usr/bin/ls -a` 和直接输入 `ls -a` 是一样的.


> 还有一个指令 `whereis`. 它会搜索更多的路径, 并返回一系列 "可能有用" 的相关文件. 这当你希望寻找多版本指令 (比如 `python3` ) 的时候特别有用.

