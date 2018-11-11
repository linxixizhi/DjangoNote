# 第三章 使用单元测试测试简单的首页

## 总结

本章介绍了以下知识。

- 新建 Django 应用。
- Django 的单元测试运行程序。
- 功能测试和单元测试之间的区别。
- Django 解析 URL 的方法，urls.py 文件的作用。
- Django 的视图函数，请求和响应对象。
- 如何返回简单的 HTML。

### 有用的命令和概念
>
> - 启动Django 的开发服务器
>
>   ```
>   python manage.py runserver
>   ```
>
> - 运行功能测试
>
>   ```
>   python functional_tests.py
>   ```
>
> - 运行单元测试
>
>   ```
>   python manage.py test
>   ```
>
> - “单元测试/ 编写代码”循环
>
>   (1) 在终端里运行单元测试。
>
>   (2) 在编辑器中改动最少量的代码。
>
>   (3) 重复上两步。

前两章相当友好，最后得到一个首页，功能测试指出首页标题没有包含“To-Do”这个词。现在，真的要写代码，去编写真正的应用了。

> ### 有问题的话
>
> 看看原文，http://www.ituring.com.cn/book/tupubarticle/22548
>
> 我故意把前两章写得这么友好和简单。从现在开始，要真正编写代码了。提前给你打个预防针：有些地方会出错。你看到的结果可能和我说的不一样。这是好事，因为这才是磨练意志的学习经历。
>
> ……

## 第一个Django应用与其测试

Django鼓励用APP的形式组织代码（虽然作者从来不用），好处挺多的，主要是方便重用代码。

```shell
python managy.py startapp lists
```

产生子文件夹lists，其中有模型、视图、测试等文件，并与子文件夹`superlists`相邻。

```
E:.
|   db.sqlite3
|   functional_tests.py
|   manage.py
+---lists
|   |   admin.py
|   |   apps.py
|   |   models.py
|   |   tests.py
|   |   views.py
|   |   __init__.py
|   \---migrations
|           __init__.py
\---superlists
    |   settings.py
    |   urls.py
    |   wsgi.py
    \---__init__.py

```

## 单元测试工作流程

> 我遵从的 TDD 方法同时使用这两种类型测试应用。采用的工作流程大致如下。
>
> (1) 先写**功能测试**，从用户的角度描述应用的新功能。
>
> (2) 功能测试失败后，想办法编写代码让它通过（或者说至少让当前失败的测试通过）。此时，使用一个或多个**单元测试**定义希望代码实现的效果，保证为应用中的每一行代码（至少）编写一个单元测试。
>
> (3) 单元测试失败后，编写最少量的**应用代码**，刚好让单元测试通过。有时，要在第 2 步和第 3 步之间多次往复，直到我们觉得功能测试有一点进展为止。
>
> (4) 然后，再次运行功能测试，看能否通过，或者有没有进展。这一步可能促使我们编写一些新的单元测试和代码等。
>
> 由此可以看出，这整个过程中，功能测试站在高层驱动开发，而单元测试则从低层驱动我们做些什么。
>
> 这个过程看起来是不是有点儿烦琐？有时确实如此，但功能测试和单元测试的目的不完全一样，而且最终写出的测试代码往往区别也很大。

## Django中的单元测试

### 一点理论

