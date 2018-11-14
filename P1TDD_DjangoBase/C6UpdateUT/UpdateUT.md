
# 改进功能测试

先来做清理工作：

1. 确保两次测试之间隔离；
2. 把time.sleep换成更靠谱的东西

## 隔离功能测试

为什么单元测试没有隔离这个问题呢？或者是，为什么我们没有遇到呢？

```shell
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.651s

OK
Destroying test database for alias 'default'...
```

看看Django的操作——为一个测试单独建一个数据库，然后完事了就删掉。

我们也可以这样么？模仿它的来？比如在`functional_tests.py`的Setup或tearDown中添加执行清理任务的代码？

幸好，Django就提供了相关的工具——`LiveServerTestCase`。

```shell
mkdir functional_tests
touch functional_tests/__init__.py

git mv functional_tests.py functional_tests/tests.py
git status
```
现在的目录：
```
├─ db.sqlite3
│  geckodriver.log
│  manage.py
│
├─functional_tests
│      tests.py
│      __init__.py
├─lists
│  │  admin.py
│  │  apps.py
│  │  models.py
│  │  tests.py
│  │  views.py
│  │  __init__.py
│  │
│  ├─migrations
│  │  │  0001_initial.py
│  │  │  0002_item_text.py
│  │  │  __init__.py
│  │  └─__pycache__
│  ├─__pycache__
│  └─templates
│    └─ home.html
└─superlists
    │  settings.py
    │  urls.py
    │  __pycache__
    │  wsgi.py
    └─__init__.py
```

以后执行功能测试，要改为`python manage.py test functional_tests`了。

### *functional_tests/tests.py*

1. 改import中和class继承的test类型

```python
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class NewVistorTest(LiveServerTestCase):
```

2. 改网址，不用硬编码localhost了

```python
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 朋友推荐了一款在线待办事项清单，
        # 叶秋去看了
        self.browser.get(self.live_server_url)
```

3. 可以注释掉或删除`if __name__ == '__main__'`代码块，因为之后都使用Django进行功能测试。

```shell
$ python manage.py test functional_tests
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVistorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "\...\superlists\functional_tests\tests.py", line 60, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 1 test in 12.861s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

是不是很像Django的单元测试？

### 只运行单元测试

说到单元测试，现在执行`python manage.py test`命令，Django会运行功能测试和单元测试：

```shell
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......F
======================================================================
[...]
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 7 tests in 9.172s

FAILED (failures=1)
```

如果只想运行单元测试，可以指定只运行lists应用中的测试：
```shell
python manage.py test lists
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......
----------------------------------------------------------------------
Ran 6 tests in 0.028s

OK
Destroying test database for alias 'default'...
```

### 有用的命令（记到小抄上！）

- 运行功能测试FT
  python manage.py test functional_tests
- 运行单元测试UT
  python manage.py test lists

## 升级Selenium和Geckodriver

当Firefox自动更新，Selenium & Geckodriver也要随之更新：

- `pip install --upgrade selenium`
- 下载新版Geckodriver
- 备份旧版，移开，将新版放到PATH
- 检查：`geckodriver --version`

## 隐式等待、显示等待和含糊的time.sleep

看看time.sleep(1)

### *functional_tests/tests.py*

```python
        # 她按回车键后，页面更新
        # 待办事项表格显示了“1.买孔雀羽”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
```

这叫显式等待，与之对应的是隐式等待。但隐式等待在Selenium3之后变得极度不可靠。（其团队也认为应该避免使用隐式等待）

然而，显式等待也有问题，我们现在设置了1秒，但如果2秒才会有响应呢？而对本机大部分测试来说，0.1秒内就够了，1秒是浪费时间。但设置0.1秒可以吗？

总之，这样设置，容易浪费时间，也可能会出现测试假阳性的现象（详情可考察[这篇文章](https://www.martinfowler.com/articles/nonDeterminism.html)


### *functional_tests/tests.py*

将`check_for_row_in_lists_tabl`改名为`wait_for_row_in_list_table`，再加一些“轮询/重试逻辑”：

```python
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10 ## 1
[...]

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:  ## 2
            try:
                table = self.browser.find_element_by_id('id_list_table')  ## 3
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])  ## 4
                return
            except (AssertionError, WebDriverException) as e:  ## 5
                if time.time() - start_time > MAX_WAIT:  ## 6
                    raise e  ## 6
                time.sleep(0.5)  ## 5
```

1. MAX_WAIT设定最大等待时间
2. 循环一直进行，直到到达`raise e ## 6`或`return`
3. 与上次一样，应该是能通过的；
4. 新增，如果通过了，到达`return`，退出函数
5. 如果再最大时间内，就等待一会儿，在继续循环
    > 我们要捕获两种异常：一种是WebDriverException，在页面未加载或Selenium 未在页面上找到表格元素时抛出；另一种是AssertionError，因为页面中虽有表格，但它可能在页面重新加载之前就存在，里面还是没有我们要找的行。
6. 程序出口之一，若程序在这里结束，则超时。

这代码有些奇奇怪怪的。。。总之，先调用它：

### *functional_tests/tests.py*

```python
[...]
        # 她按回车键后，页面更新
        # 待办事项表格显示了“1.买孔雀羽”
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # 然后页面又显示了一个文本框，可以输入其他的待办事项
        # 她输入了'Use peacock feathers to make a fly'(“用孔雀羽做假蝇”)
        # 叶秋做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单也显示了这两个待办事项
        self.wait_for_row_in_list_table('1: Buy peacock feathers')
        self.wait_for_row_in_list_table('2: Use peacock feathers to make a fly')
[...]
```

```shell
$ python manage.py test
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
......F
======================================================================
FAIL: test_can_start_a_list_and_retrieve_it_later (functional_tests.tests.NewVistorTest)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "\...\superlists\functional_tests\tests.py", line 70, in test_can_start_a_list_and_retrieve_it_later
    self.fail('Finish the test!')
AssertionError: Finish the test!

----------------------------------------------------------------------
Ran 7 tests in 8.602s

FAILED (failures=1)
Destroying test database for alias 'default'...
```

据说快了一点，但是没啥感觉（Ran 1 test in 12.861s？）

为了进一步确认做得对不对，下面开始破坏测试：

### *functional_tests/tests.py*

```python
                rows = table.find_elements_by_tag_name('tr')
                # self.assertIn(row_text, [row.text for row in rows])
                self.assertIn('foo', [row.text for row in rows])
                return
```

`    self.assertIn('foo', [row.text for row in rows])AssertionError: 'foo' not found in ['1: Buy peacock feathers']`

改回去破坏其他的：

```python
            try:
                # table = self.browser.find_element_by_id('id_list_table')
                table = self.browser.find_element_by_id('id_nothing')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
```

```shell
selenium.common.exceptions.NoSuchElementException: Message: Unable to locate element: [id="id_nothing"]
```

改回去，运行测试确认。成功后，总结下：

- 测试的隔离性
- 避免用含糊的休眠：time.sleep的度不好把握，可以用重试循环代替；
- 不要依赖Selenium3的隐式等待，至少不用它在firefox上的实现.

好，清理好代码，轻装上阵——实现多人多个清单。