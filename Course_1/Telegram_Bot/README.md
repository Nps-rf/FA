<img src="https://anexp.ru/Антиплагиат%20финансовый%20университет.png" align="right" width="256px"/>


# FA HOMEWORK BOT

* [**Используемые технологии**](#Используемые-технологии)
* [**Как пользоваться?**](#Как-пользоваться?)
* [**Как добавлять задания?**](#Как-добавлять-задания?)
* [**О проекте**](#О-проекте)
  * [**Deploy**](#Deploy)
  * [**Структура**](#Структура)
### Используемые технологии
* **Aiogram Framework** [<img align="left" width="22px" src="https://cdn4.iconfinder.com/data/icons/social-media-and-logos-11/32/Logo_telegram_Airplane_Air_plane_paper_airplane-22-256.png"/>][aiogram]
* **SQLite3** [<img align="left" width="22px" src="https://cdn1.iconfinder.com/data/icons/hawcons/32/700048-icon-89-document-file-sql-256.png"/>][SQLite]
* **Transliterate module** [<img align="left" width="22px" src="https://cdn2.iconfinder.com/data/icons/humano2/128x128/apps/character-set.png"/>][transliterate]

### Как пользоваться?

1) 📲 **Заходим к [боту](https://t.me/FA_Homework_bot)**
   1) 🔎 **Или же находим его самостоятельно:** `@FA_Homework_bot`
2) ▶ **Нажимаем на кнопку** `/start`
   1) ✏ **Или вводим её самостоятельно**
3) 🔠 **Вводим свою группу**
4) 🙃 **Если кто-то добавил задания, вы можете получить их нажав на кнопку `Получить задание!`**
   1) 😳 **Если его никто не добавлял, не расстраивайтесь, напишите [мне](https://t.me/Nps_rf) и я предоставлю вам возможность добавления домашнего задания для своей группы** 😉
5) 📅 **Выбираем дату**
6) 😊 **Получаем задание!**
### Как добавлять задания?
1) ✅ **Сперва получаем разрешение на добавление дз как в пункте 4.1**
2) ⭐ **Нажимаем на кнопку `Управление заданиями`**
3) 🤔 **Выбираем из контекстного меню необходимый предмет**
4) 📅 **Выбираем необходимую дату**
5) 📝 **Вводим задание** 
6) 🎉 **Радуемся!**
### О проекте
#### Deploy
* **Размещён на `Microsoft Azure | Windows (Windows 10 Pro)`**
#### Структура
* `bot.py`: **Основной файл который работает со всем хендлерами и обрабатывает основную логику бота**
* `Buttons.py`: **Файл со всеми клавиатурами и кнопками бота**
* `date.py`: **Файл для внутренней работы с датами**
* `db.py`: **Основной файл для работы с базами на данных на `SQLite`**
* `Schedule.py`: **Файл для получения расписания группы на основе API запросов к `ruz.fa.ru`**
* `create config.bat`: **Файл инициализации `config.py` с добавлением `TOKEN` и `green_list` из консоли**
* `Tests`: **Тесты на проверку инициализации баз данных**
### Иллюстрации

![Start](md%20images/start.png)

![Gettin_hw](md%20images/gettin_hw.png)

![HW](md%20images/HW.png)

![Managing](md%20images/manage.png)




[SQLite]: https://www.sqlite.org/docs.html
[aiogram]: https://github.com/aiogram/aiogram 
[transliterate]: https://pypi.org/project/transliterate/