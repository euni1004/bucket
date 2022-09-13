list_di = [ {'Name': 'Tom', 'Age': 30}, {'Name': 'Jack', 'Age': 31}, {'Name': 'Sue', 'Age': 32} ]

a_list=[]
for i in list_di:
    a_list.append(i['Age'])

print(max(a_list))