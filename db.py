import pymysql
import pandas as pd

#setup connection to database
def getcon(db_name):
    conn=pymysql.connect(host="localhost",port=3306,user='root',passwd='123456',db=db_name,charset='utf8')
    cursor1=conn.cursor()
    return conn,cursor1

# read file and update database
def insertData(db_name,table_name):

    conn,cursor1=getcon(db_name)

    df=pd.read_csv('bronebat.csv')
    df2 = df.astype(object).where(pd.notnull(df), "None")

    counts = 0
    for each in df2.values:

        sql = 'insert into '+table_name+ '(link, family, genus, specificEpithet, country, stateProvince, verbatimLocality, decimalLatitude, decimalLongitude, eventDate, eventTime, recordedBy, scientificName) values('
        #(link, family, genus, specificEpithet, country, stateProvince, verbatimLocality, decimalLatitude, decimalLongitude, eventDate, eventTime, recordedBy)

        for i,n in enumerate(each):

            if i < (len(each) - 1):
                #因为其中几条数据为数值型，所以不用添加双引号
                    sql = sql + '"' + str(n) + '"' + ','
            else:
                sql = sql + '"' + str(n) + '"'
        sql = sql + ');'
        print(sql)

        cursor1.execute(sql)

        conn.commit()

        counts+=1

        print('Successfully add '+str(counts)+'sets of data ')
    return conn,cursor1

def main(db_name,table_name):
    conn, cursor1 =insertData('test','bat')
    cursor1.close()
    conn.close()
if __name__=='__main__':
    main('test','bat')