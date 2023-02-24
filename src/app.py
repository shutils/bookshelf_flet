from models import init_db
import flet as ft
from component import AddBookForm, BookListView

init_db()


def main(page: ft.Page):
    page.title = "Bookshelf"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 400
    book_list_view = BookListView(page)

    page.add(
        ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    tab_content=ft.Icon(ft.icons.HOME),
                    content=book_list_view,
                ),
                ft.Tab(
                    tab_content=ft.Icon(ft.icons.ADD),
                    content=AddBookForm(main_page=page),
                ),
            ],
            expand=True,
            # タブが切り替わったときに本をリフレッシュする
            on_change=book_list_view.refresh_books,
        )
    )


ft.app(target=main)
