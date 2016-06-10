from selenium import webdriver
from getpass import getpass

import sys


lastfm_login_link = 'https://secure.last.fm/login'
lastfm_library_link = 'http://www.last.fm/user/%s/library?page='

js_script = """
var x = document.getElementsByClassName(\"chartlist-delete-button\");
for (var i = 0; i < x.length; i++) {
    x[i].click();
}
"""


if __name__ == '__main__':
    username = raw_input('Last.fm login: ')
    password = getpass('Password: ', stream=sys.stdout)

    pages = raw_input('Library pages to clear (from-to): ').split('-')

    while len(pages) != 2:
        print('Invalid pages input!')
        pages = raw_input('Library pages to clear (from-to): ').split('-')

    page_from = int(pages[0])
    page_to = int(pages[1])

    ans = raw_input('Are you sure you want to clear your scrobbles on pages %s-%s (y/n)? ' %
                    (str(page_from), str(page_to)))

    if ans.upper() == 'Y':
        link = lastfm_library_link % username

        driver = webdriver.Chrome()
        driver.get(lastfm_login_link)

        username_form = driver.find_element_by_id("id_username")
        password_form = driver.find_element_by_id("id_password")

        username_form.send_keys(username)
        password_form.send_keys(password)

        driver.find_element_by_name("submit").click()

        for i in range(page_to, page_from - 1, -1):
            l = link + str(i)
            driver.get(l)
            driver.execute_script(js_script)

        driver.close()

        print('Your scrobbles cleared')

    else:
        exit(0)
