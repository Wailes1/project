from datetime import datetime
from .models import Note
from .storage import NoteStorage

class NoteCommands:
    # Класс для обработки команд пользователя
    # Здесь я реализую всю логику работы с заметками
    
    def __init__(self, storage: NoteStorage):
        # Сохраняю объект для работы с файлами
        self.storage = storage
    
    def add_note(self, title: str, content: str):
        # Метод для добавления новой заметки
        # Получаю заголовок и текст, создаю заметку и сохраняю в файл
        
        # Проверяю что пользователь ввёл и заголовок и текст
        if not title or not content:
            raise ValueError("Заголовок и содержание обязательны!")
        
        # Создаю новый объект заметки
        note = Note(title=title, content=content)
        
        # Сохраняю заметку в файл и получаю сохранённую версию с ID
        saved_note = self.storage.save_note(note)
        
        # Сообщаю пользователю об успехе
        print(f"✅ Заметка добавлена успешно! (ID: {saved_note.id})")
    
    def list_notes(self, date_filter: str = None):
        # Метод для показа всех заметок
        # Получаю все заметки из файла и красиво их вывожу
        
        # Получаю список всех заметок
        notes = self.storage.get_all_notes()
        
        # Применяю фильтр по дате если указан
        if date_filter:
            notes = self.storage.filter_notes_by_date(notes, date_filter)
        
        # Проверяю есть ли вообще заметки
        if not notes:
            if date_filter:
                print(f"📝 Заметок за {date_filter} не найдено.")
            else:
                print("📝 Заметок пока нет. Создайте первую!")
            return
        
        # Показываю сколько всего заметок
        if date_filter:
            print(f"📋 Я нашёл {len(notes)} заметок за {date_filter}:")
        else:
            print(f"📋 Я нашёл {len(notes)} заметок:")
        
        # Перебираю все заметки и вывожу информацию о каждой
        for note in notes:
            print(f"ID: {note.id}")
            print(f"Заголовок: {note.title}")
            print(f"Содержание: {note.content}")
            print(f"Создана: {note.created_at[:16]}") 
            print("-" * 30)
    
    def search_notes(self, query: str, date_filter: str = None):
        # Метод для поиска заметок по тексту
        # Ищу в заголовках и содержании заметок
        
        # Проверяю что пользователь ввёл поисковый запрос
        if not query:
            print("Введите текст для поиска!")
            return
        
        # Ищу заметки по запросу
        notes = self.storage.search_notes(query)
        
        # Применяю фильтр по дате если указан
        if date_filter:
            notes = self.storage.filter_notes_by_date(notes, date_filter)
        
        # Проверяю нашёл ли что-нибудь
        if not notes:
            if date_filter:
                print(f"По запросу '{query}' за {date_filter} я ничего не нашёл (")
            else:
                print(f"По запросу '{query}' я ничего не нашёл (")
            return
        
        # Показываю результаты поиска
        if date_filter:
            print(f"Я нашёл {len(notes)} заметок по запросу '{query}' за {date_filter}:")
        else:
            print(f"Я нашёл {len(notes)} заметок по запросу '{query}':")
            
        for note in notes:
            print(f"ID: {note.id} - {note.title}")
            print(f"   {note.content[:60]}...")  # Показываю только начало текста
    
    def delete_note(self, note_id: int):
        # Метод для удаления заметки по ID
        # Получаю ID заметки и удаляю её из файла
        
        # Пытаюсь удалить заметку
        if self.storage.delete_note(note_id):
            print(f"Заметка ID {note_id} удалена")
        else:
            print(f"Заметка с ID {note_id} не найдена")
