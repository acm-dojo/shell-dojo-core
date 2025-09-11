到目前为止,你已经学会了使用 shell 的主要功能.

你知道在 shell 下如何应用各种不同的软件与包,但是这些包又从何而来?

于是乎在本关卡中,我们将会接触 `apt` 和 `mirror` 的概念.

在本关卡中,你将会接触 `mirror`(镜像)的概念

---

事实上,所有的包都被由称作包管理器的事物所管理.

以常见的 `Ubuntu` 系统为例,其默认包管理器为 `apt` ,它极大地简化了软件的获取、安装、升级和移除过程：

你往往只需要一条简单命令如 `sudo apt install firefox` 即可完成软件安装.

不仅如此,包管理器能够自动处理软件包之间复杂的依赖关系(`Dependencies`),确保所需的所有库和组件都能被正确安装.

---

在你接触 `shell` 的早期,你想必已经尝试了一些命令,比如:

```
sudo apt install package    # 安装包
sudo apt update             # 更新包列表
sudo apt upgrade            # 升级已安装的包
```

---

这些命令通常可以帮助你自动从对应软件包的仓库中下载.

但是很多时候,由于不可抗力因素,在国内访问国外软件仓库源速度往往较慢.

为了显著提升下载速度,我们强烈建议将系统的软件源替换为国内的镜像源（如 TUNA, USTCLUG, 阿里云）.

它们与系统默认的软件源往往拥有相同的内容,但拥有更高的传输速度.

事实上,常见的软件安装包如 `pip` , `huggingface` , `modelscope` 等都是有镜像的,各位可以自行查询.

下面以清华镜像源的 `32/64` 位 `x86` 架构处理器下的 `ubuntu 24.04` 为例进行介绍.

---

与修改 `shell` 的配置文件类似,我们需要需要修改 `ubuntu` 的软件源配置文件.

在 `ubuntu 24.04` 开始,软件源配置文件变更为 `DEB822` 格式,路径为 `/etc/apt/sources.list.d/ubuntu.sources`.

在修改镜像文件的过程中,你通常需要进行以下步骤.

---

1. 将 `ubuntu.sources` 备份到同目录下的 `ubuntu.sources.bak`.

2. 修改 `ubuntu.sources`,在这个例子里你需要将其修改为:

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

在完成这一步骤后,你可以测试与 `apt` 相关的命令,一般能够提速 `100` 倍甚至更高.

---

现在,我们要求你按照上述步骤打开并修改配置文件.

其中的 `flag` 被隐藏在配置文件的 `line 71`.

祝一切顺利,愿 shell 常伴你左右.

