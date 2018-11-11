from selenium import webdriver
import unittest

class NewVistorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        
    def tearDown(self):
        self.browser.quit()
        
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 朋友推荐了一款在线待办事项清单，
        # 叶秋去看了
        self.browser.get('http://localhost:8000')
        
        # 她注意到，网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')
        

        # 应用请她输入一个待办事项
        # 她在一个文本框中输入了“买孔雀羽”
        # 她的爱好是用假蝇做饵钓鱼
        # 她按回车键后，页面更新，待办事项表格显示了“1.买孔雀羽”
        # 然后页面又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“用孔雀羽做假蝇”
        # 叶秋做事很有条理

        # 页面再次更新，她的清单也显示了这两个待办事项

        # 叶秋想知道这个网站是否会保存她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有文字展示了这个功能

        # 她访问那个URL，发现她的待办事项列表还在

        # 她很满意，就去玩了
if __name__ == '__main__':
    unittest.main(warnings='ignore')