
在 Linux 中, “一切皆文件”的哲学意味着命令的输入和输出被视为可以重定向的流. 这一强大的概念使你能控制命令从哪里获取输入, 以及将输出发送到哪里. 

让我用清晰的示例来告诉你探索重定向的工作原理. 

---

## 输出重定向 (>)

`>` 符号将标准输出重定向到文件. 输出**不会显示在屏幕上**, **而是保存到文件中**. 

> 还记得 `pwd` 命令吗？它显示当前目录. 

```bash
pwd                    # 在屏幕上显示当前目录
pwd > my_location.txt  # 将输出保存到文件
cat my_location.txt    # 查看文件内容
```

> ⚠️ **警告**: 使用 `>` 会覆盖任何现有的文件内容！请小心. 

---

## 追加输出 (>>)

要向文件中添加内容而不覆盖它, 请使用 `>>`: 

```bash
echo "First Line" > notes.txt      # 创建/覆盖文件
echo "Second Line" >> notes.txt    # 向文件添加新行
cat notes.txt                      # 显示两行内容
```

> 思考: 上方 `notes.txt` 文件中现在有几行？是什么？答案是两行, 分别是 "First Line" 和 "Second Line". 

---

## 输入重定向 (<)

就像可以将输出重定向到文件一样, 你也可以使用文件作为命令的输入, 还是拿上面我们已经创建的 `notes.txt` 文件为例: 

```bash
# 使用该文件作为 cat 命令的输入
cat < notes.txt
```

这个命令会显示 `notes.txt` 的内容, 就像直接运行 `cat notes.txt` 一样. 

---

## 理解流类型

这一个章节我们**不作要求**, 但是了解这些内容会帮助你更好地理解重定向. 也会让你的代码 debug 过程更轻松. 

Linux 有三个标准流: 
- 标准输入 (stdin) - 流描述符 0
- 标准输出 (stdout) - 流描述符 1
- 标准错误 (stderr) - 流描述符 2

你们可能还没有听说过这三个流, 但是你们事实上肯定已经在使用 `stdin` 和 `stdout` 了. `cin` 就是从 `stdin` 读取输入, 而 `cout` 则将输出发送到 `stdout`. 更多关于流的知识, 请期待翁阿姨这个学期讲解输入输出的内容. 

你可以分别重定向每个流: 

```bash
# 仅重定向标准输出
ls -l > file_list.txt

# 仅重定向 stderr 消息
./bookstore 2> errors.txt

# 将标准输出和错误消息分别重定向到不同的文件
./bookstore > output.txt 2> errors.txt
```

---

## 高级重定向

**这一章节我们也不作要求. **

要将标准输出和错误同时重定向到同一个文件, 可以使用 `2>&1`: 

```bash
./bookstore > combined.txt 2>&1
```

你可能在想 “这都是啥？” 2>&1 的意思是: 把 `stderr` 重定向到 `stdout` 的位置, 然后 `stdout` 再被重定向到 `combined.txt`. 所以最终两个流都会进入同一个文件. 

那你可能又会问 “上述命令为什么不写成这样: `./bookstore 2>&1 > combined.txt # 这样写不对！`”

顺序很重要! 上面错误的命令会先把 `stderr` 重定向到**当前的** `stdout`（通常是屏幕）, 然后再把 `stdout` 重定向到文件. 所以最终 `stderr` 仍然会显示在屏幕上, 而不是进入文件. 所以说应当先重定向 `stdout` 到文件, 然后再把 `stderr` 重定向到 `stdout`. 事实上, 现代的 Bash 版本允许你使用更简洁的 `&>` 来实现同样的效果: 

```bash
./bookstore &> combined.txt
```

---

## 重定向到 /dev/null

当你想完全丢弃输出时, 可以重定向到 null: 

```bash
# 丢弃 stderr 输出
./bookstore 2> /dev/null

# 丢弃所有输出
./bookstore &> /dev/null
```
