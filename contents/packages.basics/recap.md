## RECAP

在本章中, 你学习/练习了以下包管理基础:

- 包/仓库/包管理器的概念;
- APT 常用命令: 安装/更新/升级/本地 .deb 安装;
- 可能需要 `sudo` 执行系统级操作.

### 指令速查表

- `sudo apt update && sudo apt upgrade` : 更新索引并升级;
- `sudo apt install <pkg>` : 安装包;
- `sudo apt install ./local.deb` : 安装本地包;
- `apt show <pkg>` / `apt search <kw>` : 查看/搜索包信息.

### 你还记得吗

- 权限章节的 `sudo` 在此需要反复使用，还记得吗?
- `which`/`whereis` 可帮你确认包安装位置.
- 下一章节将教你更换源, 显著加速 `apt` 下载.