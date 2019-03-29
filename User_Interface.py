import tkinter as tk
import tkinter.messagebox
from tkinter import ttk
import os

import Search_Engine


class UserInterface():
    def __init__(self, root):
        self.root = root
        self.root.geometry('800x600')
        self.root.config(bg='green')
        self.root.title("Search Engine ~Home Page~")

        self.searchable = False

        self.initface_home = tk.Frame(self.root, width=800, height=600, bg='green')
        self.initface_home.pack()

        #initface for load and delete botton
        self.initface_load_delete = tk.Frame(self.root, width=200, height=100, bg='green')
        self.initface_load_delete.pack(pady=20, side=tk.TOP)

        #Logo Image
        self.logo = tk.PhotoImage(file='Image/Logo.gif')
        self.w1 = tk.Label(self.initface_home, image=self.logo).pack(pady=60)

        #Combobox
        self.comvalue = tk.StringVar()
        self.comboxlist = ttk.Combobox(self.initface_home,textvariable=self.comvalue)
        self.comboxlist["values"] = ("健身")
        self.comboxlist.current(0)
        self.comboxlist.pack(pady=20)

        #User query input
        self.landString = tk.StringVar()
        self.User_Query = tk.Entry(self.initface_home, width=60, textvariable=self.landString)
        self.User_Query.pack(pady=20, side=tk.LEFT)

        #Search button
        self.resultButton = tk.Button(self.initface_home, text='Go get it!', command=self.changeInterface)
        self.resultButton.pack(padx=2, side=tk.LEFT)

        #Load data
        self.loadButton = tk.Button(self.initface_load_delete, text='Load Data!', command=self.loadData)
        self.loadButton.pack(side=tk.LEFT)

        #Delete data
        self.deleteButton = tk.Button(self.initface_load_delete, text='Delete Data!', command=self.deleteData)
        self.deleteButton.pack(padx=5, side=tk.LEFT)


    def changeInterface(self):
        if self.searchable:
            self.query = self.landString.get()
            self.initface_home.destroy()
            self.initface_load_delete.destroy()
            ContextInterface(self.root, self.query)

    def loadData(self):
        Engine = Search_Engine.Search_Engine()
        Engine.load2ES()
        tk.messagebox.showinfo(title='Congratulation!', message='Successfully load data into Elasticsearch!')
        self.searchable = True

    def deleteData(self):
        Engine = Search_Engine.Search_Engine()
        Engine.delete()
        tk.messagebox.showinfo(title='Congratulation!', message='Successfully delete data from Elasticsearch!')
        self.searchable = False





