## 环境

- ***Windows10***
- Python3.6
  - pip install virtualenvwrapper
  - 创建虚拟环境`mkvirtualenv --python=py -3.6 -c"import sys; print(sys.executable)" django1.11`
- Firefox web浏览器
- [Git](https://github.com/mozilla/geckodriver/releases		) and git bash（长篇大论）

### 如果你在window下安装Django1.11

> 针对Windows 的说明：使用git bash
>
> 在Windows 中安装Git 时，一定要选择“Use Git and included Unix tools from the Windows command prompt”（在Windows 命令提示符中运行Git 和所含的Unix 工具）。选择这个选项之后就能使用Git Bash 了。把Git Bash 作为主要命令提示符，你就能使用所有实用的GNU 命令行工具，例如ls、touch 和grep，而且目录分隔符也使用斜线表示。、
>
> Git 安装程序中，还要勾选“Use Windows’default console”（使用Windows 的默认控制台），否则Python 在Git Bash 窗口中无法正常使用。
>
> 1. 安装Python 3 时，除非已经安装了Python 2 且想继续将它用作默认版本，否则一定要选中“Add Python 3.6 to PATH”
>
> 安装完备后，在git bash中：
> ```shell 
> pip install virtualenvwrapper
> 
> # 然后让Bash自动加载virtualenvwrapper
> echo "source virtualenvwrapper.sh" >> ~/.bashrc
> source ~/.bashrc
> ```
> 测试所有软件是否正确安装的方法是，打开Git Bash 命令提示符，在任意一个文件夹中执行命令python 或pip。

本人按上方的方法配置后，依旧不能用workon启动虚拟环境，只能用source（或.)直接启动。

```
. /d/PyVirtualenv/django2.0/Scripts/activate
```

### django1.11的虚拟环境配置

- （后文不用）
- 能用virtualenv和pip的
- 下载解压[geokodriver.exe](https://github.com/mozilla/geckodriver/releases) 放到Python 的Scripts 文件夹中
- `pip install "django<1.12" "selenium<4"`

### 那么麻烦，不如就django2.0好了

看到window的django1版本那么不友好，，，而这本书给的解决方案里面，好像不兼容用户文档有中文的。

最重要的是，作者说那么多，是因为当时workon不支持windows。。。

### 来配置django2.0

- （后文用`django2.0`指代）
- 能用`virtualenv`和pip的
- 下载解压[geckodriver.exe](https://github.com/mozilla/geckodriver/releases) 放到Python 的Scripts 文件夹中。可在命令行中使用`geckodriver --version`来检查。
- `pip install "django<2.1" "selenium<4"`

