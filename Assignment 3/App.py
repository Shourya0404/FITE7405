from tkinter import *
import tkinter.font as tkFont
from tkinter import scrolledtext
from BlackScholes import BlackScholes
from AsianOption import Asian
from BasketOption import Basket
from AmericanOption import American


class App:

    def __init__(self):

        self.window =Tk()
        self.window.title("Option Pricer")
        self.window.geometry('%dx%d' % (900, 400))
        self.menubar = Menu(self.window)
        self.window.config(menu=self.menubar)


        self.__HomePage() # Creates the homepage menu
        self.CreateOptionMenu() # Creates menu for different option pricers

        # Create frames for home page and each option pricer
        self.frameHomePage = Frame(self.window)
        self.frame1 = Frame(self.window)
        self.frame2 = Frame(self.window)
        self.frame3 = Frame(self.window)
        self.frame4 = Frame(self.window)
        self.frame5 = Frame(self.window)
        self.frame6 = Frame(self.window)
        self.frame7 = Frame(self.window) 

        # Display the homepage upon starting program
        self.__forgetFrame()
        self.frameHomePage.pack()

        # Create the home page
        Label(self.frameHomePage, text="Mini Option Pricer", font=tkFont.Font(weight='bold',size=30),height=6).pack()
        Label(self.frameHomePage, text = 'By',font=tkFont.Font(weight='bold',size=15)).pack()
        Label(self.frameHomePage, text = 'Shourya Mehra',font=tkFont.Font(weight='bold',size=15)).pack()

        self.window.mainloop() # Runs the program

    def __HomePage(self):
        
        homemenu = Menu(self.menubar, tearoff=0)
        homemenu.add_command(label = "Load Homepage",command = self.load_home)
        homemenu.add_command(label = "Quit", command = self.quit)
        self.menubar.add_cascade(label = 'Program Options', menu = homemenu)

    # Load the HomePage
    def load_home(self):
        self.__forgetFrame()
        self.frameHomePage.pack()
    
    # Quit the Application
    def quit(self):
        self.window.destroy()

    # For switching pages, forget the current page and jump to another page
    def __forgetFrame(self): 
        self.frameHomePage.pack_forget()
        self.frame1.pack_forget()
        self.frame2.pack_forget()
        self.frame3.pack_forget()
        self.frame4.pack_forget()
        self.frame5.pack_forget()
        self.frame6.pack_forget()
        self.frame7.pack_forget()

    # Menu containing different pricers
    def CreateOptionMenu(self):
        pricingmenu = Menu(self.menubar, tearoff=0)
        pricingmenu.add_command(label = "Black Scholes", command = self.task1)
        pricingmenu.add_command(label = "Geometric Asian", command = self.task2)
        pricingmenu.add_command(label = "Geometric Basket", command = self.task3)
        pricingmenu.add_command(label = "Arithmetic Asian", command = self.task4)
        pricingmenu.add_command(label = "Arithmetic Basket", command = self.task5)
        pricingmenu.add_command(label = "American", command = self.task6)
        pricingmenu.add_command(label = "Implied Volatility", command = self.task7)
        self.menubar.add_cascade(label = 'Pricing Models', menu = pricingmenu)

    def task1(self):
        self.__forgetFrame()
        frame = self.frame1 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Black Scholes Price for European Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Repo Rate').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7,column=2,sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task1).grid(row = 10, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task1).grid(row = 10, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 11, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task1(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.q = 0
        self.task1()

    def calculate_task1(self):
        try:
            option = BlackScholes()
            result =option.euro_vanilla(float(self.S.get()),float(self.K.get()),float(self.T.get()),float(self.sigma.get()),float(self.r.get()),float(self.q.get()),self.option_type.get())
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

    def task2(self):
        self.__forgetFrame()
        frame = self.frame2 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Closed Form Price for Geometric Asian Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Observation Times').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.n).grid(row=7,column=2,sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task2).grid(row = 10, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task2).grid(row = 10, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 11, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task2(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.task2()

    def calculate_task2(self):
        try:
            option = Asian(float(self.S.get()),float(self.K.get()),float(self.T.get()),float(self.sigma.get()),float(self.r.get()),int(self.n.get()),self.option_type.get())
            result =option.geometric_asian()
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

    def task3(self):
        self.__forgetFrame()
        frame = self.frame3 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Closed Form Price for Geometric Basket Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 1st Asset').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 2nd Asset').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Volatility of 1st asset').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Volatility of 2nd asset').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Correlation between Assets').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=10,column=1,sticky=W)

        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.rho = StringVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S1).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8,column=2,sticky=W)
        Entry(frame, textvariable=self.rho).grid(row=9,column=2,sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=10, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=10, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task3).grid(row = 11, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task3).grid(row = 11, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 13, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task3(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.rho = 0
        self.task3()

    def calculate_task3(self):
        try:
            option = Basket([float(self.S1.get()),float(self.S2.get())],float(self.K.get()),float(self.T.get()),[float(self.sigma1.get()),float(self.sigma2.get())],float(self.r.get()),float(self.rho.get()),self.option_type.get())
            result =option.geometric_basket()
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

    def task4(self):
        self.__forgetFrame()
        frame = self.frame4 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Price for Arithmetic Asian Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text = "Standard Monte Carlo or Control Variate Method").grid(row = 1, column = 2)
        Label(frame, text= 'Spot Price').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Observation Times').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Number of Paths in Monte Carlo').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Use Control Variate').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=10,column=1,sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.n = StringVar()
        self.M = StringVar()
        self.control_variate = BooleanVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.n).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.M).grid(row=8,column=2,sticky=W)

        # Check button to select whether or not to use control variate
        Checkbutton(frame, text="Control Variate?", variable=self.control_variate).grid(row=9, column=2, sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=10, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=10, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task4).grid(row = 11, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task4).grid(row = 11, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 12, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task4(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.n = 0
        self.M = 0
        self.task4()

    def calculate_task4(self):
        try:
            option = Asian(float(self.S.get()),float(self.K.get()),float(self.T.get()),float(self.sigma.get()),float(self.r.get()),int(self.n.get()),self.option_type.get(),int(self.M.get()),self.control_variate.get())
            result, interval =option.arithmetic_asian()
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
            self.logs.insert(END, "The confidence interval is: {}\n".format(interval))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

    def task5(self):
        self.__forgetFrame()
        frame = self.frame5 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Price for Arithmetic Basket Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text = "Standard Monte Carlo or Control Variate Method").grid(row = 1, column = 2)
        Label(frame, text= 'Spot Price of 1st Asset').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Spot Price of 2nd Asset').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Volatility of 1st asset').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Volatility of 2nd asset').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=8,column=1,sticky=W)
        Label(frame, text= 'Correlation between Assets').grid(row=9,column=1,sticky=W)
        Label(frame, text= 'Number of Paths in Monte Carlo').grid(row=10,column=1,sticky=W)
        Label(frame, text= 'Use Control Variate').grid(row=11,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=12,column=1,sticky=W)

        self.S1 = StringVar()
        self.S2 = StringVar()
        self.K = StringVar()
        self.sigma1 = StringVar()
        self.sigma2 = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.rho = StringVar()
        self.M = StringVar()
        self.control_variate = BooleanVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S1).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.S2).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma1).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma2).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=7,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=8,column=2,sticky=W)
        Entry(frame, textvariable=self.rho).grid(row=9,column=2,sticky=W)
        Entry(frame, textvariable=self.M).grid(row=10,column=2,sticky=W)
        
        # Check button to select whether or not to use control variate
        Checkbutton(frame, text="Control Variate?", variable=self.control_variate).grid(row=11, column=2, sticky=W)

        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=12, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=12, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task5).grid(row = 13, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task5).grid(row = 13, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height = 8)
        self.logs.grid(row = 14, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task5(self):
        self.S1 = 0
        self.S2 = 0
        self.K = 0
        self.sigma1 = 0
        self.sigma2 = 0
        self.r = 0
        self.T = 0
        self.rho = 0
        self.M = 0
        self.task5()

    def calculate_task5(self):
        try:
            option = Basket([float(self.S1.get()),float(self.S2.get())],float(self.K.get()),float(self.T.get()),[float(self.sigma1.get()),float(self.sigma2.get())],float(self.r.get()),float(self.rho.get()),self.option_type.get(),int(self.M.get()),self.control_variate.get())
            result =option.arithmetic_basket()
            result, interval =option.arithmetic_basket()
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
            self.logs.insert(END, "The confidence interval is: {}\n".format(interval))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")
        

    def task6(self):
        self.__forgetFrame()
        frame = self.frame6 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Binomial Tree Price for American Call/Put Options", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Volatility').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Number of Steps').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.sigma = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.N = StringVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.sigma).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.N).grid(row=7,column=2,sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task6).grid(row = 10, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task6).grid(row = 10, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 11, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task6(self):
        self.S = 0
        self.K = 0
        self.sigma = 0
        self.r = 0
        self.T = 0
        self.N = 0
        self.task6()

    def calculate_task6(self):
        try:
            option = American(float(self.S.get()),float(self.K.get()),float(self.T.get()),float(self.sigma.get()),float(self.r.get()),int(self.N.get()),self.option_type.get())
            result =option.binomial_tree()
            self.logs.insert(END, "The Option Premium is: {}\n".format(result))
        except:       
            self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

    def task7(self):
        self.__forgetFrame()
        frame = self.frame7 
        frame.pack() # Place current frame in the window

        # Labels to show params
        Label(frame, text = "Implied Volatility Calculator", font = tkFont.Font(size = 11, weight = 'bold')).grid(row=1,column=1,sticky=W)
        Label(frame, text= 'Spot Price').grid(row=2,column=1,sticky=W)
        Label(frame, text= 'Strike Price').grid(row=3,column=1,sticky=W)
        Label(frame, text= 'Option Premium').grid(row=4,column=1,sticky=W)
        Label(frame, text= 'Risk Free Rate').grid(row=5,column=1,sticky=W)
        Label(frame, text= 'Time to Maturity (in years)').grid(row=6,column=1,sticky=W)
        Label(frame, text= 'Repo Rate').grid(row=7,column=1,sticky=W)
        Label(frame, text= 'Option Type: Call or Put').grid(row=8,column=1,sticky=W)

        self.S = StringVar()
        self.K = StringVar()
        self.option_price = StringVar()
        self.r = StringVar()
        self.T = StringVar()
        self.q = StringVar()
        self.option_type = StringVar()

        # Entry widgets to input values
        Entry(frame, textvariable=self.S).grid(row=2,column=2,sticky=W)
        Entry(frame, textvariable=self.K).grid(row=3,column=2,sticky=W)
        Entry(frame, textvariable=self.option_price).grid(row=4,column=2,sticky=W)
        Entry(frame, textvariable=self.r).grid(row=5,column=2,sticky=W)
        Entry(frame, textvariable=self.T).grid(row=6,column=2,sticky=W)
        Entry(frame, textvariable=self.q).grid(row=7,column=2,sticky=W)
        
        # Radio Button to select call or put
        Radiobutton(frame, text="Put",variable=self.option_type, value='put').grid(row=8, column=2,sticky=E)
        Radiobutton(frame, text="Call", variable=self.option_type, value='call').grid(row=8, column=2, sticky =W)

        # Reset input and log
        Button(frame, width = 20, text = "Reset Inputs",command=self.reset_task7).grid(row = 10, column = 1, columnspan = 1, sticky = E)
        
        # define run button to run the pricer
        Button(frame, width = 20, text = "Calculate",command=self.calculate_task7).grid(row = 10, column = 2, columnspan = 1, sticky = W)

        # define a window to display result
        self.logs = scrolledtext.ScrolledText(frame, width = 74, height =8)
        self.logs.grid(row = 11, column = 1, rowspan = 4, columnspan = 2, sticky = W)

    def reset_task7(self):
        self.S = 0
        self.K = 0
        self.option_price = 0
        self.r = 0
        self.T = 0
        self.q = 0
        self.task7()

    def calculate_task7(self):
        try:
            option = BlackScholes()
            result =option.get_implied_volatility(float(self.S.get()),float(self.K.get()),float(self.T.get()),float(self.r.get()),float(self.q.get()),float(self.option_price.get()),self.option_type.get())
            self.logs.insert(END, "The Implied Volatility is: {}\n".format(result))
        except:       
           self.logs.insert(END, "Input Parameter Error! Please input the correct parameters!\n")

        
if __name__ == '__main__':
    
    App()