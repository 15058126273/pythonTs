# encoding=utf-8


file = open('files/all_msg.txt', 'wb')
file1 = open('files/1000.txt', 'rb')
file2 = open('files/2000.txt', 'rb')
file3 = open('files/3000.txt', 'rb')
file4 = open('files/4000.txt', 'rb')
file5 = open('files/4077.txt', 'rb')
file6 = open('files/5077.txt', 'rb')
file7 = open('files/6077.txt', 'rb')
file8 = open('files/7077.txt', 'rb')
file9 = open('files/8077.txt', 'rb')
file10 = open('files/9077.txt', 'rb')
file11 = open('files/9851.txt', 'rb')
file12 = open('files/19851.txt', 'rb')
file13 = open('files/29851.txt', 'rb')

all_msg = file1.read()+file2.read()+file3.read()+file4.read()+file5.read()+file6.read()+file7.read() + \
          file8.read()+file9.read()+file10.read()+file11.read()+file12.read()+file13.read()
file.write(all_msg)

file.close()
file1.close()
file2.close()
file3.close()
file4.close()
file5.close()
file6.close()
file7.close()
file8.close()
file9.close()
file10.close()
file11.close()
file12.close()
file13.close()
