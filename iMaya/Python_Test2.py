from operator import *

inventory = [('apple', 3), ('banana', 2), ('pear', 5), ('orange', 1)]
getcount = itemgetter(1)
print map(getcount, inventory)
print sorted(inventory, key=getcount)
#print inventory