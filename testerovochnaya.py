import datetime

def j():
    date = '2022-11-15'
    convert_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    print(convert_date.weekday())
    

if __name__ == "__main__":
    j()


