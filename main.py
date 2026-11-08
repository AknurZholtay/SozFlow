import flet as ft
import asyncio
from words import words

def main(page: ft.Page):
    page.title="SozFlow"
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    page.padding = 30
    page.bgcolor = "#F7F9FC"
    current_word_index = 0
    auto_change_enabled = False
    auto_change_seconds = 5
    known_words = []
    review_words = []
    english_word_text = ft.Text(
        words[0]["english"],
        size=30,
        weight=ft.FontWeight.BOLD,
        )
    translation_text = ft.Text(
        words[0]["kazakh"],
        size=20,
        color="#5F6B7A"
        )
    status_text = ft.Text("",size=16)

    def show_next_word(e):
        nonlocal current_word_index
        current_word_index = (current_word_index + 1) % len(words)
        english_word_text.value = words[current_word_index]["english"]
        translation_text.value = words[current_word_index]["kazakh"]
        translation_text.update()
        page.update()
        print("Батырма басылды.")

    async  def auto_change_words():
        nonlocal current_word_index

        while auto_change_enabled:
            await asyncio.sleep(auto_change_seconds)
            
            if auto_change_enabled:
                current_word_index = (current_word_index + 1) % len(words)
                english_word_text.value = words[current_word_index]["english"]
                translation_text.value = words[current_word_index]["kazakh"]
                
                page.update(
                english_word_text,
                translation_text
                )


    def toggle_auto_change(e):
        nonlocal auto_change_enabled
        auto_change_enabled = e.control.value

        if e.control.value:
            page.run_task(auto_change_words)

    def change_auto_interval(e):
        nonlocal auto_change_seconds
        auto_change_seconds = int(e.control.value)
        print(f"Автоматты ауыстыру уақыты {auto_change_seconds} секундқа өзгертілді.")

    def mark_as_known(e):
        current_word = words[current_word_index]

        if current_word not in known_words:
            known_words.append(current_word)

        status_text.value = f"{current_word["english"]}-сөз білемін тізіміне қосылды"
        status_text.update()

        print(known_words)

    def mark_for_review(e):
        current_word = words[current_word_index]

        if current_word not in review_words:
            review_words.append(current_word)   

        status_text.value = f"{current_word["english"]}-сөз қайта қарау тізіміне қосылды"
        status_text.update()  
        print(review_words)
    
    word_content = ft.Column(
        controls=[
            english_word_text,
            translation_text
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
    )   

    word_card = ft.Container(
        content=word_content,
        width=320,
        padding=30,
        bgcolor="#EAF2FF",
        border_radius=20,
    ) 

    page.add(ft.Text("SozFlow",size=28,weight=ft.FontWeight.BOLD))
    page.add(word_card)

    page.add(
            ft.Button(
                content="Келесі сөз", 
                on_click=show_next_word,
                bgcolor="#3B82F6",
                color="#FFFFFF",
            ),
    )        
    page.add(
        ft.Row(
            controls=[
                ft.Button(
                    content="Білемін",
                    on_click=mark_as_known,
                ),
                ft.Button(
                    content="Қайта қарау",
                    on_click=mark_for_review,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.add(status_text)
    page.add(
        ft.Dropdown(
            on_select=change_auto_interval,
            label="Ауысу уақыты",
            width=180,
            value="5",
            options=[
                ft.DropdownOption(key="5", text="5 секунд"),
                ft.DropdownOption(key="10", text="10 секунд"),
            ]
        )
    )
    page.add(
        ft.Switch(
            label="Автоматты ауыстыру",
            value=False,
            on_change=toggle_auto_change,
        )
    )

ft.run(main)