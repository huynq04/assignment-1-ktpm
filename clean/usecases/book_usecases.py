"""Use cases for book operations"""
from typing import List
from domain.entities import Book
from interfaces.repositories import IBookRepository


class ListBooksUseCase:
    """Use case for listing all books"""
    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo
    
    def execute(self) -> List[Book]:
        """Get all books"""
        return self.book_repo.get_all()


class GetBookByIdUseCase:
    """Use case for getting a book by ID"""
    
    def __init__(self, book_repo: IBookRepository):
        self.book_repo = book_repo
    
    def execute(self, book_id: int) -> Book:
        """Get book by ID"""
        book = self.book_repo.get_by_id(book_id)
        if not book:
            raise ValueError("Book not found")
        return book
