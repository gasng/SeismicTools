# Eiconal Solver

# Использование:

1. Скачать и установить Python версии 3.12 или выше

2. Установить окружение poetry, для этого в cmd прописать путь до Python 3.12 и запустить команды:
```
%LocalAppData%\Programs\Python\Python39\python.exe -m pip install poetry

%LocalAppData%\Programs\Python\Python39\python.exe -m poetry install
```

Пункты 1-2 выполняются один раз при запуске программы на новом устройстве.

# При последующем использовании выполняются только шаги 3-4:

3. В cmd перейти в директорию проекта, для этого прописать команду cd и путь до проекта
```
D:              # Переходим на диск, где лежит проект (в данном случае диск D)                 

cd D:\...\NeuralNetworkMicroSeis-main               # Переходим в папку проекта (вместо ... ваш путь)   
```
4. Для запуска программы в cmd прописать путь до вашей версии Python и запустить команду:
```
%LocalAppData%\Programs\Python\Python312\python.exe -m poetry run eiconal_solver