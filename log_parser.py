import argparse
import re
from json import dump
from collections import Counter
import os
from pprint import pprint

parser = argparse.ArgumentParser(description='Process access.log')
parser.add_argument('-f', '--file',
                    action='store',
                    default="access.log",
                    help='Log file name for parse one file, or "*" for parse all files')
parser.add_argument('-p', '--path',
                    action='store',
                    default="log/",
                    help='Path to logfiles')
args = parser.parse_args()


def files(path: str):
    """
    Генератор списка файлов в директории path
    :param path: относительный путь к каталогу с файлами логов
    :return: имя файла с путем
    """
    for file in os.listdir(path):
        file = os.path.join(path, file)
        if os.path.isfile(file):
            yield file


# Поиск токенов в строке лога nginx
def get_tokens_in(line):
    """
    :param line: строка в формате 109.169.248.247 - - [12/Dec/2015:18:25:11 +0100] "GET /administrator/ HTTP/1.1" 200 4263 "-"
    :return: кортеж токенов  (ip, time, method, url, code, duration) или None
    """
    match = re.search(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"
                      r".*:(\d{2}:\d{2}:\d{2})"
                      r".*(POST|GET|Get|get|PUT|DELETE|HEAD|Head|OPTIONS|T|PROPFIND|FOO|INDEX|SEARCH)"
                      r"\s+(.*)\s+HTTP/"
                      r".*\"\s+(\d{3})"
                      r"\s+(\d*)\s*", line)
    if match:
        return match.groups()


if __name__ == '__main__':

    # выбрать все файлы логов или конкретный файл
    if args.file == '*':
        log_files = files(args.path)
    else:
        log_files = [os.path.join(args.path, args.file)]

    print(f"log_files = {log_files}")
    file = None

    try:
        for file in log_files:
            # общее количество выполненных запросов
            total_req = 0
            # счетчик ip
            ip_cnt = Counter()
            # счетчик количества запросов по типу
            method_cnt = Counter()
            # список для поиска самых долгих запросов
            duration_list = []
            # список запросов, которые завершились клиентской ошибкой
            client_err_list = []
            # список запросов, которые завершились ошибкой со стороны сервера
            server_err_list = []

            with open(file) as f:
                lines = (line for line in f.readlines())
                for i, line in enumerate(lines):
                    tokens = get_tokens_in(line)
                    if tokens is None:
                        print(f"error parse for <{i}> line in file <{file}>:\n{line}")
                        continue
                    ip, time, method, url, code, duration = tokens
                    total_req += 1
                    method_cnt[method] += 1
                    ip_cnt[ip] += 1
                    duration_list.append({"duration": duration, "method": method, "url": url, "ip": ip, "time": time})
                    if int(code) >= 500:
                        server_err_list.append({"method": method, "url": url, "code": code, "ip": ip})
                    elif int(code) >= 400:
                        client_err_list.append({"method": method, "url": url, "code": code, "ip": ip})

            file_statictic = {
                "total_requests": total_req,
                "method_cnt": method_cnt,
                "top10_requests_ip": ip_cnt.most_common(10),
                "top10_longest_requests": sorted(duration_list, key=lambda req: req["duration"], reverse=True)[:10],
                "top10_client_err": sorted(client_err_list, key=lambda req: req["ip"])[:10],
                "top10_server_err": sorted(server_err_list, key=lambda req: req["ip"])[:10],
            }
            # сохранение статистики в файл
            pprint(file_statictic)
            with open("statistic/" + os.path.split(file)[1] + ".json", "w") as f:
                dump(file_statictic, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"При обработке файла {file} возникло исключение {e}")
        exit(1)
