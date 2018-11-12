from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
        header_text = self.browser.find_element_by_tag_name('h1').text  # 1111
        self.assertIn('To-Do', header_text)
        
        # 应用请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')  # 1111
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )
        
        # 她在一个文本框中输入了“买孔雀羽”
        # 她的爱好是用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')  # 2222
        
        # 她按回车键后，页面更新
        # 待办事项表格显示了“1.买孔雀羽”
        inputbox.send_keys(Keys.ENTER)  # 3333
        time.sleep(1)  # 4444
        
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr') ## 1111
        self.assertTrue(
            any(row.text == '1: Buy peacock feathers' for row in rows),
            "New to-do item did not appear in table"
        )
        
        # 然后页面又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“用孔雀羽做假蝇”
        # 叶秋做事很有条理
        self.fail('Finish the test!')

        # 页面再次更新，她的清单也显示了这两个待办事项
        pass
        # 叶秋想知道这个网站是否会保存她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有文字展示了这个功能

        # 她访问那个URL，发现她的待办事项列表还在

        # 她很满意，就去玩了
if __name__ == '__main__':
    unittest.main(warnings='ignore')
