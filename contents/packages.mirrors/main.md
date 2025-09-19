## 关于镜像源

在上一个单元中, 你学习了使用 `apt` 来安装软件包.

但你有没有想过, 这些软件包是从哪里来的呢?

---

事实上,所有的软件包都存储在称为软件仓库 (`Repository`) 的服务器上. 这些仓库通常由操作系统的维护者或第三方组织管理.

---

但是很多时候, 由于不可抗力因素, 在国内访问国外软件仓库源速度往往较慢.

为了显著提升下载速度, 我们强烈建议将系统的软件源替换为国内的镜像源（如 TUNA, USTCLUG, 阿里云）.

它们与系统默认的软件源往往拥有相同的内容, 但拥有更高的传输速度.

> 事实上, 常见的软件安装包如 `pip` , `huggingface` , `modelscope` 等都是有镜像的, 各位可以自行查询.

---

## 更换镜像源

一般来说, **在镜像网站上你能读到如何修改软件源的说明**, 以清华镜像源为例, 你可以访问: https://mirrors.tuna.tsinghua.edu.cn/help/ubuntu/

1. 将 `ubuntu.sources` 备份到同目录下的 `ubuntu.sources.bak`.

2. 修改 `ubuntu.sources`, 在这个例子里你需要将其修改为:

```
Types: deb
URIs: https://mirrors.tuna.tsinghua.edu.cn/ubuntu
Suites: noble noble-updates noble-backports
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg

# 以下安全更新软件源包含了官方源与镜像站配置,如有需要可自行修改注释切换
Types: deb
URIs: http://security.ubuntu.com/ubuntu/
Suites: noble-security
Components: main restricted universe multiverse
Signed-By: /usr/share/keyrings/ubuntu-archive-keyring.gpg
```

在完成这一步骤后, 你可以测试与 `apt` 相关的命令, 一般能够提速 `100` 倍甚至更高.

---

以上就是关于镜像源的内容. 如果你希望使用它提速, 可以在自己的 wsl 上做相关的配置. 祝您旅途愉快!

```
[flag]
```