from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.zdic.net/z/pyjs/')
#assert 'Yahoo!' in browser.title

menu = browser.find_element_by_css_selector(".pyul")
print(menu)
hidden_submenu = browser.find_element_by_css_selector("a")

actions = selenium.webdriver.common.action_chains.ActionChains(browser)
actions.move_to_element(menu)
actions.click(hidden_submenu)
actions.perform()

#elem = browser.find_element_by_name('p')  # Find the search box
#elem.send_keys('seleniumhq' + Keys.RETURN)

browser.quit()
