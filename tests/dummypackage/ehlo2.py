print 'Importing:' + __name__

__all__ = ['PRE_EHLO2', 'ehlo', 'imported', 'POST_EHLO2']

PRE_EHLO2 = 1

import ehlo

ehlo.hello()

try:
    imported = ehlo.PRE_EHLO
except Exception as e:
    print(e)    

POST_EHLO2 = 1

print 'Done:' + __name__
