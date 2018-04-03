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
rule_left = [] #list to store the left parts of the Rules
rule_right = [] #list to store the right parts of the Rules
rule_left_conditions = [] #list to store the conditions of the rules
rule_left_con = [] #final list to store the attribute-value pairs
rule_right_con = [] #final list to store the concept-value
attribute = [] #list to store the attributes
value = [] #list to store the values

#Looping through the lines of the Rule file
for x in lines:
	if x.startswith('!') or x.startswith('\n') or x.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')): #ignore the lines starting with !, \n and nos
		pass
	else:
		rulecount+=1
		rulesep = x.split("->") #rulesep array's first location contains the left side of the Rule and second location contains the right side
		rule_left.append(rulesep[0]) #updating the Left side of the rules
		rule_right.append(rulesep[1]) #updating the Right side of the rules


#Splitting the left side of the rule by '&'
for x in rule_left:
	rulesep2 = x.split("&")
	length = len(rulesep2)
	for y in range(0,length):
		rule_left_conditions.append(rulesep2[y])

#Stripping the conditions of the rules to remove whitespaces and brackets
for x in rule_left_conditions:
	x = x.strip()
	x = x.lstrip("(")
	x = x.rstrip(")")
	rule_left_con.append(x)

#Stripping the concept of the rules to remove whitespaces, brackets and new line
for x in rule_right:
	x = x.strip()
	x = x.lstrip("(")
	x = x.rstrip(")")
	x = x.rstrip("\n")
	rule_right_con.append(x)


for x in rule_left_con:
	sep1 = x.split(",")
	attribute.append(sep1[0])
	value.append(sep1[1])

for x in rule_right_con:
	sep1 = x.split(",")
	attribute.append(sep1[0])
	value.append(sep1[1])

print("\n", attribute)
print("\n", value)

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

#print(data)
rownum = data.shape[0] #No. of Rows in the dataframe
colnum = data.shape[1] #No. of Columns in the dataframe
print("\n\n----This report was created from the Rule file", rname, "and from the Data file", fname, "----")
print("\n\nThe total number of cases: ", rownum-1)
print("\nThe total number of Attributes: ", colnum-1)
print("\nThe total number of Rules: ", rulecount)
print("\nThe total number of Conditions: ", len(rule_left_conditions))
