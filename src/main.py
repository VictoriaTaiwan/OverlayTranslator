import sys 

from views.app import App    
class Main:    
    def __init__(self):
        self.app = App(args = sys.argv)           
        
if __name__ == "__main__":
    main = Main()