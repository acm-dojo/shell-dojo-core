## RECAP

在本章中, 你学习/练习了以下关键概念:

- Shell 通过启动时读取 `~/.bashrc` / `~/.zshrc` 来“记住”配置;
- 别名 (alias) 用 `alias name="command"` 定义, 可作为命令快捷方式, 只在当前会话生效, 要永久生效需写入 rc 配置文件并 `source` 重新加载;
- 环境变量 (Environment Variables) 是被进程读取的键值设置, 常用的有 `SHELL`, `HOME`, `USER`, `PATH`

### 指令速查表

- `alias [new_name]=[content]` : 定义别名;
- `unalias [name]` : 取消别名;
- `source ~/.bashrc` / `source ~/.zshrc` : 重新加载配置;
- `env` : 列出所有当前环境变量;

### 进阶方向

- Oh My Zsh / powerlevel10k 主题与插件生态
- `zsh-autosuggestions` 与 `zsh-syntax-highlighting` 提升交互体验
- 为常用项目写函数或脚本 + 放入 PATH 替代简单 alias
