
在上一关卡中,你学会了如何利用 `pwd`, `ls` , `cd` 浏览文件系统. 你也学会了使用 `touch` 和 `nano` 创建和编辑文件.

那么在本关卡中,你将会学习到如何利用 `shell` 对文件系统进行编辑.

---

`mkdir` 命令可以让你创建一个文件夹,或者说是创建新的目录.

你在终端输入:

```
mkdir my_folder
mkdir -p parent_folder/child_folder
```

通过 -p 参数的不同, 你可以选择创建单个文件夹或者创建多级目录.

---

`cp` 命令可以复制你的文件或目录,帮你轻松搞定备份和分发任务.

更重要的是, **源文件在命令后依旧存在**.

你在终端输入:

```
cp file.txt backup.txt
```

这会把 `file.txt` 复制成 `backup.txt`.

复制整个文件夹? 加个 `-r` 参数就行:

```
cp -r my_folder my_folder_copy
```

> **TIP** `-r` 代表递归 (recursive), 也就是复制文件夹内的所有内容, 包括子文件夹和文件.

---

与复制不同, `mv` 的移动命令表现的更像剪切, 它可以把你的文件从源文件移到目标位置.

改名如何呢? 自然是可以的. 这相当于 Windows 系统中的重命名.

```
mv file.txt file_only.txt
```

也可以将文件移到某个指定路径.

```
mv file_only.txt /home/user/target_dir
```

这个操作等价于: `mv file_only.txt /home/user/target_dir/file_only.txt`（当目标是已存在的目录时）. 

---

有复制和移动, 也就有删除命令.

`rm` 命令可以删除你的文件或目录.

在终端输入:

```
rm file_backup.txt
rm -r my_folder_backup
```

这些一般就可以实现文件和文件夹的删除, 但是如果遇到一些只读权限或者比较难以删除的文件夹, 可以采用更为暴力的强制删除:

```
rm -rf temp/
```

> ⚠️ 警告: `rm -rf` 具有不可逆风险; 务必确认路径无误. 