[MVC框架](https://docs.djangoproject.com/en/2.0/faq/general/#django-appears-to-be-a-mvc-framework-but-you-call-the-controller-the-view-and-the-view-the-template-how-come-you-don-t-use-the-standard-names)

> 抛开这些，Django 和任何一种 Web 服务器一样，主要任务是决定用户访问网站中的某个 URL 时做些什么。Django 的工作流程有点儿类似下述过程。
>
> (1) 针对某个 URL 的 HTTP **请求**进入。
>
> (2) Django 使用一些规则决定由哪个**视图**函数处理这个请求（这一步叫作**解析** URL）。
>
> (3) 选中的视图函数处理请求，然后返回 HTTP **响应**。
>
> 因此要测试两件事。
>
> - 能否解析网站根路径（“/”）的 URL，将其对应到我们编写的某个视图函数上？
> - 能否让视图函数返回一些 HTML，让功能测试通过？

### *lists/tests.py*

```python
from django.urls import resolve
from django.test import TestCase
from lists.views import home_page

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)
```

- `resolve` 是 Django 内部使用的函数，用于解析 URL，并将其映射到相应的视图函数上。检查解析网站根路径“/”时，是否能找到名为 `home_page` 的函数
- 

```shell
$ python manage.py test
ImportError: cannot import name 'home_page'
```

功能测试和单元测试都失败了，但是这是预期的失败。

## 编写应用代码（终于）

使用TDD时，**每次修改的代码尽量少，让失败的测试通过即可**。尤其时学习和起步阶段，一次只能修改（或添加）一行代码。

现在，来修正，而且是只修正这个错误：无法从lists.views中导入home_page。

### *lists/views.py*

```python
from django.shortcuts import render

# Create your views here.
home_page = None
```

!!!哇，作者你搞我？？？哎，接着做呗，说不定TDD就是这样的。

再次测试（又失败了‘:-( ’ ），顺便看看怎么阅读调用跟踪吧。。。###后接数字代表步骤。

```shell
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
E
======================================================================
ERROR: test_root_url_resolves_to_home_page_view (lists.tests.HomePageTest)
## 222.看哪个测试失败了，最好是之前编写的测试，这里是的。
----------------------------------------------------------------------
Traceback (most recent call last):
  File "E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C3testHomepage\superlists\lists\tests.py", line 8, in test_root_url_resolves_to_home_page_view
    found = resolve('/')
## 333.看导致失败的测试代码：这里是found = resolve('/')一行
## 444.继续往下看，找问题相关应用代码。
  File "D:\PyVirtualenv\django2.0\lib\site-packages\django\urls\base.py", line 24, in resolve
    return get_resolver(urlconf).resolve(path)
  File "D:\PyVirtualenv\django2.0\lib\site-packages\django\urls\resolvers.py", line 527, in resolve
    raise Resolver404({'tried': tried, 'path': new_path})
## 111.错误本身并不可怕，看这个错误就能发现问题了。
django.urls.exceptions.Resolver404: {'tried': [[<URLResolver <URLPattern list> (admin:admin) 'admin/'>]], 'path': ''}
## 111.错误本身并不可怕，可怕的是看这个错误还不能发现问题。

----------------------------------------------------------------------
Ran 1 test in 0.001s

FAILED (errors=1)
Destroying test database for alias 'default'...
```

其实，第一步的时候，就知道怎么回事了——Django解析`admin/`、的时候，Django抛出404错误。就是Django无法找到`admin/`的URL映射。

## URLS.py

`superlists/superlists`中有一个主`urls.py`文件，应用于整个网站，看看吧：

### *superlists/urls.py*

```python
"""superlists URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

```

> 这里也有很多Django自己生成的辅助注释和默认检验。

这里的path使你不需使用正则表达式匹配。

我们的文件将先变成这样：

```python
from django.contrib import admin
from django.urls import path
from lists import views

urlpatterns = [
    path('', views.home_page, name='home'),
]
```

再`python manage.py test`测试……尼玛，这次调用跟踪两屏幕那么长，还好，看最后一行就可以了：

```
TypeError: view must be a callable or a list/tuple in the case of include().
```

就式view中的页面不能被调用——`home_page = None`

可以调整下，把`home_page`从`None`变为可调用的函数。

> *lists/views.py*

```python
from django.shortcuts import render

# Create your views here.
def home_page():
    pass
```

### 终于成功！git。

```shell
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
Destroying test database for alias 'default'...
```



```shell
git diff
git commit -am "First unit test and url mapping, dummy view"
```

## 为视图编写单元测试

需求：

- 函数不能pass，要返回真正的HTML函数；
- 为视图编写相关测试

### *lists/tests.py*

```python
from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest

from lists.views import home_page

class HomePageTest(TestCase):
    
    def test_root_url_resolves_to_home_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct_html(self):
        request = HttpRequest()  # 1
        response = home_page(request)  # 2
        html = response.content.decode('utf8')  # 3
        self.assertTrue(html.startswith('<html>'))  # 4
        self.assertIn('<title>To-Do lists</title>', html)  # 5
        self.assertTrue(html.endswith('</html>'))  # 4
```

1. 创建`HttpRequest`对象，被请求网页时，Django收到的就是它；
2. 将`HttpRequest`传入`home_page`视图，得到响应——`HttpResponse`
3. 用`.content`提取response中的内容——或许时0011110...10110001？然后用`.decode()`将这种原始字节转换为发给用户的HTML字符串。
4. 希望网页以`<html>`开头，以`</html>`结尾
5. 希望响应中有一个`<title>`标签，其内容包含单词“To-Do lists”。

运行单元测试吧，不出意外：

```
TypeError: home_page() takes 0 positional arguments but 1 was given
```

home_page()后面没有参数，但我们给了一个。

## 单元测试/编写代码循环

现在要开始适应TDD这种“单元测试/编写代码”的循环了：

1. 在终端运行单元测试，看它们时如何失败的；
2. 在编辑器中改动**最少**量的代码，让当前失败的测试通过。
3. 回到1

好像工作量很大，初期也是如此。但是这会减少许多排错时间，且熟练后小步走，编写速度也会很快。

接下来，我们开始快步走，代码也只是局部改动：

### *lists/views.py*

```python
def home_page(request):
    pass
```

- 运行测试

```
    html = response.content.decode('utf8')  # 3
AttributeError: 'NoneType' object has no attribute 'content'
```

- 编写代码

> *lists/views.py*

```python
from django.http import HttpResponse

def home_page(request):
    return HttpResponse()
```

- 测试

```
    html = response.content.decode('utf8')  # 3
AttributeError: 'HttpRequest' object has no attribute 'content'
```

- 编。。

```python
def home_page(request):
    return HttpResponse('<html><title>To-Do lists</title></html>')
```

- 测。。

OK!!!其实是不耐烦了一连三步，详情看http://www.ituring.com.cn/book/tupubarticle/22548。

### 功能测试

先启动django，后运行功能测试：

```
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVistorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 18, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 7.145s

FAILED (failures=1)
```

还是错了？？？？哦，是那个自己设置的错。。。django一端报错也挺多。



## git

```shell
$ git diff
$ git commit -am "Basic view now returns minimal HTML"
$ git log --oneline
```

`git diff`会显示一些tests.py中新增的文本，以及view中一些奇奇怪怪的玩意。按q就退出了，大概是vim形态。

![](E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C3testHomepage\gitdiff.PNG)

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

### 进入git bash

![](E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C3testHomepage\openbash.PNG)

![](E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C3testHomepage\gitbash.PNG)

```bash
git config --global i18n.logoutputencoding utf-8
```

[参考网站](https://segmentfault.com/a/1190000000578037)，但目前，`powershell`里的乱码无解。

