from csv import DictWriter
import csv

labels = ['url', 'name', 'vido']
dct_arr = []
hikaku = []


with open('ccv_dict2.csv', 'r') as ff:
        reader = csv.DictReader(ff)
        z = [row for row in reader]

for x in z:
    c = x['name']
    hikaku.append(c)


for i in range(1, 40):
    i +=1
    urls = {'url':f'tiko{i}', 'name':f'afaf{i}', 'vido':f'sfasf{i}' }
    dct_arr.append(urls)


with open('ccv_dict2.csv', 'a', newline='') as f:
    writer = DictWriter(f, fieldnames=labels)
    for elem in dct_arr:
        if elem['name'] not in hikaku:

            writer.writerow(elem)
        
        else :
            print('被ってるよん')





