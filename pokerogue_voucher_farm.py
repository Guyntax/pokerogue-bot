import cv2 as cv
import numpy as np
import os
from mss import mss
import time
import keyboard
import datetime


N = 1
# Change the working directory to the folder this script is in.
# Doing this because I'll be putting the files from each video in their own folder on GitHub
# os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Can use IMREAD flags to do different pre-processing of image files,
# like making them grayscale or reducing the size.
# https://docs.opencv.org/4.2.0/d4/da8/group__imgcodecs.html

def imread(path, filename):
     return cv.imread(path + filename, cv.IMREAD_GRAYSCALE)

path_pre_game = os.getcwd() + '\\templates_pre_game\\'
path_game = os.getcwd() + '\\templates_game\\'

side_menu_im = imread(path_pre_game, 'menu.jpg')
new_game_im = imread(path_pre_game, 'new_game.jpg')
continue_im = imread(path_pre_game, 'continue.jpg')
new_game_w_continue_im = imread(path_pre_game, 'new_game_w_continue.jpg')
blank_black_im = imread(path_pre_game, 'blank_black.jpg')
blank_green_im = imread(path_pre_game, 'blank_green.jpg')
add_to_party_im = imread(path_pre_game, 'add_to_party.jpg')
select_a_machine_im = imread(path_pre_game, 'select_a_machine.jpg')
load_screen_im = imread(path_pre_game, 'load_screen.jpg')


what_will_im = imread(path_game, 'what_will.jpg')
wants_to_learn_im = imread(path_game, 'wants_to_learn.jpg')
reroll_im = imread(path_game, 'reroll.jpg')
skip_an_item_im = imread(path_game, 'skip_an_item.jpg')
no_pp_im = imread(path_game, 'no_pp.jpg')
is_disabled_im = imread(path_game, 'is_disabled.jpg')
will_you_switch_im = imread(path_game, 'will_you_switch.jpg')
pokemon_info_im = imread(path_game, 'pokemon_info.jpg')
fainted_im = imread(path_game, 'fainted.jpg')
evolved_im = imread(path_game, 'evolved.jpg')
rare_candy_im = imread(path_game, 'rare_candy.jpg')
voucher_im = imread(path_game, 'voucher.jpg')
voucher_plus_im = imread(path_game, 'voucher_plus.jpg')
voucher_premium_im = imread(path_game, 'voucher_premium.jpg')



# new_game_im = cv.imread(path_pre_game + 'new_game.jpg', cv.IMREAD_GRAYSCALE)
# continue_im = cv.imread(path_pre_game + '\\continue.jpg', cv.IMREAD_GRAYSCALE)
# new_game_im = cv.imread(path_pre_game + '\\new_game.jpg', cv.IMREAD_GRAYSCALE)
# add_to_party_im = cv.imread(path_pre_game + '\\add_to_party.jpg', cv.IMREAD_GRAYSCALE)

# wants_to_learn_im = cv.imread(path_game + '\\wants_to_learn.jpg', cv.IMREAD_GRAYSCALE)
# reroll_im = cv.imread(path_game + '\\reroll.jpg', cv.IMREAD_GRAYSCALE)
# no_pp_im = cv.imread(path_game + '\\no_pp.jpg', cv.IMREAD_GRAYSCALE)
# is_disabled_im = cv.imread(path_game + '\\is_disabled.jpg', cv.IMREAD_GRAYSCALE)
# will_you_switch_im = cv.imread(path_game + '\\will_you_switch.jpg', cv.IMREAD_GRAYSCALE)
# pokemon_info_im = cv.imread(path_game + '\\pokemon_info.jpg', cv.IMREAD_GRAYSCALE)



with mss() as sct:

    monitor = sct.monitors[1]
    raw_im = sct.grab(monitor)
    screenshot_im = cv.cvtColor(np.array(raw_im), cv.COLOR_BGR2GRAY)

