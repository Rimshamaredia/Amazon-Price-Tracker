import time
from datetime import datetime

from Tracker import inputDetails, sendEmail, checkPrice, getTime


print("~ Amazon Price Tracker ~")
data_dict = inputDetails()
iters = 0  # counts the number of price checks done
while True:
    iters += 1
    print("\nCheck #", iters, "on:", datetime.today())
    # check if the price has dropped
    try:
        checkPrice(data_dict)
    except Exception as e:
        if e != "SystemExit":
            print("\nSorry! Price tracking attempt failed.")
            exit()
    
    # print the frequency of price checks
    print("Price will be checked every " + getTime(data_dict["often"]))
    print("Interrupt keyboard to stop. (Ctrl+C)")
    time.sleep(data_dict["often"])
