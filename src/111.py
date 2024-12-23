
#cursor = cnxn.cursor()
with open('create_table.sql','r') as inserts:
    sql =  inserts.read()

print(sql)
