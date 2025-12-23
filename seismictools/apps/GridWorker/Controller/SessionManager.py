import json
import os

class SessionManager:
    def __init__(self, session_file="session.json", message_callback=None):
        self.session_file = session_file
        self.message_callback = message_callback

    def show_message(self, message):
        """
            Функция выводит сообщения в строку состояния
            message (str): Текст сообщения для отображения
        """
        if self.message_callback:
            self.message_callback(message)

    def save_session(self, file_path=None, objects=None):
        """
            Функция сохраняет текущую сессию в JSON-файл
            file_path (str): Путь к загруженному файлу карты
            objects (list): Список объектов для сохранения
        """
        session_data = {
            'file_path': file_path,
            'objects': objects or []
        }
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            self.show_message(f"Ошибка сохранения сессии: {e}")

    def load_session(self):
        """
            Функция загружает сессию из JSON-файла
        """
        if not os.path.exists(self.session_file):
            return None

        try:
            with open(self.session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.show_message(f"Ошибка загрузки сессии: {e}")
            return None