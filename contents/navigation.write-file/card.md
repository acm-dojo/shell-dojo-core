## 任务卡

要求将 `/challenge/.robin` 下的 `to_cp` 文件拷贝到 `/challenge/challenge_tmp/directory/cp_end/` 目录下, 名称保持不变;

然后将  `/challenge/.robin` 下的 `to_mv` 文件 移动到  `/challenge/challenge_tmp/directory/mv_end/` 目录下, 名称保持不变;

随后将 `/challenge/.robin` 下的 `to_delete` 文件删除,

最后在 `/challenge/.robin` 运行 `/challenge/run filesystem`, 即能通关.

> **TIP** 当你希望复制到的位置中间有目录不存在时, 你可以使用 `mkdir -p` 命令创建多级目录. 你也可以选择手动一个个创建它们.

> **TIP** 随时随地你都可以通过 `/challenge/card` 指令查看任务卡, 用 `/challenge/tutorial` 指令查看教程.