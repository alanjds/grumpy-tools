print 'Importing:' + __name__

__all__ = ['PRE_EHLO', 'hello', 'POST_EHLO']

PRE_EHLO = 1

def hello():
    print "hello, world"

POST_EHLO = 1

print 'Done:' + __name__
