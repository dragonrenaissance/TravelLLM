    

from llm import *
import requests
import urllib
url = "https://www.viator.com/tours/Big-Island-of-Hawaii/Snorkel-and-Dolphin-Adventure/d669-15509P1"

url_2_work = "https://www.viator.com/tours/Big-Island-of-Hawaii/Kona-Tradewind-Sail/d669-2774P37"

url_not_work =  "https://www.viator.com/tours/Big-Island-of-Hawaii/Viator-Exclusive-Wildlife-guaranteed-snorkel-and-lunch-in-Kona/d669-2774P21"

value = "1/2/3"
encodedValue = urllib.parse.quote_plus(value)
print(value)
print(encodedValue)

print(CruateGen(url_not_work))


