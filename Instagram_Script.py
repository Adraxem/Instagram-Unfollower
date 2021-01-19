import tkinter as tk
import time
from Instagram_class import followerr
from selenium import webdriver
import csv




#Opening a tkinter window and assigning text messages to it and designating geometry w.r.t. pixels
window = tk.Tk()
window.title('Instagram Script')
window.geometry('480x110')
lab = tk.Label(window,text='Enter Your instagram ID, phone number or mail adress please: ')


#Embedding entry boxes into tkinter interface for users to enter their ID and password
entre = tk.Entry(window)
label = tk.Label(window,text='Enter your instagram password please: ')
eentry = tk.Entry(window)


def input1():

    #obtaining user ID from the entry box inside tkinter interface
    global ID
    ID = entre.get()


    #obtaining user password from the entry box inside tkinter interface
    global passwort
    passwort = eentry.get()


    #assigning valuables for future use and destroying the tkinter interface after the data has been gathered.
    global path
    global driver
    global a
    window.destroy()


    #Declaring the selenium's (chromedriver.exe) and it's destination(where that executable file is inside computer).
    path = 'C:\Program Files (x86)\chromedriver.exe'


    #opening selenium's web driver and assigning the driver, and redirecting the driver to the website where we execute.
    driver = webdriver.Chrome(path)
    driver.get('https://www.instagram.com/')
    time.sleep(0.4)


    #finding username and password entry boxes in instagram website, and sending them the data acquired from entry boxes.
    a = driver.find_element_by_name('username')
    a.send_keys(ID)
    b = driver.find_element_by_name('password')
    b.send_keys(passwort)


    #Click the login button to access the instagram page we'd like to execute.
    c = driver.find_elements_by_tag_name('button')
    time.sleep(0.3)
    (c[1]).click()
    time.sleep(5)


    #accessing profile through clicking the profile buttons on instagram interface.
    profile = driver.find_element_by_class_name('_6q-tv')
    profile.click()
    time.sleep(0.1)
    in_profile = driver.find_element_by_class_name('-qQT3')
    in_profile.click()
    time.sleep(3)


    #accessing follower bar via clicking it, the window that we gather data from opens.
    follower = driver.find_elements_by_class_name('Y8-fY ')[1]
    follower.click()
    time.sleep(0.5)
    e1_space = driver.find_element_by_class_name('_1XyCr')
    e1_space.click()
    time.sleep(0.3)


    #Executing the very same operation for acquiring the 'following' data and access everyone that we follow.
    r = '\t'
    path = 'C:\Program Files (x86)\chromedriver.exe'
    driver1 = webdriver.Chrome(path)
    driver1.get('https://www.instagram.com/')
    time.sleep(0.4)
    a = driver1.find_element_by_name('username')
    a.send_keys(ID)
    b = driver1.find_element_by_name('password')
    b.send_keys(passwort)
    c = driver1.find_elements_by_tag_name('button')
    time.sleep(0.3)
    (c[1]).click()
    time.sleep(7)
    profile = driver1.find_element_by_class_name('_6q-tv')
    profile.click()
    time.sleep(0.1)
    in_profile = driver1.find_element_by_class_name('-qQT3')
    in_profile.click()
    time.sleep(3)
    follower = driver1.find_elements_by_class_name('Y8-fY ')[2]
    follower.click()
    time.sleep(0.4)



    #To obtain all the follower data, the follower page needs to be scrolled down,
    # until there is no account left to scroll down.
    #Hence this can only be done by executing some javascript commands, this part of the script sends some javascript
    #commands to website for it to execute, which perfectly scrolls down.
    jsKomut = '''
        sayfa = document.querySelector(".isgrP");
                        sayfa.scrollTo(0,sayfa.scrollHeight);
                        var sayfaSonu = sayfa.scrollHeight;
                        return sayfaSonu;
        '''
    sayfaSonu = driver.execute_script(jsKomut)


    #A While loop needs to be executed because how long will it take is unpredictable.
    while True:
        son = sayfaSonu
        time.sleep(0.5)
        sayfaSonu = driver.execute_script(jsKomut)

        #stating that if we had reached the end of the page, following will be executed.
        if son == sayfaSonu:
            time.sleep(5)
            count = 0


            #finding all accounts that follows us using selenium function and assigning it to takiped variable.
            takiped = driver.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")


            #Opening a csv file which is handy for large data storing and writing all the followers of us into that file.
            with open('followers.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter='\n')


            #Iterating over the ones that follow us, so that we can append them to a csv file.
            for takipci in takiped:
                p = []
                t = []
                p.append(takipci.text)

                #actually there was literally no need for me to do this LOL.
                followerr(p[0], takipci)

                count += 1


                #appending all the followers to the new opened csv file.
                with open('followers.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(p)
            csvfile.close()
            break
    sayfaSonu1 = driver1.execute_script(jsKomut)


    #Now this While loop is doing both comparison and csv file writing job.
    while True:
        son = sayfaSonu1
        if son == sayfaSonu1:
            time.sleep(5)
            count = 0

            #obtaining all the data that followed by us, the 'following' ones.
            #Opening a new csv file to append and read all the data from it once it has stored.
            #Again gathering following data using selenium function driver.find_element_...
            takipciler = driver1.find_elements_by_css_selector(".FPmhX.notranslate._0imsa")
            with open('following.csv', 'w', newline='') as csvfile:
                spamwriter = csv.writer(csvfile, delimiter='\n')
            u = []


            #appending all the followings to a list.
            for takip in takipciler:
                u.append(takip.text)

            for takipci in takipciler:
                p = []
                p.append(takipci.text)
                count += 1


                #Same, writing and appending to a csv file.
                with open('following.csv', 'a', newline='') as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=' ', quoting=csv.QUOTE_MINIMAL)
                    spamwriter.writerow(p)
                with open('followers.csv', 'r') as file:
                    reader = csv.reader(file)
                    j = []
                    for row in reader:
                        j.append(row[0])



                    #Now, here's the interesting part. While trying to make selenium press the unfollow button,
                    #i discovered something that is hidden in it's xpath variable.
                    #and using that xpath variable trick, i managed to make program do all the work by itself.
                    #Also, made it click using selenium.
                    if (takipci.text) not in j:
                        n = (u.index(takipci.text))+1
                        o = driver1.find_elements_by_xpath('/html/body/div[5]/div/div/div[2]/ul/div/li[{}]/div/div[3]/button'.format(n))
                        o[0].click()
                        time.sleep(0.4)
                        letgo = driver1.find_element_by_xpath('/html/body/div[6]/div/div/div/div[3]/button[1]')
                        letgo.click()
                        time.sleep(0.8)
                continue

        break



#tkinter interface necessary requirement commands for it to work.
but = tk.Button(window,text='Proceed!',command = input1)
lab.pack()
entre.pack()
label.pack()
eentry.pack()
but.pack()
window.mainloop()

#Vielen Dank!
#Ardacan YILDIZ-19.01.2021
