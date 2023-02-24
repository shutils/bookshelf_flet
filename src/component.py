import flet as ft
from models import Book, delete_book, create_book, get_book_all


class BookListView(ft.ListView):
    def __init__(self, main_page: ft.Page):
        super().__init__()
        self.main_page = main_page
        self.refresh_books(None)

    def refresh_books(self, e):
        # 既存のコントロールをクリアして取得した本を追加する
        self.controls.clear()
        books = get_book_all()
        for book in books:
            self.controls.append(BookCard(book, self, self.main_page))
        self.main_page.update()


class BookCard(ft.Card):
    def __init__(self, book: Book, parent: ft.ListView, main_page: ft.Page):
        super().__init__()
        self.id = book.id
        self.parent = parent
        self.main_page = main_page
        self.dlg = ft.AlertDialog(
            title=ft.Text("削除してよろしいですか？"),
            actions=[
                ft.ElevatedButton("Yes", on_click=self.delete_record),
                ft.ElevatedButton("No", on_click=self.close_dlg),
            ]
        )
        self.content = ft.Container(
            content=ft.Column(
                [
                    ft.ListTile(
                        title=ft.Text(book.title),
                        subtitle=ft.Text("Some text.")
                    ),
                    ft.Row(
                        [
                            ft.Container(content=ft.ElevatedButton("削除", on_click=self.confirm, style=ft.ButtonStyle(
                                color={ft.MaterialState.DEFAULT: ft.colors.WHITE},
                                bgcolor={ft.MaterialState.DEFAULT: ft.colors.RED},
                                shape={
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=8)}
                            )), padding=5),
                        ], alignment=ft.MainAxisAlignment.END),
                ]
            )
        )

    def delete_record(self, e):
        delete_book(self.id)
        self.parent.controls.remove(self)
        self.dlg.open = False
        self.main_page.update()

    def confirm(self, e):
        self.main_page.dialog = self.dlg
        self.dlg.open = True
        self.main_page.update()

    def close_dlg(self, e):
        self.dlg.open = False
        self.main_page.update()


class AddBookForm(ft.Column):
    def __init__(self, main_page: ft.Page):
        super().__init__()
        self.input_field = ft.TextField()
        self.main_page = main_page
        self.controls = [
            ft.Text("タイトル"),
            self.input_field,
            ft.FilledButton("追加", on_click=self.add_book, icon=ft.icons.ADD)
        ]

    def add_book(self, e):
        create_book(self.input_field.value)
        dlg = ft.AlertDialog(
            title=ft.Text("本を追加しました")
        )
        self.main_page.dialog = dlg
        dlg.open = True
        self.main_page.update()