class ContextInterface():
    def __init__(self, root, query):
        self.root = root
        self.root.config(bg='black')
        self.root.title("Search Engine ~Information Page~")
        self.root.geometry('800x600')


        #Catch user question
        self.query = query

        #Search Result
        self.quotes, self.upperbound = self.Search(self.query)
        self.index = 0
        self.lowerbound = 0

        #Interface for All
        self.initface_info = tk.Frame(self.root, width=800, height=600, bg='black')
        self.initface_info.pack()

        #Interface for Logo
        self.initface_logo = tk.Frame(self.initface_info, width=800, height=30, bg='black')
        self.initface_logo.pack(pady=5, anchor='w')

        #Interface for Message
        self.initface_message = tk.Frame(self.initface_info, width=400, height=600, bg='white')
        self.initface_message.pack(padx=120, pady=50)


        #Interface for Button
        self.initface_button = tk.Frame(self.initface_info, width=60, height=30, bg='black')
        self.initface_button.pack()

        #Interface for Page Info
        self.initface_page = tk.Frame(self.initface_info, width=4, height=4, bg='black')
        self.initface_page.pack(pady=10)


        #Logo Image
        self.logo = tk.PhotoImage(file='Image/Logo2.gif')
        self.w1 = tk.Label(self.initface_logo, image=self.logo).pack()


        #Last Page Button
        self.lst_pg = tk.ttk.Button(self.initface_button, text='<- Last', style="RB.TButton", command=self.LastPage)
        self.lst_pg.pack(side=tk.LEFT)

        #Button style
        tk.ttk.Style().configure("RB.TButton", foreground='blue', background='red')
        #Back Button
        self.btn_back = tk.ttk.Button(self.initface_button, text='Back to Home Page', style="RB.TButton", command=self.backHome)
        self.btn_back.pack(side=tk.LEFT)

        #Next Page Button
        self.nxt_pg = tk.ttk.Button(self.initface_button, text='Next ->', style="RB.TButton", command=self.NextPage)
        self.nxt_pg.pack(side=tk.LEFT)


        #Page Info
        self.page_info = tk.Text(self.initface_page, wrap=tk.WORD, height=2, width=2, bg='brown')
        self.page_info.pack(side=tk.RIGHT)
        self.page_info.insert(tk.END, '1')



        #Message block
        self.scrollbar = tk.Scrollbar(self.initface_message)
        self.scrollbar.pack(fill=tk.Y, side=tk.RIGHT)

        self.text = tk.Text(self.initface_message, wrap=tk.WORD, yscrollcommand=self.scrollbar.set, bg='white')
        self.text.pack(fill=tk.BOTH)
        self.success = self.SetQuote()

        self.scrollbar.config(command=self.text.yview)




    def backHome(self):
        self.initface_info.destroy()
        UserInterface(self.root)


    def NextPage(self):
        if self.index < self.upperbound:
            self.index += 1
            self.page_info.delete(1.0, tk.END)
            self.page_info.insert(tk.END, str(self.index+1))
            self.text.delete(1.0, tk.END)
            self.EmergeMessage()


    def LastPage(self):
        if self.index > self.lowerbound:
            self.index -= 1
            self.page_info.delete(1.0, tk.END)
            self.page_info.insert(tk.END, str(self.index+1))
            self.text.delete(1.0, tk.END)
            self.EmergeMessage()


    def SetQuote(self):
        self.EmergeMessage()

        return True


    def Search(self, query):
        Engine = Search_Engine.Search_Engine()
        Result = Engine.query(query)

        return Result, len(Result)-1


    def EmergeMessage(self):
        #Set Floor color
        self.text.tag_config('topic', background="green", foreground="yellow")
        self.text.tag_config('floor', background="green", foreground="blue")

        topics = self.quotes[self.index]['title']
        topics_process = [topics[j] for j in range(len(topics)) if ord(topics[j]) in range(65536)]
        topics = ''
        for char in topics_process:
            topics += char

        article = self.quotes[self.index]['content']
        article_process = [article[j] for j in range(len(article)) if ord(article[j]) in range(65536)]
        article = ''
        for char in article_process:
            article += char

        comments = self.quotes[self.index]['comments']
        comments_process = [comments[j] for j in range(len(comments)) if ord(comments[j]) in range(65536)]
        comments = ''
        for char in comments_process:
            comments += char

        comments = comments.split('<eos>')


        self.text.insert(tk.END, topics+'\n', 'topic')
        self.text.insert(tk.END, '\n\n')
        self.text.insert(tk.END, article)
        self.text.insert(tk.END, '\n\nPost Date: {createdAt}\nLike: {likeCount}\nComment Amount: {commentCount}\n\n'.format(createdAt=self.quotes[self.index]['createdAt'],
                                                                                                                        likeCount=self.quotes[self.index]['likeCount'],
                                                                                                                        commentCount=self.quotes[self.index]['commentCount']
                                                                                                                       ))

        self.text.insert(tk.END, '\nComments:\n\n')
        floor_num = 1
        likeCount_str = self.quotes[self.index]['comments_likeCount']
        likeCount_str = likeCount_str.split('<eos>')

        for comment in comments:
            self.text.insert(tk.END, 'Floor {num}:\n'.format(num=str(floor_num)), 'floor')
            self.text.insert(tk.END, comment)
            self.text.insert(tk.END, '\nLike: {likeCount_comment}\n\n'.format(likeCount_comment=likeCount_str[floor_num-1]))
            floor_num += 1




if __name__ == '__main__':
    root = tk.Tk()
    UserInterface(root)
    root.mainloop()
