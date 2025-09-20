## RECAP

在本章中, 你学习/练习了以下权限与提权概念:

- 用户与用户组: 每个文件都有 owner 与 group;
- 权限位 `rwx`: 读/写/执行, 三组人有分别的权限(用户/用户组/其他);
- `chmod` 符号/八进制表示法修改权限;
- `sudo` 以 root 权限执行单条命令; `su` 切换用户.

### 指令速查表

- `ls -al` : 查看权限与归属;
- `chmod u+x script.sh` / `chmod 755 script.sh` : 赋予执行权限;
- `chmod g= o=r file` : 精细化控制;
- `sudo <cmd>` / `sudo su` : 临时/交互式获取管理员权限.

### 你还记得吗

- 当 `cp/mv/rm` 遇到“权限不足”时你需要使用 `sudo`;
- 脚本无执行位时仍可 `bash script.sh` 运行, 但添加执行位可直接 `./script.sh`;
- 包管理与系统配置更改通常需要 `sudo`.