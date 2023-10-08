from rxconfig import config
import reflex as rx
import json


class JsonState(rx.State):
    json_text: str = ''
    error_message: str = ''  # поле для отображения сообщения об ошибке

    def update_json_text(self, text: str):
        self.json_text = text
        self.error_message = ''  # очистка ошибки при изменении текста

    def format_json(self):
        try:
            formatted_json = json.dumps(json.loads(self.json_text), indent=4)
            self.json_text = formatted_json
            self.error_message = ""  # очистка ошибки при успешном форматировании
        except json.JSONDecodeError:
            self.error_message = "Ошибка: введенный текст не является корректным JSON."


def index() -> rx.Component:
    return rx.container(
        rx.card(
            rx.vstack(
                rx.box("JSON Editor"),
                rx.box(
                    rx.text_area(value=JsonState.json_text, placeholder="Вставьте или напишите JSON здесь...",
                                 on_change=JsonState.update_json_text, width='md')
                ),
                rx.button("Форматировать JSON", on_click=JsonState.format_json),
                rx.cond(JsonState.error_message,
                        rx.box(JsonState.error_message),
                        rx.box("")
                )
            )
        )
    )


# Add state and page to the app.
app = rx.App()
app.add_page(index)  # передаем класс JsonState как аргумент
app.compile()
