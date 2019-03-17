# git配置

[TOC]

> 这里假设python3在系统PATH中。

如果你在window下安装Django2.0，就不用配置git bash。cmd 或 powershell就可以了。因为windows早就能用workon管理虚拟环境了。（但是我不想看到那长长的工作路径，还是转了git bash）

## git安装

而不幸，你在window下安装Django1.11。要么，卸掉重装2.0；要么就按下面的方式安装git：

1. 【第四页】“Use Git and included Unix tools from the Windows command prompt”（在Windows 命令提示符中运行Git 和所含的Unix 工具）

![在Windows命令提示符中运行Git和所含的Unix工具](git%E9%85%8D%E7%BD%AE/%E5%9C%A8Windows%E5%91%BD%E4%BB%A4%E6%8F%90%E7%A4%BA%E7%AC%A6%E4%B8%AD%E8%BF%90%E8%A1%8CGit%E5%92%8C%E6%89%80%E5%90%AB%E7%9A%84Unix%E5%B7%A5%E5%85%B7.PNG)

1. 【第八页】勾选“Use Windows’default console”（使用Windows 的默认控制台）

![使用Windows的默认控制台](git%E9%85%8D%E7%BD%AE/%E4%BD%BF%E7%94%A8Windows%E7%9A%84%E9%BB%98%E8%AE%A4%E6%8E%A7%E5%88%B6%E5%8F%B0.PNG)

1. 【我的方式】由于按下方的方法配置后，仍然无法在git bash使用workon打开虚拟环境（或许与目录有中文有关？）选择使用`source </path/to/activate>`手动开启。

```
. /d/PyVirtualenv/django2.0/Scripts/activate
```

> 1. 【作者的方式】安装完备后，在git bash中：
>
> ```shell 
> pip install virtualenvwrapper
> 
> # 然后让Bash自动加载virtualenvwrapper
> echo "source virtualenvwrapper.sh" >> ~/.bashrc
> source ~/.bashrc
> ```
>
> 测试所有软件是否正确安装的方法是，打开Git Bash 命令提示符，在任意一个文件夹中执行命令python 或pip。

## [配置别名](https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/001375234012342f90be1fc4d81446c967bbdc19e7c03d3000)

我们只需要敲一行命令，以后`st`就表示`status`，还有类似的：

```
$ git config --global alias.st status
$ git config --global alias.co checkout
$ git config --global alias.ci commit
$ git config --global alias.br branch
```



```
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```



## [中文乱码解决方案](https://segmentfault.com/a/1190000000578037)
### git status


#### 乱码例子

`"git\351\205\215\347\275\256/"`

#### 解决

```shell
git config --global core.quotepath false
```

### git log

![](P1TDD_DjangoBase\C3testHomepage\gitdiff.PNG)

`git log --oneline`，有乱码

```
2b57ae1 (HEAD -> master) <E4><B8><80><E5><A4><A9><E8><A2><AB><E6><B5><8B><E8><AF><95><E8><99><90>
<E4><BA><86><E5><A5><BD><E5><87><A0><E9><81><8D><EF><BC><8C><E4><BD><86><E6><88><91><E7><9F><A5><E9><81><93><E8><BF><99><E6><98><AF><E6><9C><89><E7><94><A8><E7><9A><84>
af5c9f2 (origin/master) First unit test and url mapping, dummy view
be2ac47 Add the note of chapter 2, write the first unittest and use the unittest packet.
d6d4645 fixed two bugs
0728cf1 fix some bugs
be6e2ab added
33ef4b9 This is about django study.
```

```bash
git config --global i18n.logoutputencoding utf-8
```

[参考网站](https://segmentfault.com/a/1190000000578037)，但目前，`powershell`里的乱码貌似无解。

## 进入git bash

### 小技巧，快速打开

按WIN键输入“git bash”

![搜索gitbash.PNG](git%E9%85%8D%E7%BD%AE/%E6%90%9C%E7%B4%A2gitbash.PNG)

### 在某个目录，快速打开

- git bash: 鼠标右键即可
- Powershell: shift+鼠标右键快速打开

![shift_鼠标右键快速打开.PNG](git%E9%85%8D%E7%BD%AE/shift_%E9%BC%A0%E6%A0%87%E5%8F%B3%E9%94%AE%E5%BF%AB%E9%80%9F%E6%89%93%E5%BC%80.PNG)


## 外观配置

window的命令行又短又宽（大概是下图这种比例），黑色也很刺眼，按下图方式进入属性配置（在窗口首行右击选择属性），然后调整两个属性。

![进入属性](git%E9%85%8D%E7%BD%AE/%E8%BF%9B%E5%85%A5%E5%B1%9E%E6%80%A7.PNG)

![调整窗口大小](git%E9%85%8D%E7%BD%AE/%E8%B0%83%E6%95%B4%E7%AA%97%E5%8F%A3%E5%A4%A7%E5%B0%8F.PNG)

![调整窗口大小](git%E9%85%8D%E7%BD%AE/%E8%B0%83%E6%95%B4%E9%A2%9C%E8%89%B2%E4%B8%BARGB545964.PNG)
