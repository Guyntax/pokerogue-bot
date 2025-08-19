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


new_game_im = imread(path_pre_game, 'new_game.jpg')
continue_im = imread(path_pre_game, 'continue.jpg')
new_game_w_continue_im = imread(path_pre_game, 'new_game_w_continue.jpg')
blank_black_im = imread(path_pre_game, 'blank_black.jpg')
blank_green_im = imread(path_pre_game, 'blank_green.jpg')
add_to_party_im = imread(path_pre_game, 'add_to_party.jpg')


wants_to_learn_im = imread(path_game, 'wants_to_learn.jpg')
reroll_im = imread(path_game, 'reroll.jpg')
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

def search_and_process_item(item_im, confidence_threshold):
    confidence_1 = match_and_locate_template(screenshot_im, item_im, item_1_mask)
    confidence_2 = match_and_locate_template(screenshot_im, item_im, item_2_mask)
    confidence_3 = match_and_locate_template(screenshot_im, item_im, item_3_mask)
    if confidence_1 > confidence_threshold:
        pass
    elif confidence_2 > confidence_threshold:
        keyboard.press_and_release('right')
        time.sleep(0.5)
    elif confidence_3 > confidence_threshold:
        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('right')
        time.sleep(0.5)
    keyboard.press_and_release('z')
    time.sleep(0.5)
    keyboard.press_and_release('z')
    time.sleep(1)

def reroll_special_function(confidence_threshold):
    confidence_rare_candy = match_and_locate_template(screenshot_im, rare_candy_im)
    confidence_voucher = match_and_locate_template(screenshot_im, voucher_im)
    confidence_voucher_plus = match_and_locate_template(screenshot_im, voucher_plus_im)
    confidence_voucher_premium = match_and_locate_template(screenshot_im, voucher_premium_im)

    if confidence_voucher_premium > confidence_threshold:
        search_and_process_item(voucher_premium_im, confidence_threshold)
        return True

    if confidence_voucher_plus > confidence_threshold:
        search_and_process_item(voucher_plus_im, confidence_threshold)
        return True
    
    if confidence_voucher > confidence_threshold:
        search_and_process_item(voucher_im, confidence_threshold)
        return True
    
    if confidence_rare_candy > confidence_threshold:
        search_and_process_item(rare_candy_im, confidence_threshold)
        return True
    
    return False



