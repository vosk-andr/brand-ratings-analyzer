import argparse
import csv
from tabulate import tabulate

# Функция читает данные в файлах, записывает brand и rating в словарь report_dict и выводит словарь с brand и средними значениями rating для своих брендов
def brand_ratings(files):
  report_dict = {}
  for file in files:
    try:
      with open (f'./files/{file}', encoding='utf-8') as r_file:
        file_reader = csv.DictReader(r_file, delimiter=',')
        for row in file_reader:
          report_dict.setdefault(row['brand'], []).append(float(row['rating']))
    except FileNotFoundError:
      raise FileNotFoundError(f"Файл {file} не найден")
    except KeyError: 
      raise KeyError(f"Неверный формат таблицы в файле {file}")
  if not report_dict:
    raise ValueError("Нет данных для построения отчета")
  return {brand: round(sum(ratings)/len(ratings), 2) for brand, ratings in report_dict.items()}

# Функция сохранения отчета
def save_report(report, filename):
  with open (f'./reports/{filename}.csv', mode = 'w', newline = '', encoding='utf-8') as w_report:
    writer = csv.writer(w_report)
    writer.writerow(['brand', 'rating'])
    writer.writerows(report)

# Функция принимает аргументы files и report, передает их в другие функции и выводит таблицу в консоль
def create_report():
  try:
    parser = argparse.ArgumentParser(description='Выводит файлы и отчет')
    parser.add_argument("--files", nargs='*', help='Файлы по которым будет строится отчет')
    parser.add_argument("--report", help='Название отчета')
    arg = parser.parse_args()
    if not arg.files:
      print ("Укажите файлы для построения отчета")
      exit(1)
    report = sorted(brand_ratings(arg.files).items(), key=lambda x: x[1], reverse=True)
    table = tabulate(report, headers=(['brand', 'rating']), tablefmt = 'grid', floatfmt = '.2f', showindex=True)
    print(table)
    if not arg.report:
      print ("Отчет сформирован без сохранения в папку reports")
    else:
      save_report(report, arg.report)
  except FileNotFoundError as e:
    print(e)
  except KeyError as e:
    print(e)
  except ValueError as e:
    print(e)
  except Exception as e:
    print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
  create_report()