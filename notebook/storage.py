import json
import os
from typing import List
from .models import Note

class NoteStorage:
    # Класс для работы с файлом заметок
    # Здесь вся логика чтения и записи в JSON файл
    def __init__(self, filename: str = "notes.json"):
        # Конструктор - настраиваю файл для хранения заметок
        # Имя файла где будут храниться заметки
        self.filename = filename
        
        # Убеждаюсь что файл существует
        self._ensure_storage_file()
    
    def _ensure_storage_file(self):
        # Внутренний метод - создаю файл если его нет
        if not os.path.exists(self.filename):
            # Создаю пустой файл с пустым списком заметок
            with open(self.filename, 'w') as f:
                json.dump([], f)
            print(f"📁 Создан новый файл для заметок: {self.filename}")
    
    def _read_notes(self) -> List[dict]:
        # Внутренний метод - читаю все заметки из файла
        # Возвращаю список словарей (сырые данные)
        try:
            # Пытаюсь открыть файл и прочитать JSON
            with open(self.filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Если файл пустой или повреждён - возвращаю пустой список
            return []
    
    def _write_notes(self, notes_data: List[dict]):
        # Внутренний метод - записываю заметки в файл
        # Получаю список словарей и сохраняю в JSON
        with open(self.filename, 'w') as f:
            # Использую indent=2 для красивого форматирования
            json.dump(notes_data, f, indent=2)
    
    def get_all_notes(self) -> List[Note]:
        # Получаю все заметки как объекты Note
        # Читаю из файла и преобразую словари в объекты
        # Читаю сырые данные из файла
        notes_data = self._read_notes()
        
        # Преобразую каждый словарь в объект Note
        return [Note.from_dict(note_data) for note_data in notes_data]
    
    def save_note(self, note: Note) -> Note:
        # Сохраняю одну заметку в файл
        # Если у заметки нет ID - значит она новая
        # Читаю текущие заметки из файла
        notes_data = self._read_notes()
        
        # Проверяю новая это заметка или существующая
        if note.id is None:
            # Это новая заметка - нужно назначить ID
            if notes_data:
                # Нахожу максимальный ID и увеличиваю на 1
                note.id = max([n['id'] for n in notes_data]) + 1
            else:
                # Если это первая заметка - ID = 1
                note.id = 1
            
            # Добавляю новую заметку в список
            notes_data.append(note.to_dict())
        
        # Сохраняю обновлённый список обратно в файл
        self._write_notes(notes_data)
        
        return note
    
    def delete_note(self, note_id: int) -> bool:
        # Удаляю заметку по ID
        # Возвращаю True если удалил, False если не нашёл
        # Читаю текущие заметки
        notes_data = self._read_notes()
        
        # Запоминаю сколько было заметок до удаления
        initial_length = len(notes_data)
        
        # Создаю новый список без заметки с указанным ID
        notes_data = [note for note in notes_data if note['id'] != note_id]
        
        # Проверяю изменился ли список
        if len(notes_data) < initial_length:
            # Если да - сохраняю изменения
            self._write_notes(notes_data)
            return True
        
        # Если не изменился - значит заметка не найдена
        return False
    
    def search_notes(self, query: str) -> List[Note]:
        # Ищу заметки по тексту в заголовке и содержании
        # Получаю все заметки
        notes = self.get_all_notes()
        
        # Привожу запрос к нижнему регистру для поиска без учёта регистра
        query = query.lower()
        
        # Ищу заметки где запрос есть в заголовке или тексте
        return [
            note for note in notes 
            if query in note.title.lower() or query in note.content.lower()
        ]
