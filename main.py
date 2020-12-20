from selenium.common.exceptions import TimeoutException
# private variables and information are stored in inputs.py file
#           username_str = 'username'
#           password_str = 'password'
#           hash_str = {"#1", "#2", "#3", "#4", "#5", "#6"}
#           target_of_likes = 100
#           max_tryings = 3
#           max_skip = 10
#           path_to_chromedriver = '/path/to/chromedriver'
from inputs import *
from definitions import *
import sys

original_stdout = sys.stdout
f = open('WorkSpace/IgBot/LogFiles/log_file.txt', 'w')
f.close()


browser = lunch_browser(path_to_chromedriver, False)
cookies_accept(browser, ita)
login(browser, username_str, password_str)
avoid_popups(browser, ita)

total_aim_of_likes = 0
total_viewed_posts = 0
total_liked = 0

for hash_i in hash_str:
    # print(f"searching for {hash_i} posts")
    number_of_posts = search_hashtag(browser, ita, hash_i)
    # max_number_of_scroll_to_bottom = math.floor(number_of_posts/100)
    # random_scrolls = random.randint(1, max_number_of_scroll_to_bottom)
    # print(f"total number of scroll to proceed = {random_scrolls}")
    # scroll_down_function(browser, random_scrolls)
    click_first_pic(browser)

    # create variables that counts liked posts, total viewed, tryings, result of like function and number
    # of total posts skipped in a row
    liked = 0
    total = 0
    tryings = 0
    result_of_LIIO = 0
    skip = 0

    # starting from the most recent post there is no need to change the xpath of the 'next_post' bc they are all equal
    while (liked < target_of_likes) and (skip < max_skip):
        try:
            result_of_LIIO = like_if_its_ok(browser, liked)
            liked += result_of_LIIO
            browser.find_element_by_xpath("/html/body/div[5]/div[1]/div/div/a[2]").click()
            total += 1
            if result_of_LIIO == 1:
                skip = 0
            else:
                skip += 1
        except TimeoutException:
            if tryings == max_tryings:
                # print(f'image did not load after {max_tryings} attempts')
                browser.close()
                exit()
            back_n_forth(browser)
            tryings += 1

    # display outcome
    with open('WorkSpace/IgBot/LogFiles/log_file.txt', 'a') as f:
        sys.stdout = f
        print(f"- {hash_i} posts, target of likes = {target_of_likes}, likes = {liked}, total viewed = {total}")
    total_aim_of_likes += target_of_likes
    total_viewed_posts += total
    total_liked += liked

with open('WorkSpace/IgBot/LogFiles/log_file.txt', 'a') as f:
    sys.stdout = f
    print(f"total target = {total_aim_of_likes}, total viewed = {total_viewed_posts}, total liked = {total_liked}")

sys.stdout = original_stdout
with open('WorkSpace/IgBot/LogFiles/log_file.txt', 'r') as f:
    print(f.read())
# close browser and exit
browser.close()
