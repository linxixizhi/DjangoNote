TDD（测试驱动开发）是一项像武术一样的技能，或许你有一个不太好说话的师傅，比如，山羊。

如果你要开发一个网站，你朋友刚好也做过，他可能会告诉你下载什么、安装那个、配置这个、运行脚本……但是：

> TDD的过程中，第一步始终是——**编写测试**。

**首先要编写测试，然后运行，看看是否和预期一样，*失败*。**

**只有失败了，才继续下一步——编写应用程序**

或许就像山羊那样，一次只迈一步，不管多陡峭的坡，都将迈过！（早期程序员是男生居多吧？都那么爱动物么。。）

我们也会这样。

## 功能测试

确保你安装并配置好了环境，然后来编写这份功能测试（Functional Test, FT）：

> functional_tests.py

```python
from selenium import webdriver  # 导入webdriver包

brower = webdriver.Firefox()  #打开（新的）Firefox浏览器
brower.get('http://localhost:8000')  # 在这个打开的浏览器打开这个网站。

assert 'Django' in brower.title  # 断言，检查这个网页的标题是否包含单词'Django'
```

还记得吗，测试要失败哦？要确保这份测试出错——主要是要assert后面是False啦。

```shell
$ python functional_tests.py
Traceback (most recent call last):
  File "functional_tests.py", line 4, in <module>
    browser.get('http://localhost:8000')
```

> 什么？不一样？
>
> 如果看到导入selenium错误，或者geckodriver错误，去检查环境。
>
> 如果看到其他错误，注意拼写咯。

失败以后呢？对的，开发程序。

## 让Django跑起来

windows命令行中输入以下代码，（其实都一样了）

```shell
$ django-admin startproject superlists
```

django会在构造如下目录：

```powershell
E:.
│  FT.md
│  functional_tests.py
│  geckodriver.log
│
└─superlist
    │  manage.py
    │
    └─superlist
            settings.py
            urls.py
            wsgi.py
            __init__.py
```

> `superlist`里面有个`superlist`。。。令人困惑，但这是历史原因。
>
> 反正，现在只要知道，`superlists/superlists`文件夹的作用是保存整个项目的文件，包括`setting.py`（存储网站全局配置信息）；`manage.py`，作用之一是用于运行开发服务器；等等
>
> 现在，来试着运行(RUN)它：

```shell
cd superlists
python manage.py runserver
```

```shell
You have 14 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
November 10, 2018 - 16:42:58
Django version 2.0.9, using settings 'superlists.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

先不管这个`You have 14 unapplied migration(s).`，放着这个进程就好，换一个cmd，即再打开一个命令行窗口，进入`functional_tests.py`所在的目录：

```powershell
python functional_tests.py
```

> 看看那个火箭吧（2.0+版本福利）

## 工作目录

```
(django2.0) E:\application\websites\django\TestCaprineDjango\P1 TDD_DjangoBase\C1functionalTests>ls
FT.md  functional_tests.py  geckodriver.log  superlists

(django2.0) \....\>mv functional_tests.py superlists/

(django2.0) \....\>cd superlists

(django2.0) \....\superlists>ls
db.sqlite3  functional_tests.py  manage.py  superlists
```

真实、详细的地址`E:\application\websites\django\TestCaprineDjango\P1 TDD_DjangoBase\C1functionalTests\superlists>`蛋疼得很。而且每个人、每台电脑、每个项目都可能不一样，故以后用`/.../superlists/`表示它，或者直接用$省略地址。

```shell

```

> 还是说得太复杂了？那就记住/.../superlists/

## git

看看要git的文件

```shell
E:.
│  FT.md
│  functional_tests.py
│  geckodriver.log
│
└─superlist
    │  manage.py
    │
    └─superlist
            settings.py
            urls.py
            wsgi.py
            __init__.py
```

### git init和exclude配置

```shell
$ git init
```

> db.sqlite3 是数据库文件，无须纳入版本控制。前面见过的geckodriver.log 是Selenium 的日志文件，也无须跟踪变化。我们要把这两个文件添加到一个特殊的文件`.gitignore `中，让Git 忽略它们:

然而[那种方法很烦](https://www.cnblogs.com/phonecom/p/7016450.html)我选择，还顺便把麻烦的`__pycache__/`处理掉了：

> 在.git/info/exclude中，设置的则是你自己本地需要排除的文件


```
# git ls-files --others --exclude-from=.git/info/exclude
# Lines that start with '#' are comments.
# For a project mostly in C, the following would be a good set of
# exclude patterns (uncomment them if you want to use them):
# *.[oa]
# *~
*.pyc # 忽略所有后缀为.pyc的文件
__pycache__/
*.sqlite3
*.pdf
geckodriver.log
```



> “接下来还是要用`git status`命令查看进度，我才不会告诉你，这个命令用得太多了，所有我 一般使用`git st`，同样功能的！我更不会告诉你，别的命令也用别称。”

。。。要自己加[Alias](https://git-scm.com/book/en/v2/Git-Basics-Git-Aliases)，

```shell
# git rm -r --cached
$ git add .
$ git status
```

总之，结果是

```shell
On branch master

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)

        new file:   functional_tests.py
        new file:   manage.py
        new file:   superlists/__init__.py
        new file:   superlists/settings.py
        new file:   superlists/urls.py
        new file:   superlists/wsgi.py
```
相对于原来的配置，优雅，简洁。

### commit

```shell
git commit -m "This is about django study. "
```

注意这个日志是绕不过的，贪省事只会弹出Vim来让你填。你还不一定会Vim。

或许，你还可以创建个GitHub账号，把这些存到GitHub上。具体看GitHub文档。

[这篇文章](https://blog.csdn.net/qq_36474990/article/details/79208445)勉强够用。



先配置ssh，打开git bash，

```shell
ssh-keygen -t rsa -C "youremail"    //引号里填上你自己的邮箱
```

然后一直按回车，把生成的密钥文件复制到剪切板：

```shell
cat id_rsa.pub | clip
```

去GitHub上配置ssh。详情看文章](https://blog.csdn.net/qq_36474990/article/details/79208445)。

配置好后，在GitHub上新建一个repository，取好名字，新建页面会有这么两行：

```shell
shell git remote add origin https://github.com/linxixizhi/DjangoNote.gitgit 
push -u origin master
```

复制粘贴到久等了的cmd命令行：

```
(django2.0) \...\superlists>git push -u origin master
Enumerating objects: 9, done.
Counting objects: 100% (9/9), done.
Delta compression using up to 4 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (9/9), 2.64 KiB | 1.32 MiB/s, done.
Total 9 (delta 0), reused 0 (delta 0)
remote:
remote: Create a pull request for 'master' on GitHub by visiting:
remote:      https://github.com/linxixizhi/DjangoNote/pull/new/master
remote:
To https://github.com/linxixizhi/DjangoNote.git
 * [new branch]      master -> master
Branch 'master' set up to track remote branch 'master' from 'origin'.

(django2.0) \...\superlists>
```

吃个鸡庆祝下？

```