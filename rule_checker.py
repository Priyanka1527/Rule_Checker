#Author: Priyanka Saha

import pandas
import itertools


#user defined function definitions
def case_compare(data,attribute,value,concept,decision):
	flag = 0
	

	global complete_classified_correct, complete_classified_incorrect, classified_not
	
	row = data.shape[0]
	column = data.shape[1]
	len1 = len(attribute)
	new_header = data.iloc[0] #grab the first row for the header
	data = data[1:] #take the data less the header row
	data.columns = new_header #set the header row as the df header
	headerlist = list(data.columns.values) #to get the headers of the table
	header_list_length = len(headerlist) #length of the headerlist
	
	

	#checking each case if being matched by the rule completely
	for index, row in data.iterrows():
		
		k=0
		for item in attribute:
			if(".." in value[k]): #checking ifthe value is numerical interval
				value_range = value[k].split("..")
				value_left = value_range[0]
				value_right = value_range[1]
				if(value_left <= row[item] <=  value_right or row[item] == '*' or row[item] == '-' ): #The closed interval range is considered while checking
					flag = 1
					k = k+1
				else:
					flag = 0
					break
			else:
				if(row[item] == value[k] or row[item] == '*' or row[item] == '-' ):
					flag = 1
					k = k+1
				else:
					flag = 0
					break
		
		if(flag == 1):
			dec = data.iloc[index-2,header_list_length-1]
			if(dec == decision[0]):
				complete_classified_correct.append(index-2)
				
				
			else:
				complete_classified_incorrect.append(index-2)
				

		else:
			classified_not.append(index-2)
	

	#-----print the list of cases---------		
		
	#print("\n\nCorrectly classified: ")	
	#for j in complete_classified_correct:
	#	print("Case: ", j+1, " ")
	#	for k in range(0,header_list_length):
	#		print(data.iloc[j,k], end=' ')
	#	print("\n")
	#print("\nTotal number of cases that are Correctly classified: ", len(complete_classified_correct))


	#print("\n\nIncorrectly classified: ")
	#for j in classified_incorrect:
	#	print("Case: ", j, " ")
	#	for k in range(0,header_list_length):
	#		print(data.iloc[j,k], end=' ')
	#	print("\n")
	#print("\nTotal number of cases that are Incorrectly classified: ", len(classified_incorrect))


	#print("\n\nNot classified: ")
	#for j in classified_not:
	#	print("Case: ", j+1, " ")
	#	for k in range(0,header_list_length):
	#		print(data.iloc[j,k], end=' ')
	#	print("\n")
	#print("\nTotal number of cases that are Not classified: ", len(classified_not))
	
#Execution begins
rname = input('Enter Rule filename: ')

# Open the Rule file with read only permit
f = open(rname, "r")
# read all lines at once
lines = list(f)
# close the file after reading the lines.
f.close()

fname = input('Enter Data filename: ')
#data = pandas.read_table(fname, header=None, delimiter=r"\s+")
#Read the data into Pandas Dataframe as a table with delimeter as whitespace
data = pandas.read_table(fname, header=None, delim_whitespace=True)

no_of_conditions = 0 #to store the total number ofconditions in the rule file
rulecount = 0 #Count the number of rules
rule_left = [] #list to store the left parts of the Rules
rule_right = [] #list to store the right parts of the Rules
attribute = [] #list to store the attributes
value = [] #list to store the values
concept = [] #list to store the concepts
decision = [] #list to store the decision values
rule_left_conditions = [] #to store the conditions
rule_left_con = [] #to store conditions after stripping brackets
specificity = []
strength = []
matchcase = []

data.drop(data.index[0],inplace=True)
data.iloc[0] = data.iloc[0].replace('[','') #remove leading bracket from first row
data.iloc[0] = data.iloc[0].replace(']','') #remove trailing bracket from first row

rownum_old = data.shape[0] #to get the rowcount
colnum_old = data.shape[1] #to get the column count


for i in range(0,colnum_old-1):
	data.iloc[0,i] = data.iloc[0, i+1]


data.dropna(axis=1, how='any',inplace=True) #drop all the columns having any NaN values


rownum = data.shape[0] #No. of Rows in the dataframe
colnum = data.shape[1] #No. of Columns in the dataframe


global complete_classified_correct, complete_classified_incorrect, classified_not
complete_classified_correct = []
complete_classified_incorrect = []
classified_not = []
#Looping through the lines of the Rule file
for x in lines:
	if x.startswith('!') or x.startswith('\n'): #ignore the lines starting with !, \n and nos
		pass
	elif x.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
		
		numberstr = [a.strip() for a in x.split(',')]
		specificity.append(numberstr[0])
		strength.append(numberstr[1])
		matchcase.append(numberstr[2])
	elif(x.startswith('(')):
		rulecount+=1
		if("->" not in x):
			l = (lines.index(x))+1
			l2 = lines[l]
			l2 = l2.strip()
			x = x+l2
			
			rulesep = x.split("->") #rulesep array's first location contains the left side of the Rule and second location contains the right side
		


		elif("->" in x):

			rulesep = x.split("->") #rulesep array's first location contains the left side of the Rule and second location contains the right side
		

		rule_left.append(rulesep[0]) #updating the Left side of the rules
		rule_right.append(rulesep[1]) #updating the Right side of the rules

		rulesep2 = rule_left[0].split("&")
		length = len(rulesep2)
		no_of_conditions = no_of_conditions + length

		rule_right[0] = rule_right[0].strip()
		rule_right[0] = rule_right[0].lstrip("(")
		rule_right[0] = rule_right[0].rstrip(")")
		rule_right[0] = rule_right[0].rstrip("\n")

		sep2 = rule_right[0].split(",")

		concept.append(sep2[0])
		decision.append(sep2[1])
	
		for y in range(0,length):
			rule_left_conditions.append(rulesep2[y])
		
		#Stripping the conditions of the rules to remove whitespaces and brackets
		for z in rule_left_conditions:
			z = z.strip()
			z = z.lstrip("(")
			z = z.rstrip(")")
			rule_left_con.append(z)
		for u in rule_left_con:
			sep1 = u.split(",")
			attribute.append(sep1[0])
			value.append(sep1[1])
			
		
		#call the function for checking cases
		
		case_compare(data,attribute,value,concept,decision)
		
		rule_left = [] #list to store the left parts of the Rules
		rule_right = [] #list to store the right parts of the Rules
		attribute = [] #list to store the attributes
		value = [] #list to store the values
		concept = [] #list to store the concepts
		decision = [] #list to store the decision values
		rule_left_conditions = []
		rule_left_con = []

classified_not = [x for x in classified_not if x not in complete_classified_correct]
classified_not = [x for x in classified_not if x not in complete_classified_incorrect]

classified_not = list(set(classified_not))
complete_classified_correct_nodup = list(set(complete_classified_correct))
complete_classified_incorrect_nodup = list(set(complete_classified_incorrect))

response_match_factor = input('Do you want to use the Matching Factor (y/n): ')
response_strength_prob = input('Do you want to use Strength (s) or Conditional Probability (p): ')
response_specificity = input('Do you want to use the factor associated with Specificity (y/n): ')
response_support = input('Do you want to use the support of other rules or not (y/n): ')
response_concept_stat = input('Do you want to know the Concept Statistics (y/n): ')
response_classified = input('Do you want to know how Cases associated with Concepts are Classified (y/n): ')
#print(data.iloc[:,colnum-1])
#printing statements
print("\n\n-----------!!! General Statistics !!!-------------")
print("\n\n----This report was created from the Rule file", rname, "and from the Data file", fname, "----")
print("\n\nThe total number of cases: ", rownum-1)
print("\nThe total number of Attributes: ", colnum-1)
print("\nThe total number of Rules: ", rulecount)
print("\nThe total number of Conditions: ", no_of_conditions)
print("\nThe total number of cases that are NOT classified: ", len(classified_not))
print("\n\nCOMPLETE MATCHING: ")
print("\nThe total number of cases that are incorrectly classified: ", len(complete_classified_incorrect_nodup))
print("\nThe total number of cases that are correctly classified: ", len(complete_classified_correct_nodup))

decision_list = data.iloc[:,colnum-1].unique()
decision_list = decision_list[1:]


if(response_concept_stat is 'y' or response_concept_stat is 'Y'):
	print("\n\n-----------!!! Concept Statistics !!!-------------")
	for item in decision_list:
		incorr = 0
		corr = 0
		print("\n\nConcept(",data.iloc[0,colnum-1], item, ")" )
		print("\nThe total number of cases that are NOT classified: ", len(classified_not))
		print("\nCOMPLETE MATCHING: ")
		for j in complete_classified_incorrect_nodup:
			if data.iloc[j+1,colnum-1] is item:
				incorr = incorr + 1
		print("\nThe total number of cases that are incorrectly classified: ", incorr)
		for j in complete_classified_correct_nodup:
			if data.iloc[j+1,colnum-1] is item:
				corr = corr + 1
		print("\nThe total number of cases that are correctly classified: ", corr)


if(response_classified is 'y' or response_classified is 'Y'):
	print("\n\n-----------!!! Classification of Cases associated with Concepts !!!-------------")
	for item in decision_list:
		incorr = 0
		corr = 0
		print("\n\nConcept(",data.iloc[0,colnum-1], item, ")" )
		print("\nThe total number of cases that are NOT classified: ", len(classified_not))
		print("\nCOMPLETE MATCHING: ")
		print("\nList of cases that are Incorrectly classified: ")
		for j in complete_classified_incorrect_nodup:
			if data.iloc[j+1,colnum-1] is item:
				for j in complete_classified_correct_nodup:
					for k in range(0,colnum):
						print(data.iloc[j,k], end=' , ')
				print("\n")
		
		print("\nList of cases that are Correctly classified: ")
		for j in complete_classified_correct_nodup:
			if data.iloc[j+1,colnum-1] is item:
				for j in complete_classified_correct_nodup:
					for k in range(0,colnum):
						print(data.iloc[j,k], end=' , ')
				print("\n")
		
