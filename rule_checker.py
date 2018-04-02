import pandas

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


rulecount = 0 #Count the number of rules
rule_left = [] #list to keep the left parts of the Rules
rule_right = [] #list to keep the right parts of the Rules

#Looping through the lines of the Rule file
for x in lines:
	if x.startswith('!') or x.startswith('\n') or x.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')): #ignore the lines starting with !, \n and nos
		pass
	else:
		rulecount+=1
		rulesep = x.split("->") #rulesep array's first location contains the left side of the Rule and second location contains the right side
		rule_left.append(rulesep[0]) #updating the Left side of the rules
		rule_right.append(rulesep[1]) #updating the Right side of the rules

print("\n\n", rule_left)
print("\n\n", rule_right)

print("\n\nNumber of Rules: ", rulecount)

data.drop(data.index[0],inplace=True)
data.iloc[0] = data.iloc[0].replace('[','') #remove leading bracket from first row
data.iloc[0] = data.iloc[0].replace(']','') #remove trailing bracket from first row

rownum_old = data.shape[0]
colnum_old = data.shape[1]

#print(rownum_old)
#print(colnum_old)

for i in range(0,colnum_old-1):
	data.iloc[0,i] = data.iloc[0, i+1]


data.dropna(axis=1, how='any',inplace=True) #drop all the columns having any NaN values

print(data)
rownum = data.shape[0] #No. of Rows in the dataframe
colnum = data.shape[1] #No. of Columns in the dataframe
print("\n\nThe total number of cases: ", rownum-1)
print("\n\nThe total number of Attributes: ", colnum-1)
