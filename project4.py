#1a - Create a tuple of the following numbers 1,2,3,4,5

number1to5 = tuple([1, 2, 3, 4, 5])
print(number1to5)



#1b - Use this tuple as an iterable to show the squared terms instead. 

#Hmm, something isn't working... (hint it's a small review of 'for' loops) 

for value in number1to5:
 print(value**2) #something isn't working right.. fix it!🔨


#2 - I'm trying to split the following tuple into two separate lists...

#but I want it sorted first. Help me out 🙂

year_value = ((2020,45),(1980,23),(2004,55),(1995,11))

###Add ONE line here 😀
year_value = sorted(year_value)

###

year_list = []
value_list = []

for year, value in year_value:

 year_list.append(year)

 value_list.append(value)

print(year_list)
print(value_list)


#3 - Oops, it was supposed to be Jan Smith... can you replace with RegEx?

import re

messy_data = "<id value='jan.sith.$D2019-12-01$T10:45:00Z-85354-9'/>"
new_match = re.sub(r"jan\.sith", "jan.smith", messy_data)
print(new_match)



#4 - Can you also extract the date?
import re
messy_data = "<id value='jan.sith.$D2019-12-01$T10:45:00Z-85354-9'/>"

#Hint: Take it one step at a time! Notice how there is a $ between the date? Try to split...

#Hint: after splitting, look at the list you made... just select the correct item such as split_messy_data[1]

split_messy_data = (re.split(r"\$", messy_data))# First, complete the code to split
print(split_messy_data)

date = split_messy_data[1]
print(date)

new_date = date[1:]  # Remove the first character 'D'
print(new_date)
