在上一关卡中,你学会了如何利用 `mkdir`, `touch` , `vim` 对于文件与文件夹的骨架进行修改.

那么在本关卡中,你将会学习到如何利用 `其他命令` 对文件进行移动、复制和删除.

---

`cp` 命令可以复制你的文件或目录,帮你轻松搞定备份和分发任务.

更重要的是,源文件在命令后依旧存在.

你在终端输入:

```
cp file.txt backup.txt
```

这会把 `file.txt` 复制成 `backup.txt`.

复制整个文件夹? 加个 `-r` 参数就行:

```
cp -r my_folder my_folder_copy
```

---

与复制不同, `mv`的移动命令表现的更像剪切, 它可以把你的文件从源文件移到目标位置.

改名如何呢?自然是可以的.

```
mv file.txt file_only.txt
```

也可以将文件移到某个指定路径.

```
mv file_only.txt /home/user/hentai
```

这个操作等价于: `mv file.txt /home/user/hentai/file_only.txt`.

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

---

现在, 你需要完成的任务是: