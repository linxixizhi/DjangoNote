# Chapter2 UnitTest

目前，Django已经是“可用的”了。

现在，是时候知道要做什么了——一个待办事项清单。

> 这说明我们始终追求时尚，一开始教网站就先介绍怎么开发博客，后来一窝蜂地又介绍论坛和投票应用，现在流行待办事项清单。

一个待办清单，只显示一个由文本字符串组成的列表，是个最简可用的例子，也挺适合用来介绍应用——演示Web开发主要过程，以如何在各个步骤中保持TDD的理念。

> 而且，可以用各种方式拓展功能——使用不同的持久模型、添加最后期限、提醒和分享功能、改进客户端UI……甚至可以不局限于待办清单，可以列出任何事项。
>
> 比如，[奇妙清单](https://www.wunderlist.com/zh/)。

## FT驱动开发最简可用应用

使用Selenium实现的FT可以驱动真正的网页浏览器，让我们从用户角度查看应用。也因此，这种测试叫FT（功能测试）

> 或者说是验收、端到端、黑箱，喜欢就好

功能测试应有一个人类可读、容易理解的故事。为了讲清楚这故事，需结合测试代码和代码注释——先写注释，勾勒重点，从而使写出的代码人类可读，甚至作为应用功能与需求的文档用于分享讨论。

这章强调“最简可用应用”，我们现在就来开发这个最简可用待办事项清单——输入并保存用户的待办事项，保存到用户删除为止。

### functional_tests.py
>
> ```python
>from selenium import webdriver
>
>browser = webdriver.Firefox()
># 朋友推荐了一款在线待办事项清单，
># 叶秋去看了
>browser.get('http://localhost:8000')
>
># 她注意到，网页的标题和头部都包含“To-Do”这个词
>assert 'To-Do' in browser.title
>
># 应用请她输入一个待办事项
># 她在一个文本框中输入了“买孔雀羽”
># 她的爱好是用假蝇做饵钓鱼
># 她按回车键后，页面更新，待办事项表格显示了“1.买孔雀羽”
># 然后页面又显示了一个文本框，可以输入其他的待办事项
># 她输入了“用孔雀羽做假蝇”
># 叶秋做事很有条理
>
># 页面再次更新，她的清单也显示了这两个待办事项
>
># 叶秋想知道这个网站是否会保存她的清单
># 她看到网站为她生成了一个唯一的URL
># 而且页面中有文字展示了这个功能
>
># 她访问那个URL，发现她的待办事项列表还在
>
># 她很满意，就去玩了
>
>browser.quit()
> ```
>
> ### 注释是谎言？
>
> 简单重复代码意图的是：
>
> ```python
> # 把wibble的值增加 1
> wibble += 1
> ```
>
> 这样的注释毫无意义、不便修改、会误导人。
>
> 我们要努力做到让代码可读，使用有意义的变量名和函数名，保持代码结构清晰，这样就不再需要通过注释说明代码做了什么，只要偶尔写一些注释说明为什么这么做。
>
> 进一步了解：
>
> - 行为驱动开发（Behaviour Driven Development，详情参见附录E）
> - 测试DSL（Domain Specific Language，领域特定语言）

### 注定失败的第一次测试

更新`functional_tests.py`，打开两个cmd，进入相关虚拟环境和工作目录，

先启动服务器

```shell
python manage.py runserver
```

在另一个cmd中运行测试

```shell
python functional_tests.py
```


> 我的小抄
> ```shell
> cd E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C2unittest\superlists
> 
> e:
> 
> workon django2.0
> python manage.py runserver
> ```
>
> ```shell
> cd E:\application\websites\django\TestCaprineDjango\P1TDD_DjangoBase\C2unittest\superlists
> 
> e:
> 
> python functional_tests.py
> ```

```shell
Traceback (most recent call last):
  File "functional_tests.py", line 9, in <module>
    assert 'ToDo' in browser.title
AssertionError
```

预期的失败，其实是好消息啦——测试编写正确。

## 2.2 Python标准库的unittest模块

### 用unittest模块处理几个问题

> 1. `AssertionError`消息没什么用，如果测试能指出在浏览器的标题中到底找到了什么就好了。
> 2. Firefox 窗口一直停留在桌面上，如果能自动将其关闭就好了。

```python
from selenium import webdriver

browser = webdriver.Firefox()
browser.get('http://localhost:8000')
try:
    assert 'To-Do' in browser.title, "Browser title was " + browser.title
except AssertionError:
    print('Test failed normally')
finally:
    browser.quit()
```



但是用`unittest`模块更好：

>```python
>from selenium import webdriver
>import unittest
>
>class NewVistorTest(unittest.TestCase):
>    def setUp(self):
>        self.browser = webdriver.Firefox()
>        
>    def tearDown(self):
>        self.browser.quit()
>        
>    def test_can_start_a_list_and_retrieve_it_later(self):
>        # 朋友推荐了一款在线待办事项清单，
>        # 叶秋去看了
>        self.browser.get('http://localhost:8000')
>        
>        # 她注意到，网页的标题和头部都包含“To-Do”这个词
>        self.assertIn('To-Do', self.browser.title)
>        self.fail('Finish the test!')
>        
>
>        # 应用请她输入一个待办事项
>        # 她在一个文本框中输入了“买孔雀羽”
>        # 她的爱好是用假蝇做饵钓鱼
>        # 她按回车键后，页面更新，待办事项表格显示了“1.买孔雀羽”
>        # 然后页面又显示了一个文本框，可以输入其他的待办事项
>        # 她输入了“用孔雀羽做假蝇”
>        # 叶秋做事很有条理
>
>        # 页面再次更新，她的清单也显示了这两个待办事项
>
>        # 叶秋想知道这个网站是否会保存她的清单
>        # 她看到网站为她生成了一个唯一的URL
>        # 而且页面中有文字展示了这个功能
>
>        # 她访问那个URL，发现她的待办事项列表还在
>
>        # 她很满意，就去玩了
>if __name__ == '__main__':
>    unittest.main(warnings='ignore')
>```

关于语法、命名的注释不应该写在代码里面，我们就在这里讨论好了：

1. class继承`unittest.TestCase`类，
2. 方法名很长`test_can_start_a_list_and_retrieve_it_later`，但起个有意义的名称是必要的，且你不用调用这个方法。
3. `setUp`方法：在测试之前运行；`tearDown`方法：在测试之后运行。后者有点类似`try/except/finally`语句，除非`setUp`方法异常
4. `assertIn`断言辅助函数，具体见[unittest的官方文档](https://docs.python.org/3.6/library/unittest.html)
5. `self.fail`调用失败，生成指定错误消息。此处用来结束测试
6. `warnings='ignore'`，禁止抛出`ResourceWarning`，可以移除。

再来试一下：

```shell
$ python functional_tests.py
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (__main__.NewVistorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "functional_tests.py", line 17, in test_can_start_a_list_and_retrieve_it_later
    self.assertIn('To-Do', self.browser.title)
AssertionError: 'To-Do' not found in 'Django: the Web framework for perfectionists with deadlines.'

----------------------------------------------------------------------
Ran 1 test in 7.393s

FAILED (failures=1)
```

这个测试不仅实现了上面两个需求，还有比较完整、排版尚可的报告。

你可以找找看，运行几个测试，几个失败了，还有`assertIn`的作用是什么...

## 2.3 git、小结

```shell
git status
git diff  # 查看上一次提交和当前硬盘中保存内容之间的差异
git add .
git commit -am "Add the note of chapter 2, write the first ut and use the unittest packet. "# -a参数自动添加已跟踪文件的改动，若无新增文件，可用此参数而去掉git add的步骤
```

现在到哪里了？测试完备、需求明确、可以真正开始写代码了！

有用的TDD概念，添加到Anki中

用户故事
从用户的角度描述应用应该如何运行。用来组织功能测试。

预期失败
意料之中的失败