Linux 是一个多用户系统, 这意味着它内置了一套规则来防止文件被不该访问或修改的人读取或改动. 本课将帮助你理解并控制这些规则. 

---

## 用户和用户组

在 Linux 中, 一切都归属于某个用户. 每个文件、每个进程（正在运行的程序）都关联到一个特定的用户账户, 系统据此“记账”. 

**用户** (user)：一个独立的账户. 当你登录时, 你是以特定用户的身份行动. 最强大的用户称为 root（或超级用户）, 它对整个系统拥有几乎不受限制的访问能力. 

**用户组** (group)：用户的集合. 用户组使得同时管理多个用户的权限变得容易. 一个常见例子是用于网页服务的 www-data 组, 倘若你host过网站的话你会听说过这一点, 你不希望每个普通用户都能改网站文件；同样, 你也不希望像 Nginx、Caddy 这样的网页服务器进程能访问你的私人文件. [这篇文章很好地解释了这点](https://askubuntu.com/questions/873839/what-is-the-www-data-user). 

你可以使用 whoami 命令查看你是谁. 

```bash
whoami
```

---

## `rwx` 权限

在之前的课程中, 你已经学习了 `ls -la` 命令, 其中 `-l` 参数显示文件的详细信息, 包括它们的权限. 你可能看到像这样的内容：

```bash
total 96
drwxr-x--- 119 theunknownthing  staff   3.7K Sep 15 16:09 ..
drwxr-xr-x   8 theunknownthing  staff   256B Sep 15 16:00 contents
drwxr-xr-x  15 theunknownthing  staff   480B Sep 15 15:59 .git
-rw-r--r--   1 theunknownthing  staff   1.1K Sep  9 20:58 README.md
...
```

看到 `drwxr-xr-x` 部分了吗？这就是显示权限的地方. 

---

让我首先解释这些字符的含义. 有三种基本权限：

- 读取 (r)：查看文件内容或列出目录内容的能力. 

- 写入 (w)：更改或删除文件, 或在目录内创建/删除文件的能力. 

- 执行 (x)：运行文件（如果它是程序或脚本）或进入目录（`cd` 进入）的能力. 

第一个字符表示文件类型：`d` 表示目录, `-` 表示普通文件, `l` 表示符号链接, 以及其他字符表示特殊文件类型. 

所以, 在 `drwxr-xr-x  15 theunknownthing  staff   480B Sep 15 15:59 .git` 中：

- `d` 表示这是一个目录. 
- 然后你可以看到恰好 9 个字符, 分为三组, 每组三个. 

  前 3 个字符 (`rwx`) 是**所有者**的权限. 这里, `rwx` 意味着**所有者**可以读取、写入和执行. 此文件的所有者是 `theunknownthing`. 

  中间 3 个字符 (`r-x`) 是**用户组**的权限. 这里, `r-x` 意味着**用户组**可以读取和执行, 但不能写入. 此文件的用户组是 `staff`. 

  最后 3 个字符 (`r-x`) 是其他人（其余所有人）的权限. 同样, `r-x` 意味着他们可以读取和执行, 但不能写入. 

---

为了加深理解, 让我们看另一个例子：`-rw-r--r--   1 theunknownthing  staff   1.1K Sep  9 20:58 README.md`

在看下一页的答案之前, 请先自己解读一下. 思考：

- 这是什么类型的文件？
- 所有者拥有什么权限？为什么所有者没有执行权限？
- 用户组拥有什么权限？
- 其他人拥有什么权限？

---

第一个字符是 `-`, 表示这是一个普通文件. 

所有者拥有 `rw-` 权限, 意味着他们可以读取和写入文件, 但不能执行它（这很明显, 因为它是一个Markdown文本, 你不能运行它）. 

> Tips：并非所有文本文件都“不能执行”, 而是“默认没有执行位”. 若它是脚本并设置了执行位且有正确的 shebang（例如 #!/usr/bin/env bash）, 可直接执行；即使没有执行位, 也可用解释器显式运行, 例如 bash script.sh 需要脚本具备读权限. 了解 shebang, 请参阅[这里](https://en.wikipedia.org/wiki/Shebang_(Unix)). 不过, 我不要求你现在掌握它. 

用户组拥有 `r--` 权限, 意味着 `staff` 组中的用户可以查看文件内容, 但不能修改或执行它. 

其他人也拥有 `r--` 权限, 意味着他们也只能读取文件. 

---

## 使用 `chmod` 更改权限

chmod（change mode）命令用于更改文件的权限. 你可以通过两种常见方式来做这件事：**符号表示法**或**八进制表示法**. 

我们首先学习符号表示法, 这种方式更直观. 

这种方法使用字母（`u` 表示 user（所有者）, `g` 表示 group, `o` 表示 others, `a` 表示 all）和符号（+ 添加, - 删除, = 设置）来修改权限. 

```bash
# 为owner添加执行权限
chmod u+x script.sh

# 设置others的权限为只读
chmod o=r README.md

# 移除除owner外所有人的读取权限, 这里 `go` 表示 `g` 和 `o`
chmod go-r README.md

# 移除groups的所有权限
chmod g= script.sh
```

---

## 八进制表示法

这种方法使用数字来表示每个类别的权限. 这有点像二进制! `r = 4, w = 2, x = 1`. 你可以将想要的权限对应的数字相加. 

| 数字 | 权限 | 含义                |
| ---- | ---- | ------------------- |
| 7    | rwx  | 读、写和执行, 4+2+1 |
| 6    | rw-  | 读和写, 2+4         |
| 5    | r-x  | 读和执行, 4+1       |
| 4    | r--  | 只读, 4             |
| 0    | ---  | 无权限, 0           |

使用八进制表示法的 `chmod` 命令使用一个 3 位数字, 分别代表用户、组和其他人的权限（按此顺序）. 要设置权限为 rwxr-xr-x（用户可以做任何事；组和其他人可以读取和执行）, 你将使用数字 755. 

```bash
chmod 755 script.sh
```

这将为所有者设置 7（rwx）, 为组设置 5（r-x）, 为其他人设置 5（r-x）. 

---

## 使用 `sudo` 获取超级用户权限

当你需要执行一些你的普通用户账户无权执行的操作时, 例如安装软件或编辑系统配置文件, 会发生什么？

```bash
apt update
```

你会得到错误：

```bash
Reading package lists... Done
E: Could not open lock file /var/lib/apt/lists/lock - open (13: Permission denied)
E: Unable to lock directory /var/lib/apt/lists/
W: Problem unlinking the file /var/cache/apt/pkgcache.bin - RemoveCaches (13: Permission denied)
W: Problem unlinking the file /var/cache/apt/srcpkgcache.bin - RemoveCaches (13: Permission denied)
```

为此, 你需要管理员权限. sudo 命令让你以超级用户（root）身份执行**单个命令**. 

```bash
sudo apt update
```

> 🈲 root 用户可以做任何事, 包括意外删除你的整个系统. 在使用 sudo 运行任何命令前请仔细检查. 你可能见过一些梗图让你执行 `sudo rm -rf /*`. 别做! 我不会来帮你恢复系统的! 

---

如果你想亲自登录 root 用户, 可以使用 `su` 命令（substitute user, 替换用户）. 
```bash
sudo su
```

这相当于用 sudo 以提权方式运行 `su`；在不带参数时, `su` 默认切到 root. 

> Tips: 直接运行 su（不带 sudo）默认会询问“目标用户的密码”（通常是 root 的密码）. 在 Ubuntu 上, root 账户默认可能被锁定, 此时 su 不可用, 但 sudo su 会要求你输入当前用户的密码（前提是你在 sudoers 中）. 

当然, `su` 不仅限于切换到 root. 如果你知道其密码, 你可以切换到任何用户. 

```bash
su some_username
```

如果你知道他们的密码, 或者如果你当前的用户拥有比该用户更高的权限, 这将切换到 `some_username`. 所以从 root 切换到任何用户不需要该用户的密码. 