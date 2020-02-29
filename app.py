from mongoengine import *
import csv
import datetime

class TimeSeriesPoint(EmbeddedDocument):
    Time = DateTimeField()
    Value = IntField()


class ConfirmedCase(Document):
    Province = StringField()
    Country = StringField()
    Location = PointField(auto_index=True)
    Data = EmbeddedDocumentListField(TimeSeriesPoint)


connect('viral')

# case = ConfirmedCase(Province='asdf', Country='fdsa', Location=[1, 2]).save()
with open('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    rownum = 0
    cols = []
    for row in spamreader:
        if rownum == 0:
            cols = row
        else:
            datas = []
            datanum = 4
            for d in row[4:]:
                datas.append(TimeSeriesPoint(Value=int(d),Time=datetime.datetime.strptime(cols[datanum],'       ')))
                datanun+=1
            case = ConfirmedCase(
                Province = row[0],
                Country = row[1],
                Location = [
                    float(row[2]),
                    float(row[3])
                ],
                Data = []
            )
        rownum += 1
        # print ', '.join(row)
        # break