def get_low_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x*0, x)
    yy = slice(y // 7 * 5, y)
    return yy, xx

def get_high_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x * 0, x // 2)
    yy = slice(y *0, y // 4)
    return yy, xx

def get_yes_no_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x // 7 * 5, x)
    yy = slice(y // 7 * 3, y // 7 * 6)
    return yy, xx

def get_item_1_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x //20 *5, x // 20 *9)
    yy = slice(y // 20 *7, y // 20 *11)
    return yy, xx

def get_item_2_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x //20 *8, x // 20 *12)
    yy = slice(y // 20 *7, y // 20 *11)
    return yy, xx

def get_item_3_mask(im):
    x = im.shape[1]
    y = im.shape[0]
    xx = slice(x //20 *11, x // 20 *15)
    yy = slice(y // 20 *7, y // 20 *11)
    return yy, xx


low_mask = get_low_mask(screenshot_im)
high_mask = get_high_mask(screenshot_im)
# yes_no_mask = get_yes_no_mask(screenshot_im)
item_1_mask = get_item_1_mask(screenshot_im)
item_2_mask = get_item_2_mask(screenshot_im)
item_3_mask = get_item_3_mask(screenshot_im)


def match_and_locate_template(screenshot, image, mask=None):
    if mask is None:
        match_result = cv.matchTemplate(screenshot, image, cv.TM_CCOEFF_NORMED)
        _, result_confidence, _, _ = cv.minMaxLoc(match_result)
    else:
        match_result = cv.matchTemplate(screenshot[mask], image, cv.TM_CCOEFF_NORMED)
        _, result_confidence, _, _ = cv.minMaxLoc(match_result)
    return result_confidence


def get_screenshot():
    with mss() as sct:

        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        screenshot_im = cv.cvtColor(np.array(im), cv.COLOR_BGR2GRAY)
    return screenshot_im






def main():
    CONFIDENCE_THRESHOLD = 0.6
    MIN_DELAY = 0.2
    SPEND_VOUCHER = True    
    SHINY_GATCH = False
    VOUCHER_TYPE = "premium" # plus or premium

    def go_to_load_game_menu():
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)


    def refresh_page():
        keyboard.press_and_release('ctrl+r')
        time.sleep(MIN_DELAY)

    time.sleep(0.5)
    refresh_page()
    time.sleep(2)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, continue_im) < CONFIDENCE_THRESHOLD:
        print("Continue - Reset battle")
        if counter >= 100 :
            return
        keyboard.press_and_release('x')
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1
    time.sleep(0.5)
    go_to_load_game_menu()
    time.sleep(0.5)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, load_screen_im) < CONFIDENCE_THRESHOLD:
        print("Load reset battle")
        if counter >= 100 :
            return
        if counter >= 20 and match_and_locate_template(ss, continue_im) >= CONFIDENCE_THRESHOLD:
            go_to_load_game_menu()
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    time.sleep(0.5)

    keyboard.press_and_release('z')
    time.sleep(MIN_DELAY)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, what_will_im, low_mask) < CONFIDENCE_THRESHOLD:
        print("Reset battle - Start")
        if counter >= 100 :
            return
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    def open_side_menu():
        keyboard.press_and_release('m')
        time.sleep(MIN_DELAY)
    
    time.sleep(0.5)
    open_side_menu()
    time.sleep(0.5)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, side_menu_im) < CONFIDENCE_THRESHOLD:
        print("Reset battle - Save and quit")
        if counter >= 100 :
            return
        ss = get_screenshot()
        time.sleep(0.5)
        counter += 1

    def save_and_quit():
        keyboard.press_and_release('up')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('up')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    time.sleep(0.5)
    save_and_quit()
    time.sleep(0.5)



    if SPEND_VOUCHER:
        ss = get_screenshot()
        counter = 0
        while match_and_locate_template(ss, continue_im) < CONFIDENCE_THRESHOLD:
            print("Continue - Egg gatcha")
            if counter >= 100:
                return
            ss = get_screenshot()
            time.sleep(0.5)
            counter += 1

        time.sleep(0.5)

        keyboard.press_and_release('m')
        time.sleep(MIN_DELAY)

        ss = get_screenshot()
        counter = 0
        while match_and_locate_template(ss, side_menu_im) < CONFIDENCE_THRESHOLD:
            print("Select egg gatcha")
            if counter >= 100:
                return
            ss = get_screenshot()
            time.sleep(0.5)
            counter += 1

        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

        ss = get_screenshot()
        counter = 0
        while match_and_locate_template(ss, select_a_machine_im, low_mask) < CONFIDENCE_THRESHOLD:
            print("Egg gatcha")
            if counter >= 100:
                return
            ss = get_screenshot()
            time.sleep(0.5)
            counter += 1
        
        if VOUCHER_TYPE == "premium":
            keyboard.press_and_release('down') # extra down for premium voucher
            time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        if SHINY_GATCH:
            keyboard.press_and_release('right')
            time.sleep(MIN_DELAY)

        # wait for gatcha_machine change
        time.sleep(1)

        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z') # Extra
        time.sleep(MIN_DELAY)

        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)

     
    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, continue_im) < CONFIDENCE_THRESHOLD:
        print("Continue - Main battle")
        if counter >= 100:
            return
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('x')
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    time.sleep(0.5)

    
    go_to_load_game_menu()

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, load_screen_im) < CONFIDENCE_THRESHOLD:
        print("Load main battle")
        if counter >= 100 :
            return
        if counter >= 20 and match_and_locate_template(ss, continue_im) >= CONFIDENCE_THRESHOLD:
            go_to_load_game_menu()
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    time.sleep(0.5)

    def load_penultimate_game():
        keyboard.press_and_release('up')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('up')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    def load_second_game():
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    def load_third_game():
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('down')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    load_penultimate_game()
    # load_second_game()
    # load_third_game()

    # ss = get_screenshot()
    # while match_and_locate_template(ss, will_you_switch_im, low_mask) < CONFIDENCE_THRESHOLD:
    #     print(0)
    #     print(match_and_locate_template(ss, will_you_switch_im, low_mask))
    #     keyboard.press_and_release('x')
    #     time.sleep(0.5)
    #     ss = get_screenshot()


    # time.sleep(0.5)
    # keyboard.press_and_release('x')
    # time.sleep(MIN_DELAY)

    # time.sleep(1)

    # keyboard.press_and_release('x')
    # time.sleep(MIN_DELAY)

    time.sleep(0.5)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, what_will_im, low_mask) < CONFIDENCE_THRESHOLD:
        print("Main battle - Start")
        if counter >= 100:
            return
        if counter >= 20 and match_and_locate_template(ss, load_screen_im) >= CONFIDENCE_THRESHOLD:
            load_penultimate_game()
        keyboard.press_and_release('x')
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    def attack():
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)


    attack()

    # time.sleep(0.5)
    # keyboard.press_and_release('right')
    # time.sleep(MIN_DELAY)

    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)

    # # EXTRA
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)

    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, skip_an_item_im, low_mask) < CONFIDENCE_THRESHOLD:
        print("Skip item")
        if counter >= 100:
            return
        if counter >= 20 and match_and_locate_template(ss, what_will_im, low_mask) >= CONFIDENCE_THRESHOLD:
            attack()
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('x')
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    time.sleep(0.5)

    def select_reward_voucher_plus():
        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)
        # keyboard.press_and_release('left')
        # time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    def select_reward_voucher_premium():
        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('right')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('right')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)

    def select_second_reward():
        keyboard.press_and_release('x')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('right')
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('z')
        time.sleep(MIN_DELAY)   


    def select_reward():
        if VOUCHER_TYPE == "plus":
            select_reward_voucher_plus()
        elif VOUCHER_TYPE == "premium":
            # select_reward_voucher_premium()
            select_second_reward()

    select_reward()

    # keyboard.press_and_release('down')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('down')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('up')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY) 

    # time.sleep(2)

    # keyboard.press_and_release('right')
    # time.sleep(MIN_DELAY) 
    # keyboard.press_and_release('z')
    # time.sleep(MIN_DELAY) 

    # ss = get_screenshot()
    # while match_and_locate_template(ss, will_you_switch_im, low_mask) < CONFIDENCE_THRESHOLD:
    #     print(2)
    #     time.sleep(0.5)
    #     ss = get_screenshot()
    ss = get_screenshot()
    counter = 0
    while match_and_locate_template(ss, what_will_im, low_mask) < CONFIDENCE_THRESHOLD:
        print("Main battle - Completed")
        if counter >= 100:
            return
        if counter >= 20 and match_and_locate_template(ss, skip_an_item_im, low_mask) >= CONFIDENCE_THRESHOLD:
            select_reward()
        time.sleep(MIN_DELAY)
        keyboard.press_and_release('x')
        time.sleep(0.5)
        ss = get_screenshot()
        counter += 1

    # keyboard.press_and_release('x')
    # time.sleep(MIN_DELAY)
    # keyboard.press_and_release('x')
    # time.sleep(MIN_DELAY)

    # time.sleep(MIN_DELAY)


    return

counter = 0

while True:
    start_time = datetime.datetime.now()
    try:
        main()
    finally:
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        difference_seconds = time_difference.total_seconds()
        print(f"Time difference: {difference_seconds} seconds")

