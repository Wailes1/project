import argparse
from .models import Note
from .storage import NoteStorage

class NoteCommands:
    # Класс для обработки команд пользователя
    # Здесь я реализую всю логику работы с заметками
    
    def __init__(self, storage: NoteStorage):
        # Сохраняю объект для работы с файлами
        self.storage = storage
    
    def add_note(self, title: str, content: str):
        """
        Метод для добавления новой заметки
        Получаю заголовок и текст, создаю заметку и сохраняю в файл
        """
        # Проверяю что пользователь ввёл и заголовок и текст
        if not title or not content:
            raise ValueError("Заголовок и содержание обязательны!")
        
        # Создаю новый объект заметки
        note = Note(title=title, content=content)
        
        # Сохраняю заметку в файл и получаю сохранённую версию с ID
        saved_note = self.storage.save_note(note)
        
        # Сообщаю пользователю об успехе
        print(f"✅ Заметка добавлена успешно! (ID: {saved_note.id})")
    
    def list_notes(self):
        # Метод для показа всех заметок
        # Получаю все заметки из файла и красиво их вывожу
        # Получаю список всех заметок
        notes = self.storage.get_all_notes()
        
        # Проверяю есть ли вообще заметки
        if not notes:
            print("📝 Заметок пока нет. Создайте первую!")
            return
        
        # Показываю сколько всего заметок
        print(f"📋 Я нашёл {len(notes)} заметок:")
        
        # Перебираю все заметки и вывожу информацию о каждой
        for note in notes:
            print(f"ID: {note.id}")
            print(f"Заголовок: {note.title}")
            print(f"Содержание: {note.content}")
            print(f"Создана: {note.created_at[:16]}")  # Обрезаю дату для красоты
            print("-" * 30)
    
    def search_notes(self, query: str):
        # Метод для поиска заметок по тексту
        # Ищу в заголовках и содержании заметок
        # Проверяю что пользователь ввёл поисковый запрос
        if not query:
            print("🔍 Введите текст для поиска!")
            return
        
        # Ищу заметки по запросу
        notes = self.storage.search_notes(query)
        
        # Проверяю нашёл ли что-нибудь
        if not notes:
            print(f"😞 По запросу '{query}' я ничего не нашёл (")
            return
        
        # Показываю результаты поиска
        print(f"🎯 Я нашёл {len(notes)} заметок по запросу '{query}':")
        for note in notes:
            print(f"ID: {note.id} - {note.title}")
            print(f"   {note.content[:60]}...")  # Показываю только начало текста
    
    def delete_note(self, note_id: int):
        # Метод для удаления заметки по ID
        # Получаю ID заметки и удаляю её из файла
        # Пытаюсь удалить заметку
        if self.storage.delete_note(note_id):
            print(f"🗑️ Заметка ID {note_id} удалена")
        else:
            print(f"⚠️ Заметка с ID {note_id} не найдена")

def setup_parser():
    # Функция для настройки парсера аргументов командной строки
    # Здесь я определяю какие команды понимает моя программа
    # Создаю парсер с описанием программы
    parser = argparse.ArgumentParser(description='📝 Мой менеджер заметок')
    
    # Добавляю команду для добавления заметки
    parser.add_argument('--add', action='store_true', 
                       help='Добавить новую заметку')
    
    # Добавляю команду для показа всех заметок
    parser.add_argument('--list', action='store_true', 
                       help='Показать все заметки')
    
    # Добавляю команду для поиска заметок
    parser.add_argument('--search', type=str, 
                       help='Найти заметки по тексту')
    
    # Добавляю команду для удаления заметки
    parser.add_argument('--delete', type=int, 
                       help='Удалить заметку по ID')
    
    # Добавляю параметры для создания заметки
    parser.add_argument('--title', type=str, 
                       help='Заголовок заметки')
    parser.add_argument('--content', type=str, 
                       help='Текст заметки')
    
    return parser
