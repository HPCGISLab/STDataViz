# A class to manage log massage
# 2016/02/25
# Cheng Zhang (czhang0328@gmail.com)

class GUILog(object):
    def __init__(self,title = ""):
        self.title = "--- " + title + " ---\n"
        self.clear()
        self.lineNum = 0
        
    def add(self,s):
        self.lineNum += 1
        self.str += '[{0}]: {1}\n'.format(self.lineNum, s)
        
    def clear(self):
        self.lineNum = 0
        self.str = self.title
        
    def __repr__(self):
        '''
        the __repr__ method is what happens when you use the repr() function
        '''
        return "Log Object"
        
    def __str__(self):
        '''
        The __str__ method is what happens when you print it
        '''
        return self.str
        
def log_test():
    m_log = GUILog("This is a test Log")
    print m_log
    m_log.add("I am good")
    print m_log
    m_log.add("afsda")
    print m_log
    m_log.clear()
    print m_log
    m_log.add("afsda")
    print m_log
    
if __name__ ==  '__main__':
    log_test()