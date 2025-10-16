import json
from datetime import datetime

class Note:
    # Класс для представления одной заметки
    # Здесь я определяю из каких данных состоит каждая заметка    
    def __init__(self, title: str, content: str):
        # Конструктор класса - создаю новую заметку
        # Вызывается когда пишу Note ("Заголовок", "Текст")
        # ID пока неизвестен, будет назначен при сохранении
        self.id = None
        
        # Заголовок заметки - то что видно в списке
        self.title = title
        
        # Основной текст заметки
        self.content = content
        
        # Дата создания - ставлю текущее время
        self.created_at = datetime.now().isoformat()
    
    def to_dict(self):
        # Преобразую объект заметки в словарь
        # Это нужно чтобы сохранить заметку в JSON файл
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        # Создаю объект заметки из словаря
        # Это нужно когда загружаю заметки из JSON файла
        # Использую classmethod чтобы можно было вызывать Note.from_dict()
        # Создаю новую заметку с данными из словаря
        note = cls(data['title'], data['content'])
        
        # Восстанавливаю ID и дату создания
        note.id = data['id']
        note.created_at = data['created_at']
        
        return note # возвращаю готовый объект Note
