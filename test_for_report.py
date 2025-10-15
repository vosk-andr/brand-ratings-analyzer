import csv
import os
import sys

from report import create_report, brand_ratings, save_report

# Проверка основного скрипта (create_report) на работу: с большим количеством файлов; с данными которые повторяются; не округленными данными
def create_report_file_normal():
  with open ('./files/test_products1.csv', mode='w', newline='', encoding='utf-8') as brn:
    writer = csv.writer(brn)
    writer.writerow(['brand', 'rating'])
    writer.writerow(['apple', '4.40'])
    writer.writerow(['samsung', '4.70'])
    writer.writerow(['xiaomi', '4.50'])
    writer.writerow(['samsung', '4.50'])
  with open ('./files/test_products2.csv', mode='w', newline='', encoding='utf-8') as brn:
    writer = csv.writer(brn)
    writer.writerow(['brand', 'rating'])
    writer.writerow(['apple', '4.531'])
    writer.writerow(['samsung', '4.824'])
    writer.writerow(['xiaomi', '4.614'])
    writer.writerow(['samsung', '4.644'])
  with open ('./files/test_products3.csv', mode='w', newline='', encoding='utf-8') as brn:
    writer = csv.writer(brn)
    writer.writerow(['brand', 'rating'])
    writer.writerow(['apple', '4.598'])
    writer.writerow(['samsung', '4.8999'])
    writer.writerow(['xiaomi', '4.685'])
    writer.writerow(['samsung', '4.699'])
  try:
    sys.argv = ['report.py', '--files', 'test_products1.csv', 'test_products2.csv', 'test_products3.csv', '--report', 'test_report']
    create_report()
    with open('./reports/test_report.csv', encoding='utf-8') as t_r:
      test_reader = csv.DictReader(t_r)
      data = {row['brand']: float(row['rating']) for row in test_reader}
    assert abs(data['apple'] - 4.51) < 0.01
    assert abs(data['samsung'] - 4.71) < 0.01
    assert abs(data['xiaomi'] - 4.60) < 0.01
    print ('Проверка test_save_report пройдена')
  except Exception as e:
    print (f'Полученные значения в test_save_report не совпадают с заданными, система выдает ощибку: {e}')
  for file in ['test_products1.csv', 'test_products2.csv', 'test_products3.csv']:
    os.remove(f'./files/{file}')
  os.remove(f'./reports/test_report.csv')

# Проверка функции brand_ratings на получение неправильной таблицы
def brand_ratings_file_with_broken_table():
  with open ('./files/test_products.csv', mode='w', newline='', encoding='utf-8') as brn:
    writer = csv.writer(brn)
    writer.writerow(['brand1', 'rating1'])
    writer.writerow(['apple', '4.5'])
    writer.writerow(['samsung', '4.8'])
    writer.writerow(['xiaomi', '4.6'])
    writer.writerow(['samsung', '4.6'])
  try:
    brand_ratings(['test_products.csv'])
    assert False, 'Должна быть ошибка в части brand_ratings_broken_table'
  except KeyError:
    print ('Проверка brand_ratings_file_with_broken_table пройдена')
  os.remove('./files/test_products.csv')

# Проверка функции brand_ratings на получение пустого файла
def brand_ratings_empty_file():
  with open ('./files/test_products.csv', mode='w', newline='', encoding='utf-8') as brn:
    writer = csv.writer(brn)
    writer.writerow("")
  try:
    brand_ratings(['test_products.csv'])
    assert False, 'Должна быть ошибка в части brand_ratings_empty_file'
  except ValueError:
    print ('Проверка brand_ratings_empty_file пройдена')
  os.remove('./files/test_products.csv')

# Проверка функции brand_ratings на получение несуществующей таблицы
def brand_ratings_with_file_not_exist():
  try:
    brand_ratings(['test_products.csv'])
    assert False, 'Должна быть ошибка в части brand_ratings_with_file_not_exist'
  except FileNotFoundError:
    print ('Проверка brand_ratings_with_file_not_exist пройдена')

# Проверка работоспособности функции save_report
def test_save_report():
  test_data =[('apple', 4.41), ('samsung', 4.74), ('xiaomi', 4.54)]
  save_report(test_data, 'test_report')
  assert os.path.exists('./reports/test_report.csv')
  with open('./reports/test_report.csv', encoding='utf-8') as t_r:
    test_reader = list(csv.reader(t_r))
  try:
    assert test_reader[1][1] == '4.41'
    assert test_reader[2][1] == '4.74'
    assert test_reader[3][1] == '4.54'
    print ('Проверка test_save_report пройдена')
  except Exception as e:
    print (f'Полученные значения в test_save_report не совпадают с заданными, система выдает ощибку: {e}')
  os.remove(f'./reports/test_report.csv')

# Запуск проверок
def start_tests():
  tests = [create_report_file_normal, brand_ratings_file_with_broken_table, brand_ratings_empty_file, test_save_report]
  good = 0
  errors = 0
  for test in tests:
    try:
      test()
      good += 1
    except:
      errors += 1
  print (f'Пройдено тестов = {good}, ошибок = {errors}')

if __name__ == "__main__":
  start_tests()