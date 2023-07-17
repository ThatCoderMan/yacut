# YaCut
![workflows](https://github.com/ThatCoderMan/yacut/actions/workflows/workflow.yml/badge.svg)

<details>
<summary>Project stack</summary>

- Python 3.10
- Flask
- Flask-WTF
- SQLAlchemy
- Alembic
- GitHub Actions

</details>

Сервис для сокращения ссылок и последующей переадресации на сайт при использовании сокращённой

## Запуск проекта
### Установка
Клонируйте репозиторий:
```commandline
git clone git@github.com:ThatCoderMan/yacut.git
```
Перейдите в папку `yacut`
```commandline
cd yacut
```
Активируйте виртуальное окружение:
- Для Linux/macOS:
    ```commandline
    source venv/bin/activate
    ```
- Для Windows:
    ```commandline
    source venv/scripts/activate
    ```
Установити зависимости из файла `requirements.txt`:
```commandline
pip install -r requirements.txt
```
Запустите программу:
```commandline
flask run
```
## Автор проекта
- [Artemii Berezin](https://github.com/ThatCoderMan)
