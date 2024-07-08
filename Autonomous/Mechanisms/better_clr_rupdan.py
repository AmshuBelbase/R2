import sys
from time import sleep
from machine import Pin, SoftI2C

from tcs34725 import *  # class library

"""def is_purple(r, g, b):
    Check if the color follows the purple ratio pattern 
    if g == 0 or b == 0:
        return False  # Avoid division by zero

    r_g_ratio = r / g
    r_b_ratio = r / b
    g_b_ratio = g / b

    # Adjusted ratios and thresholds for more accurate detection
    return (2.50 <= r_g_ratio <= 3.00 and
            1.20 <= r_b_ratio <= 2.80 and
            0.60 <= g_b_ratio <= 1.00)
"""
def detect_color(counts_history):
    """ Determine the color based on the largest value being consistent for 3 consecutive readings """
    #p_max = all((counts[1] > counts[2] and counts[1] > counts[3]) and counts[2] > counts[3] for counts in counts_history)
    p_max = False
    b_max = False
    r_max = False
    g_max = False
    for counts in counts_history:
        if (counts[1] > counts[2] and counts[1] > counts[3] and counts[3] > counts[2]):
            #if(counts[3] > counts[2]):
                p_max=True
        elif (counts[1] > counts[2] and counts[1] > counts[3]):
            r_max=True
        elif (counts[2] > counts[1] and counts[2] > counts[3]):
            g_max=True
        elif (counts[3] > counts[2] and counts[3] > counts[1]):
            b_max=True
        
    '''   
    r_max = all(counts[1] > counts[2] and counts[1] > counts[3] for counts in counts_history)
    g_max = all(counts[2] > counts[1] and counts[2] > counts[3] for counts in counts_history)
    b_max = all(counts[3] > counts[1] and counts[3] > counts[2] for counts in counts_history)
    '''
    
                
            
    
    if p_max:
        return "Purple"
    elif r_max:
        return "Red"
    elif g_max:
        return "-"
    elif b_max:
        return "Blue"
    else:
        return "-"

def main():
    print("Starting tcs34725_test program")
    if sys.platform == "pyboard":  # test with PyBoard
        tcs = TCS34725(scl=Pin("B6"), sda=Pin("B7"))  # instance of TCS34725 on pyboard
    else:  # test with ESP32 board
        tcs = TCS34725(scl=Pin(9), sda=Pin(8))  # instance of TCS34725 on ESP32
    if not tcs.isconnected:  # terminate if not connected
        print("Terminating...")
        sys.exit()
    tcs.gain = TCSGAIN_LOW
    tcs.integ = TCSINTEG_HIGH
    tcs.autogain = False  # use autogain!

    counts_history = []

    print(" Clear   Red Green  Blue    gain  >")
    try:
        while True:  # forever
            """ show color counts """
            counts_tuple = tcs.colors  # obtain all counts
            counts = list(counts_tuple)  # list of 4 counts
            for count in counts_tuple:
                # show 'absolute' light value (count / gain-factor)
                if count >= tcs.overflow_count:  # overflow?
                    count = -1  # overflow reported as count -1
                print(" {:5d}".format(count // tcs.gain_factor), end="")
            
            counts_history.append(counts)
            if len(counts_history) > 3:
                counts_history.pop(0)  # keep only the last 3 readings

            if len(counts_history) == 3:
                color = detect_color(counts_history)
            else:
                color = "-"

            red = counts[1]
            green = counts[2]
            blue = counts[3]

            """if color == "-" and is_purple(red, green, blue):
                color = "Purple"
                 """

            print("    ({:2d})  {:s}" .format(tcs.gain_factor, color))
            sleep(0.15)  # interval between reads

    except KeyboardInterrupt:
        print("Closing down!")

    except Exception as err:
        print("Exception:", err)

    tcs.close()

main()