def main():
    CONFIDENCE_THRESHOLD = 0.7

    confidence_reroll = match_and_locate_template(voucher_premium_im, reroll_im)
    if (confidence_reroll >= CONFIDENCE_THRESHOLD):
        return
    confidence_reroll = match_and_locate_template(voucher_plus_im, reroll_im)
    if (confidence_reroll >= CONFIDENCE_THRESHOLD):
        return
    confidence_reroll = match_and_locate_template(voucher_im, reroll_im)
    if (confidence_reroll >= CONFIDENCE_THRESHOLD):
        return

    # if new_game_result_confidence >= CONFIDENCE_THRESHOLD:
    #         keyboard.press_and_release('z')
    #         time.sleep(1)
    #         keyboard.press_and_release('z')
    #         time.sleep(1)
    #         keyboard.press_and_release('z')
    #         time.sleep(1)
    #         keyboard.press_and_release('z')
    #         time.sleep(1)
    #         keyboard.press_and_release('enter')
    #         time.sleep(1)
    #         keyboard.press_and_release('z')
    #         time.sleep(1)


    confidence_reroll = match_and_locate_template(screenshot_im, reroll_im)
    if (confidence_reroll >= CONFIDENCE_THRESHOLD):
            print(f"reroll: {confidence_reroll}")
            if reroll_special_function(CONFIDENCE_THRESHOLD):
                 return
            
            keyboard.press_and_release('x')
            time.sleep(1)
            keyboard.press_and_release('z')
            time.sleep(1+N)
            return

    confidence_evolved = match_and_locate_template(screenshot_im, evolved_im, low_mask)
    if (confidence_evolved >= CONFIDENCE_THRESHOLD):
            print(f"evolved: {confidence_evolved}")
            keyboard.press_and_release('x')
            time.sleep(1)
            keyboard.press_and_release('z')
            time.sleep(1+N)
            return

    confidence = match_and_locate_template(screenshot_im, wants_to_learn_im, low_mask)
    if confidence >= CONFIDENCE_THRESHOLD:
            print(f"want to learn: {confidence}")
            keyboard.press_and_release('z')
            time.sleep(1)
            keyboard.press_and_release('z')
            time.sleep(1)
            keyboard.press_and_release('x')
            time.sleep(1)
            keyboard.press_and_release('z')
            time.sleep(1)
            keyboard.press_and_release('z')
            time.sleep(2)
            return

    no_pp_confidence = match_and_locate_template(screenshot_im, no_pp_im, low_mask)
    is_disabled_confidence = match_and_locate_template(screenshot_im, is_disabled_im, low_mask)
    if (no_pp_confidence >= CONFIDENCE_THRESHOLD) or (is_disabled_confidence >= CONFIDENCE_THRESHOLD):
            print(f"no pp : {no_pp_confidence}")
            print(f"is disabled: {is_disabled_confidence}")
            keyboard.press_and_release('x')
            time.sleep(1)
            keyboard.press_and_release('right')
            time.sleep(1+N)
            return
    

    will_you_switch_confidence = match_and_locate_template(screenshot_im, will_you_switch_im, low_mask)
    if (will_you_switch_confidence >= CONFIDENCE_THRESHOLD):
        print(f"will you switch: {will_you_switch_confidence}")
        keyboard.press_and_release('x')
        time.sleep(1)
        keyboard.press_and_release('x')
        time.sleep(1+N)
        return


    pokemon_info_confidence = match_and_locate_template(screenshot_im, pokemon_info_im, high_mask)
    if (pokemon_info_confidence >= CONFIDENCE_THRESHOLD):
        print(f"pokemon info: {pokemon_info_confidence}")
        keyboard.press_and_release('x')
        time.sleep(1)
        keyboard.press_and_release('right')
        time.sleep(1)
        keyboard.press_and_release('x')
        time.sleep(1+N)
        return

    confidence = match_and_locate_template(screenshot_im, add_to_party_im)
    if confidence >= CONFIDENCE_THRESHOLD:
        print(f"add to party: {confidence}")
        keyboard.press_and_release('x')
        time.sleep(0.5)
        keyboard.press_and_release('up')
        time.sleep(0.5)
        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('right')
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)
        keyboard.press_and_release('x')
        time.sleep(0.5)
        
        keyboard.press_and_release('down') ##down
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)
        keyboard.press_and_release('enter')
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)

        time.sleep(2)

        keyboard.press_and_release('up')
        time.sleep(1)
        keyboard.press_and_release('up')
        time.sleep(0.5)
        return


    confidence = match_and_locate_template(screenshot_im, fainted_im, low_mask)
    if confidence >= CONFIDENCE_THRESHOLD:
        print(f"fainted: {confidence}")
        keyboard.press_and_release('x')
        time.sleep(1)
        keyboard.press_and_release('x')
        time.sleep(1)
        return


    
    confidence = match_and_locate_template(screenshot_im, continue_im)
    if confidence >= CONFIDENCE_THRESHOLD:
        print(f"continue: {confidence}")
        keyboard.press_and_release('down')
        time.sleep(0.5)
        keyboard.press_and_release('z')
        time.sleep(0.5)
        return
    
    confidence_black = match_and_locate_template(screenshot_im, blank_black_im)
    confidence_green = match_and_locate_template(screenshot_im, blank_green_im)
    if (confidence_black >= CONFIDENCE_THRESHOLD) or (confidence_green >= CONFIDENCE_THRESHOLD):
        print(f"black: {confidence_black}")
        print(f"green: {confidence_green}")
        time.sleep(1+N)
        return
    
    keyboard.press_and_release('z')
    time.sleep(1+N/2)
    return





counter = 0

while True:
    start_time = datetime.datetime.now()

    with mss() as sct:

        monitor = sct.monitors[1]
        im = sct.grab(monitor)
        screenshot_im = cv.cvtColor(np.array(im), cv.COLOR_BGR2GRAY)

    # cv.imwrite(f'screenshots/output_image_{counter}.png', screenshot_im)
    counter += 1

    # screenshot_im = cv.imread(path + '\\screenshots\\screenshot.jpg', cv.IMREAD_UNCHANGED).astype(np.float32)
    # new_game_result = cv.matchTemplate(screenshot_im, new_game_im, cv.TM_CCOEFF_NORMED)
    # wants_to_learn_result = cv.matchTemplate(screenshot_im, wants_to_learn_im, cv.TM_CCOEFF_NORMED)
    # reroll_result = cv.matchTemplate(screenshot_im, reroll_im, cv.TM_CCOEFF_NORMED)
    # no_pp_result = cv.matchTemplate(screenshot_im, no_pp_im, cv.TM_CCOEFF_NORMED)
    # is_disabled_result = cv.matchTemplate(screenshot_im, is_disabled_im, cv.TM_CCOEFF_NORMED)

    # _, new_game_result_confidence, _, _ = cv.minMaxLoc(new_game_result)
    # _, wants_to_learn_confidence, _, _ = cv.minMaxLoc(wants_to_learn_result)
    # _, reroll_confidence, _, _ = cv.minMaxLoc(reroll_result)
    # _, no_pp_confidence, _, _ = cv.minMaxLoc(no_pp_result)
    # _, is_disabled_confidence, _, _ = cv.minMaxLoc(is_disabled_result)

    try:
        main()
    finally:
        end_time = datetime.datetime.now()
        time_difference = end_time - start_time
        difference_seconds = time_difference.total_seconds()
        # print(f"Time difference: {difference_seconds} seconds")

