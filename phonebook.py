"""Консольная телефонная книга с хранением контактов в JSON-файле."""

import json
from pathlib import Path


DATA_FILE = Path("data/contacts.json")


def load_contacts() -> list[dict[str, str]]:
    """Загрузить контакты из файла или вернуть пустой список."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            contacts = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Не удалось прочитать файл контактов. Открыта пустая книга.")
        return []

    if not isinstance(contacts, list):
        print("Файл контактов имеет неверный формат. Открыта пустая книга.")
        return []

    return contacts


def save_contacts(contacts: list[dict[str, str]]) -> None:
    """Сохранить все контакты в JSON-файл."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(contacts, file, ensure_ascii=False, indent=4)


def show_contacts(contacts: list[dict[str, str]]) -> None:
    """Показать все сохранённые контакты."""
    if not contacts:
        print("\nТелефонная книга пуста.")
        return

    print("\n--- Список контактов ---")
    for index, contact in enumerate(contacts, start=1):
        print(f"{index}. {contact['name']} — {contact['phone']}")
    print("-" * 28)


def add_contact(contacts: list[dict[str, str]]) -> None:
    """Получить данные пользователя и добавить новый контакт."""
    name = input("Введите имя: ").strip()
    phone = input("Введите номер телефона: ").strip()

    if not name or not phone:
        print("Имя и номер не могут быть пустыми.")
        return

    contacts.append({"name": name, "phone": phone})
    save_contacts(contacts)
    print(f"Контакт «{name}» успешно добавлен.")


def search_contact(contacts: list[dict[str, str]]) -> None:
    """Найти контакты по части имени."""
    query = input("Введите имя для поиска: ").strip().casefold()
    if not query:
        print("Введите имя или его часть.")
        return

    found_contacts = [
        contact for contact in contacts if query in contact["name"].casefold()
    ]

    if not found_contacts:
        print("Контакт не найден.")
        return

    print(f"\nНайдено контактов: {len(found_contacts)}")
    for contact in found_contacts:
        print(f"- {contact['name']}: {contact['phone']}")


def show_menu() -> None:
    """Вывести пункты главного меню."""
    print("\n1. Показать контакты")
    print("2. Добавить контакт")
    print("3. Найти контакт")
    print("4. Выход")


def main() -> None:
    """Запустить консольное приложение."""
    contacts = load_contacts()

    while True:
        show_menu()
        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            show_contacts(contacts)
        elif choice == "2":
            add_contact(contacts)
        elif choice == "3":
            search_contact(contacts)
        elif choice == "4":
            print("До свидания!")
            break
        else:
            print("Неверный выбор, попробуйте снова.")


if __name__ == "__main__":
    main()
