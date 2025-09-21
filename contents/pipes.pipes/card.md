## 任务卡

`/challenge/bookstore.log` 是助教 Bookstore 项目中截取出的日志文件, 你需要通过分析日志文件来完成本次任务:

- 统计任何人切换 (SwitchUser) 到 **非root** 用户的次数, 并且将这个结果 **pipe** 给 `/challenge/submit` 指令来提交结果.

> **TIP** `grep -v` 可以实现反向过滤, 也就是**过滤掉包含某个关键词的行**, 只**保留不包含该关键词**的行.

> **TIP** 你可以用 `grep -c` 输出当前匹配的行数, 或者将结果 pipe 进 `wc -l` 统计行数. 后者事实上用得更加广泛.

> **TIP** 随时随地你都可以通过 `/challenge/card` 指令查看任务卡, 用 `/challenge/tutorial` 指令查看教程.