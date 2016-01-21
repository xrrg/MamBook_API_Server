from django.shortcuts import render
import xlrd
from MamBook.models import *
# Create your views here.


def parse():
    rd = xlrd.open_workbook('/home/gambrinius/PycharmProjects/MamBook_API_Server/Развивайка0-3.xls',
                            formatting_info=True)  # change file name to current parse

    sheet = rd.sheet_by_index(0)

    values = [sheet.row_values(row_num) for row_num in range(sheet.nrows)]
    category_list = []

    for value in values:  # change values of file parse
        year = value[0]
        month = value[1]
        day = value[2]
        title = value[3]
        text = value[4]
        category = value[5]
        category_list.append(category)

        try:    # select needs parsing Object
            Progress(title=title, content=text, year=int(year), day=int(day), month=int(month),
                     category=Category.objects.get(name=category),
                     do_advice='Well done!', not_do_advice='You failed.').save()
        except Exception:
            pass

        try:
            pass  # Achievement(title=title, content=text, year=year, month=month, number=number).save()
        except Exception:
            pass

        try:
            pass  # SelfDevelopment(title=title, content=text, day=day).save()
        except Exception:
            pass

    category_set = set(category_list)
    category_set.remove('')

    for category in category_set:
        Category(name=category).save()

    return 0


def initialize(request):
    context = dict()

    return render(request, 'main.html', context)
