## RECAP

在本章中, 你学习了以下内容:

- Linux 中的命令大多是可执行文件 (Binary/Executable)
- 未指定路径时, Shell 会在 PATH 环境变量指定的目录中查找可执行文件运行

### 指令速查表

- `which <command>`: 查找命令的路径
- `whereis <command>`: 查找某个命令的相关文件 (用于多版本管理居多)
- `echo $PATH`: 查看 PATH 环境变量
- `export PATH=/new/path:$PATH`: 修改 PATH 环境变量 (添加新路径)
