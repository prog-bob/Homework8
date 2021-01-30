# Homework8
## Модуль обработки логов с использованием Python
В качестве источника логов выбран лог opencart (файл access.log для apache или nginx)

Описание реализации:

1. Возможность указать директорию где искать логи или конкретный файл с помощью опций
--file и --path. При указании --file=* анализируются все файлы логов из директории --path.
2. В случае если файл не может быть обработан, то скрипт завершится с ошибкой (1).
3.Собираться следующая статистическая информация:
- общее количество выполненных запросов
- количество запросов по типу: GET - 20, POST - 10 и т.п.
- топ 10 IP адресов, с которых были сделаны запросы
- топ 10 самых долгих запросов, должно быть видно метод, url, ip, время запроса
- топ 10 запросов, которые завершились клиентской ошибкой, должно быть видно метод, url, статус код, ip адрес
- топ 10 запросов, которые завершились ошибкой со стороны сервера, должно быть видно метод, url, статус код, ip адрес
4. Собранная статистика сохраняется в файл с расширением *json в каталог statistic/ с тем же именем, что и файл лога.
5. Скриншот с примером использования находится в папке screenshots
    - пример конфигурации
    - пример записи в логе, которую невозможно распарсить
