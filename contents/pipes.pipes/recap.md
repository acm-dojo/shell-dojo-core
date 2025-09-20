## RECAP

在本章中, 你学习/练习了以下管道用法:

- `A | B` : 将 A 的标准输出作为 B 的标准输入;
- 链式组合: `cat file | grep pat | wc -l`.

### 指令速查表

- `ps -A | grep bash` : 进程筛选示例;
- `grep ERROR log | wc -l` : 统计匹配行数;
- `cat a b | grep x > out` : 结合管道与重定向.