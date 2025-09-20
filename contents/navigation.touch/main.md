在上一个任务中, 你学习了如何在文件系统中导航. 从这个挑战开始, 你会学到如何对于文件系统作出改变.

---

## touch: 创建空文件

```
~ $ touch fish
touch: cannot touch 'fish': Permission denied
```

在 Linux 中, `touch` 命令用于创建空文件. 因此, `touch fish` 不是摸鱼, 而是在当前目录创建一个名为 `fish` 的空文件.

你可以用 `ls` 来验证文件是否创建成功.

```
~ $ ls
some-file
~ $ touch fish
~ $ ls
fish  some-file
```

---

## nano: 命令行中的文本编辑器

`touch` 很好, 但是除了在脚本中我们并不怎么用到它. 为什么呢? 因为我们创建文件通常是想在文件中写点东西, 而使用重定向等手段 (之后会讲到) 来写文件并不方便.

- 有没有什么软件可以在命令行中方便地编辑文本呢?

- 有的, 你可以使用 `nano`.

---

`nano` 是一款以命令行界面为基础的文本编辑器. 它非常轻量, 易于上手, 是 Linux 系统中最常见的文本编辑器之一. 你的 WSL 系统中也自带了 `nano`.

使用 `nano` 只需要在终端输入 `nano <filename>` 即可. 如果 `<filename>` 对应的文件不存在, `nano` 会自动帮你创建一个新文件.

---

`nano` 有不少快捷键; 你可以在屏幕的底部看到它们. `^` 代表 `Ctrl` 键. 常用操作有:

- `Ctrl + O`: 保存文件 (O 代表 Output)
- `Ctrl + X`: 退出 `nano` (X 代表 eXit)
