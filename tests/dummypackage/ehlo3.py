print 'Importing:' + __name__

PRE_EHLO3 = 1

import ehlo2

try:
    imported = ehlo2.PRE_EHLO2
except Exception as e:
    print(e)    

POST_EHLO3 = 1

print 'Done:' + __name__

