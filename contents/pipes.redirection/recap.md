## RECAP

在本章中, 你学习/练习了以下重定向语法:

- `>` / `>>` : 标准输出覆盖/追加到文件;
- `<` : 将文件作为标准输入传给命令;
- `2>` / `&>` / `2>&1` : 重定向标准错误/合并输出.

### 指令速查表

- `pwd > file` : 将输出写文件;
- `echo "this is the new line" >> file` : 末尾追加一行;
- `cat < file` : 用文件作为 `cat` 命令的输入;
- `cmd > out.txt 2> err.txt` : 分流 stdout/stderr;
- `cmd &> all.txt` : 合并输出到同一文件.