<h1 align="center">Directory API</a> 

<h2 align="left">Для запуска проекта через Docker необходимо:</h2>

• Создать и заполнить файл ```.env``` по шаблону файла ```.env.sample```

• Создать и заполнить файл ```.env.docker``` по шаблону файла ```.env.docker.sample```

• Запустить Docker командой:
```shell
docker compose up --build
```

    Для тестирования сервиса рекомендуется использовать ```Postman```, 
    файл с коллекцией находится в корне проекта

________________________________________
## Эндпоинты (Endpoints)

### Добавление в БД из exclel файла

URL: /directory/upload_materials/

Метод: ```POST```

Пример запроса:

            file: <file.xlsx>

Пример структуры файла excel:

| Материал         | Категория    | Код материала   | Стоимость материала  | 
|:----------------:|:------------:|:---------------:|:--------------------:|
| Наименование 1   | Категория 1  | Код 1           | Стоимость 1          | 
| Наименование 2   | Категория 2  | Код 2           | Стоимость 2          |
| Наименование 3   | Категория 3  | Код 3           | Стоимость 3          |
| Наименование 4   | Категория 4  | Код 4           | Стоимость 4          |

 
Ответ:
- Добавляет в БД данные из excel таблицы
________________________________________
### Просмотр списка/создания/обновления/удаления материалов

URL: /directory/materials/

Метод: ```GET```, ```POST```, ```PUT```, ```DELETE```
________________________________________
### Просмотр списка/создания/обновления/удаления категорий

URL: /directory/categories/

Метод: ```GET```, ```POST```, ```PUT```, ```DELETE```
________________________________________
### Вывод стоимости вложенных материалов

URL: /directory/categories_with_cost/

Метод: ```GET```
________________________________________

- К проекту подключен Swagger, дополнительную информацию можно найти по URL: ```/docs/```

### Удачи!
  
