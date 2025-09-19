这一关卡里, 我们大致谈一谈我们已经谈了三个关卡的管道.

---

先举个例子：

```
$ echo 'Hello World!' | cat
Hello world!
```

我们知道 cat 的作用是将文件重定向到标准输出（这里的 文件 可以是磁盘上的内容，也可以是 Unix/Linux 意义下各种设备被映射到的操作对象），但是这次 cat 之后没有跟着任何参数，所以 cat 是将什么内容重定向了呢？答案就是在管道符 | 前的 echo 'Hello World!' 命令里。

---

管道符的使用通常是这样的:

```
command_A | command_B
```

管道符将 command_A 的标准输出和标准错误 参考这里 定向到 command_B 的标准输入上（这句话似乎不能再通俗了）。考虑到 bash 里所有的变量都是字符串类型，于是利用这个语言特性可以很方便地将信息在命令间传递。

---

再举几个例子：

```
$ cat ~/.bashrc | less
# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples
```

作用是先将 ~/.bashrc 的内容输出到标准输出，然后由管道符定向到 less 的输入，于是就可以用 less 愉快地查看了。

---

下一个例子:

这里的 ps -A 是一个输出文件的指令, 现在我们用 grep 筛选一下文件中有关 pts 的字符:

```
$ ps -A | grep pts
 1793 pts/0    00:00:00 zsh
 1890 pts/1    00:01:16 hexo
 4170 pts/0    00:00:00 ps
 4171 pts/0    00:00:00 grep
 ```

上一篇介绍 grep 的时候我们是把目标文件（被匹配的文件）作为参数传给grep ，但是它其实也支持从标准输入读入目标内容啊！所以就可以用管道符把 ps -A 的结果传递给 grep.

管道的用法博大精深, 更多的用法就留给各位自己去探索了.
