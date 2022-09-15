from selenium import webdriver

driver = webdriver.Chrome()
driver.add_cookie({"name": "portail_session", "value": 'secret', "domain": "portail.henallux.be"})
driver.get("https://portail.henallux.be/")
driver.execute_script("download_planning()")
