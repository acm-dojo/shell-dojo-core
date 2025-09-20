## RECAP

在本章中, 你学习/练习了以下镜像源知识:

- 仓库镜像的意义: 同步官方仓库, 但网络距离更近, 下载更快;
- 通过替换 sources 配置即可切换镜像;
- 更换后运行 `sudo apt update` 以刷新索引.

### 操作速查表

- 备份源文件: `sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak` 或备份 `.sources` 格式;
- 编辑源: 根据镜像站帮助页更新 `sources.list` 或 `ubuntu.sources`;
- [清华源](https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/)、[中科大源](https://mirrors.ustc.edu.cn/help/ubuntu.html)、[交大源](https://mirror.sjtu.edu.cn)。
- 刷新索引: `sudo apt update`.