## 环境

### [书中环境](http://www.ituring.com.cn/book/tupubarticle/22542)

### 本人环境

- ***Windows10***
- Python3.6
  - 安装时选择“Add Python 3.6 to PATH”，或手动添加到路径。
  - pip install virtualenvwrapper
  - 创建虚拟环境`mkvirtualenv --python=py -3.6 -c"import sys; print(sys.executable)" django2.0`
- Firefox web浏览器
- [Git](https://github.com/mozilla/geckodriver/releases		) and git bash（安装时注意，见下）

### django1.11的虚拟环境配置

- （后文不用）
- 能用virtualenv和pip的
- 下载解压[geokodriver.exe](https://github.com/mozilla/geckodriver/releases) 放到Python 的Scripts （真实环境）文件夹中
- `pip install "django<1.12" "selenium<4"`

### 来配置django2.0

- （后文用`django2.0`指代）
- 能用`virtualenv`和pip的
- 下载解压[geckodriver.exe](https://github.com/mozilla/geckodriver/releases) 放到Python 的Scripts （真实环境）文件夹中。可在命令行中使用`geckodriver --version`来检查。
- `pip install "django<2.1" "selenium<4"`

## [长篇大论的git bash](git.md)

