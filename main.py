# Это главный файл программы - Менеджер заметок
# Здесь происходит запуск и обработка команд пользователя

import sys
import os
import argparse  # Импортирую argparse для работы с аргументами командной строки

# Добавляю текущую папку в путь поиска модулей, чтобы Python нашёл мои файлы
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импортирую свои классы из пакета notebook
from notebook.commands import NoteCommands
from notebook.storage import NoteStorage

def setup_parser():
    # Функция для настройки парсера аргументов командной строки
    # Здесь я определяю какие команды понимает моя программа
    parser = argparse.ArgumentParser(
        description='📝 Мой менеджер заметок - программа для ведения записей'
    )
    
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
    
    # Добавляю параметр для фильтрации по дате
    parser.add_argument('--date', type=str, 
                       help='Фильтр по дате (today, week, month, ГГГГ-ММ-ДД, ГГГГ-ММ, ГГГГ)')
    
    # Добавляю параметры для создания заметки
    parser.add_argument('--title', type=str, 
                       help='Заголовок заметки')
    
    parser.add_argument('--content', type=str, 
                       help='Текст заметки')
    
    return parser

def main():
    # Главная функция программы
    # Здесь я обрабатываю команды которые ввёл пользователь
    # Использую argparse для разбора аргументов командной строки
    
    # Создаю парсер аргументов командной строки
    parser = setup_parser()
    
    # Разбираю аргументы которые ввёл пользователь
    args = parser.parse_args()
    
    try:
        # Создаю объект для работы с файлом заметок
        storage = NoteStorage()
        
        # Создаю объект для выполнения команд
        commands = NoteCommands(storage)
        
        # Проверяю какую команду ввёл пользователь и выполняю её
        if args.add:
            # Команда добавления заметки
            if not args.title or not args.content:
                print("Ошибка: для добавления заметки нужно указать --title и --content")
                return
            
            # Вызываю метод добавления заметки
            commands.add_note(args.title, args.content)
        
        elif args.list:
            # Команда показа всех заметок
            commands.list_notes(args.date)
        
        elif args.search:
            # Команда поиска заметок
            commands.search_notes(args.search, args.date)
        
        elif args.delete:
            # Команда удаления заметки
            commands.delete_note(args.delete)
        
        else:
            # Если команда не распознана - показываю справку
            print("Неизвестная команда. Доступные команды:")
            parser.print_help()
    
    except Exception as e:
        # Ловлю все возможные ошибки чтобы программа не "упала"
        print(f"Произошла ошибка: {e}")

# Эта строка означает что код выполнится только если файл запущен напрямую
if __name__ == "__main__":
    main()
