import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod


class Book:
    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content


class DisplayStrategy(ABC):
    @abstractmethod
    def display(self, content: str) -> None:
        pass


class ConsoleDisplayStrategy(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content)


class ReverseDisplayStrategy(DisplayStrategy):
    def display(self, content: str) -> None:
        print(content[::-1])


class PrintStrategy(ABC):
    @abstractmethod
    def print(self, title: str, content: str) -> None:
        pass


class ConsolePrintStrategy(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book: {title}...")
        print(content)


class ReversePrintStrategy(PrintStrategy):
    def print(self, title: str, content: str) -> None:
        print(f"Printing the book in reverse: {title}...")
        print(content[::-1])


class SerializeStrategy(ABC):
    @abstractmethod
    def serialize(self, title: str, content: str) -> str:
        pass


class JSONSerializeStrategy(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        return json.dumps({"title": title, "content": content})


class XMLSerializeStrategy(SerializeStrategy):
    def serialize(self, title: str, content: str) -> str:
        root = ET.Element("book")
        title_elem = ET.SubElement(root, "title")
        title_elem.text = title
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content
        return ET.tostring(root, encoding="unicode")


class BookService:
    def __init__(self, book: Book, display_strategy: DisplayStrategy,
                 print_strategy: PrintStrategy, serialize_strategy: SerializeStrategy):
        self.book = book
        self.display_strategy = display_strategy
        self.print_strategy = print_strategy
        self.serialize_strategy = serialize_strategy

    def display(self) -> None:
        self.display_strategy.display(self.book.content)

    def print_book(self) -> None:
        self.print_strategy.print(self.book.title, self.book.content)

    def serialize(self) -> str:
        return self.serialize_strategy.serialize(self.book.title, self.book.content)


def main(book: Book, commands: list[tuple[str, str]]) -> None | str:
    for cmd, method_type in commands:
        if cmd == "display":
            if method_type == "console":
                service = BookService(book, ConsoleDisplayStrategy(), None, None)
            elif method_type == "reverse":
                service = BookService(book, ReverseDisplayStrategy(), None, None)
            else:
                raise ValueError(f"Unknown display type: {method_type}")
            service.display()
        elif cmd == "print":
            if method_type == "console":
                service = BookService(book, None, ConsolePrintStrategy(), None)
            elif method_type == "reverse":
                service = BookService(book, None, ReversePrintStrategy(), None)
            else:
                raise ValueError(f"Unknown print type: {method_type}")
            service.print_book()
        elif cmd == "serialize":
            if method_type == "json":
                service = BookService(book, None, None, JSONSerializeStrategy())
            elif method_type == "xml":
                service = BookService(book, None, None, XMLSerializeStrategy())
            else:
                raise ValueError(f"Unknown serialize type: {method_type}")
            return service.serialize()


if __name__ == "__main__":
    sample_book = Book("Sample Book", "This is some sample content.")
    print(main(sample_book, [("display", "reverse"), ("serialize", "xml")]))
