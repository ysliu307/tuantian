import random

U=0
k=0
count_user=0
count=0
with open('sort_data.txt', 'r') as g:
	data1 =g.readlines()
	D1=data1[0].split('\t')
	id_former=int(D1[0])
	count_user_former=0
	train_file = open('train_data.tsv', 'w')
	test_file = open('test_data.tsv', 'w')
	
	while(U<943):
		D=data1[k].split('\t')
		if len(D)!=4:
			continue
		k+=1
		current_id=int(D[0])
		if(current_id!=id_former):
			count_user = count_user_former+ int(count)
			m = -1
			flag = False
			train = []
			test = []
			for j in range(count_user_former, count_user):
				Dp=data1[j].split('\t')
				if(int(Dp[2])>=3):
					train.append(j)
				if(int(Dp[2])<3):
					test.append(j)
			array_index = random.randint(0, len(train) - 1)
			index = train[array_index]
			train = set(train)
			test = set(test)
			for j in range(count_user_former, count_user):
				elements = data1[j].split('\t')
				if j == index:
					flag = True
					test_file.write("%s %s %s\n" %(elements[0], elements[1], 1))
					
				else:
					if j in train:
						train_file.write("%s %s %s\n" %(elements[0], elements[1], 1))
					else:
						train_file.write("%s %s %s\n" %(elements[0], elements[1], 0))
					
			if flag == False:
				print(str(U) + ", " + str(index) + ": " + str(count_user_former) + ", " + str(count_user))
			id_former=current_id
			U=U+1
			count_user_former = count_user
			count=1
		else:
			count+=1
		
		if(k==len(data1)):
			break
			

train_file.close()
test_file.close()

