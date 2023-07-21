
from datetime import datetime, timedelta


from dateutil import parser
from django.shortcuts import render, redirect

from .mongodb.connect import db
from .tasks import work_process


# Create your views here.


def main(request):
    results = db.rysnya.find(sort=[("date", -1)])
    return render(request, 'infoboard/losses-list.html', {"results": transform_data_for_losses_list(results)})


def sync_losses_list(request):
    last_result = db.rysnya.find_one(sort=[("date", -1)])
    print(last_result)
    if last_result is not None:
        date = last_result["date"]
        last_date = parser.parse(date)
        now_date = datetime.now()
        period = now_date - last_date
        search_list = []
        for day in range(1, period.days + 1):
            next_date = last_date + timedelta(days=day)
            search_list.append(datetime.strftime(next_date, "%d.%m.%Y"))
        print(f'{search_list}')
        work_process.delay(search_list)
        print('------------------ sync_losses_list -------------')
    return redirect("losses")


def transform_data_for_losses_list(data):
    result = []
    for el in data:
        date = datetime.strftime(parser.parse(el['date']), '%d.%m.%Y')
        list_tuple = []
        for key, value in el.items():
            if key != '_id' and key != 'date':
                list_tuple.append((key, value))
        result.append((date, list_tuple))
    return result


