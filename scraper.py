#
# 1/26/14
# Web Scraper written in Python3
# Author Tim Toliver <timotet@hotmail.com>
# 
#
# The scraper takes a url or a list of url's and 
# searches for a specified string, if the string is found 
# the scraper creates a log file with just the url's listed 
# that the searched for string was in.
# When running the program a GUI pops up with dialog box's to add
# what to search for , where to load the search list from , and where to 
# put the log file. All file open dialogs default to users my documents.
#
# This script takes advantage of the awesome beautiful soup module!
#
# This is free software, use to your liking but give credit where it's due

from tkinter import *   
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from tkinter.ttk import Progressbar, Sizegrip
from urllib.request import urlopen
from bs4 import BeautifulSoup

class Window(Frame):
    
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window() 
    
    def init_window(self):
        # master window
        self.master.title("Scraper")
        
        # labels
        l1 = Label(self.master, text='Lets do some scraping, fill in the fields and hit search. Then enjoy!', fg="red")
        l1.grid(column=0, row=0, columnspan=4)
        l2 = Label(self.master, text="url or list of url's to search:")
        l2.grid(column=0, row=4)
        l3 = Label(self.master, text="location to save to:")
        l3.grid(column=0, row=5)
        l4 = Label(self.master, text="String to search for:", fg="blue")
        l4.grid(column=0, row=3)
   
        # buttons
        #b1 = Button(self.master, text="secret", command=self.secret, bg="green", activebackground="orange")
        #b1.grid(column=0, row=0, sticky=W)
        b2 = Button(self.master, text="quit", command=self.quit, fg="red", activebackground="red")
        b2.grid(column=0, row=6, sticky=W, padx=5) 
        b3 = Button(self.master, text="Browse", command=self.browse1, bg="lime", activebackground="tan")
        b3.grid(column=3, row=4, sticky=E) 
        b4 = Button(self.master, text="Browse", command=self.browse2, bg="lime", activebackground="tan")
        b4.grid(column=3, row=5, sticky=E) 
        b5 = Button(self.master, text="Search", command=self.search, bg="orange", activebackground="pink")
        b5.grid(column=3, row=6, sticky=W)
        
        # Data Entry
        self.e1 = Entry(self.master)                # default relief is SUNKEN
        self.e1.grid(column=1, row=4, sticky=(W,E), pady=5, ipady=3)
        self.e2 = Entry(self.master)
        self.e2.grid(column=1, row=5, sticky=(W,E), pady=5, ipady=3)
        self.e3 = Entry(self.master)
        self.e3.grid(column=1, row=3, sticky=(W,E), pady=5, ipady=3)
        
        # Sizegrip
        self.sg = Sizegrip(self.master).grid(column=999, row=999, sticky=(S,E))
        self.master.rowconfigure(0, weight=1)  
        self.master.columnconfigure(0, weight=1)  # these make sizegrip work
        
        # Progressbar
        self.pb = Progressbar(self.master, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.pb.grid(column=1, row=6, sticky=W)
        
    # pop-up for file open dialog
    def browse1(self):
        
        fname = askopenfilename(initialdir='C:/Users', title="Browse to file", filetypes=(("Text files", "*.txt"),
                                                                                                            ("All files", "*.*")))
        if fname:
            try:
                self.e1.insert(0, fname) # insert the file path into the dialog box
                print(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        
    # pop-up for file save dialog        
    def browse2(self):
        
        # this gives a dialog that asks for a file name to save and returns the file. It also creates the file in the location given
        fname = asksaveasfilename(initialdir='C:/Users', title="Browse to file", defaultextension=".txt", 
                                  filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if fname:
            try:
                self.e2.insert(0, fname)
                print(fname)
            except:                     # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'" % fname)
        
    def quit(self):  
        exit() 
        
    def urlSearch(self, url, logFile, sText):
        
        count = 0
        with open(logFile, "a") as f:  # append to the above created file
        
            with urlopen(url) as html:
                
                f.write("\n")
                f.write("Website:\n")
                f.write(url)
                f.write("\n")
                
                soup = BeautifulSoup(html) # create beautifulsoup object
                #print("pretty")
                #print(soup.prettify())
                print("")
                print("original encoding is: %s" % soup.original_encoding)
                #f.write("original encoding of webpage: \n")
                #f.write(soup.original_encoding)
                #f.write("\n")
                #f.write("\n")
                print("")
                
                #print("find text")
                print("string to look for:")
                print(sText)
                f.write("String to look for: \n")
                f.write(sText)
                f.write("\n")
                f.write("\n")
                
                """
                # these do the same thing
                data = soup.find(text=sText)
                print("data = %s" %data)
                if data == sText:
                    # print("in if test")
                    #text = soup.getText(sText)
                    print(data)
                    count += 1  # update the counter
                    print("found text")
                """
                
                data = []
                data = soup.find_all(text=sText)
                print("data = %s" %data)
                
                for i in range(0,len(data)):
                    
                    if data[i] == sText:
                        # print("in if test")
                        print(data[i])
                        count += 1  # update the counter
                        print("found text")
                        
                
                    
                print("Text string found %i times" % count)
                f.write("Text string found %i times" % count)
                f.write("\n")
                f.write("**************************************************************")
                f.write("\n")
                
                self.pb.step()
                self.pb.update_idletasks()
                
                print()
                print("Done")  
        
    def search(self):
        
        self.pb.start(5)   # start the progressbar with 5 millisecond interval
        
        # get the text out of the entry widget
        url = self.e1.get()      # url or list of url's
        logLoc = self.e2.get()   # location to save to log file to
        sText = self.e3.get()    # string to search for
        
        print(url)
        #print(type(url))
        print(sText)
        print(type(sText))      
        print(logLoc)
            
        # Lets parse the string from the dialog box
        # This case is if a url is typed directly into the dialog box
        if url[0] == "h" and url[1] == "t" and url[2] == "t" and  url[3] == "p":
            # print("in if")
            self.urlSearch(url, logLoc, sText)
                
        else:
            # This case is to support opening a file and getting the url or url's
            lineCount = 0
            with open(url) as f:
                for lines in f:
                    URL = f.readline()
                    # print(URL)
                    # If there is a empty line in the file pass
                    if URL in ['\n', '\r\n']:
                        print("emptyline found")
                        #pass
                    # if its the end of the file break out of the loop
                    elif URL == '':
                        break
                    else:
                        self.urlSearch(URL, logLoc, sText)
                        lineCount += 1
    
            print("%i lines read" % lineCount)
             
        self.pb.stop()  # stop the progressbar
        
        self.e1.delete(0,END)  # delete the text from the entry widget
        self.e2.delete(0,END)
        self.e3.delete(0,END)
        
        self.master.destroy() # after the search is finished close the window
        
def main():
    
    print("Here we go!")
    root = Tk()
    app = Window(root)
    root.mainloop()  
      
if __name__ == '__main__':
    main()