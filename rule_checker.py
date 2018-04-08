import pandas
import itertools

#user defined function definitions
def case_compare(datafile,attribute,value,concept,decision):
	print(data.iloc[:,0])

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
rule_left_conditions = []
rule_left_con = []

data.drop(data.index[0],inplace=True)
data.iloc[0] = data.iloc[0].replace('[','') #remove leading bracket from first row
data.iloc[0] = data.iloc[0].replace(']','') #remove trailing bracket from first row

rownum_old = data.shape[0] #to get the rowcount
colnum_old = data.shape[1] #to get the column count

#print(rownum_old)
#print(colnum_old)

for i in range(0,colnum_old-1):
	data.iloc[0,i] = data.iloc[0, i+1]


data.dropna(axis=1, how='any',inplace=True) #drop all the columns having any NaN values

#print(data)
rownum = data.shape[0] #No. of Rows in the dataframe
colnum = data.shape[1] #No. of Columns in the dataframe

#Looping through the lines of the Rule file
for x in lines:
	if x.startswith('!') or x.startswith('\n') or x.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')): #ignore the lines starting with !, \n and nos
		pass
	else:
		rulecount+=1
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
		#print(attribute)
		#print(value)
		#print("..........")
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

					
#printing statements
print("\n\n----This report was created from the Rule file", rname, "and from the Data file", fname, "----")
print("\n\nThe total number of cases: ", rownum-1)
print("\nThe total number of Attributes: ", colnum-1)
print("\nThe total number of Rules: ", rulecount)
print("\nThe total number of Conditions: ", no_of_conditions)

