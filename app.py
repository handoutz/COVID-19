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


def extract_cols(row, idx_date_start):
    num = 0
    result = []
    for col in row:
        if num >= idx_date_start:
            dt = str(col).split('/')
            dt[0] = dt[0].rjust(2, '0')
            dt[1] = dt[1].rjust(2, '0')
            result.append('/'.join(dt))
        else:
            result.append(col)
        num += 1
    return result


if __name__ == '__main__':
    with open('csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv', 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        rownum = 0
        cols = []
        for row in spamreader:
            if rownum == 0:
                cols = extract_cols(row, 4)
            else:
                datas = []
                datanum = 4
                for d in row[4:]:
                    datas.append(
                        TimeSeriesPoint(Value=int(d), Time=datetime.datetime.strptime(cols[datanum], '%m/%d/%y')))
                    datanum += 1
                case = ConfirmedCase(
                    Province=row[0],
                    Country=row[1],
                    Location=[
                        float(row[3]),
                        float(row[2])
                    ],
                    Data=datas
                ).save()
            rownum += 1
            # print ', '.join(row)
            # break
