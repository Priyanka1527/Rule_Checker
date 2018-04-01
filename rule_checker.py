import pandas

fname = input('Enter Data filename: ')
#data = pandas.read_table(fname, header=None, delimiter=r"\s+")
data = pandas.read_table(fname, header=None, delim_whitespace=True)


data.drop(data.index[0],inplace=True)
data.iloc[0] = data.iloc[0].replace('[','') #remove leading bracket from first row
data.iloc[0] = data.iloc[0].replace(']','') #remove trailing bracket from first row

rownum_old = data.shape[0]
colnum_old = data.shape[1]

#print(rownum_old)
#print(colnum_old)

for i in range(0,colnum_old-1):
	data.iloc[0,i] = data.iloc[0, i+1]


data.dropna(axis=1, how='any',inplace=True)

print(data)
rownum = data.shape[0]
colnum = data.shape[1]
print("\n\nThe total number of cases: ", rownum-1)
print("\n\nThe total number of Attributes: ", colnum-1)

