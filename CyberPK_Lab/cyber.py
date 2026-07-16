import flet as ft
import os
from google import genai
from google.genai import types

client = genai.Client()

def main(page: ft.Page):
    page.title = "CYBER_PK // MESSAGE_BUFFER"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#000000" 
    page.padding = 24
    page.window_width = 400
    page.window_height = 700
    page.scroll = ft.ScrollMode.AUTO 
    
    CYAN = "#00f0ff"
    MAGENTA = "#ff0055"
    GREY_DARK = "#0d0d0d"
    TEXT_WHITE = "#ffffff"

    generated_responses = {"direct": "", "cordial": "", "exit": ""}

    title = ft.Text(
        "CYBER_PK // v1.0", 
        size=22, 
        color=CYAN, 
        weight=ft.FontWeight.BOLD,
        font_family="monospace"
    )
    
    status_prompt = ft.Text(
        "STATUS: AWAITING_INPUT", 
        size=11, 
        color=MAGENTA,
        font_family="monospace"
    )

    input_field = ft.TextField(
        label="INPUT_BUFFER (Paste message here)",
        label_style=ft.TextStyle(color=CYAN, font_family="monospace"),
        border_color=CYAN,
        focused_border_color=MAGENTA,
        color=TEXT_WHITE,
        multiline=True,
        min_lines=3,
        max_lines=5,
        cursor_color=MAGENTA
    )

    output_area = ft.Text(
        "Awaiting intent processing...",
        size=14,
        color=CYAN,
        font_family="monospace"
    )

    output_container = ft.Container(
        content=output_area,
        bgcolor="transparent",  
        border=ft.Border(
            top=ft.BorderSide(1, CYAN),
            bottom=ft.BorderSide(1, CYAN),
            left=ft.BorderSide(1, CYAN),
            right=ft.BorderSide(1, CYAN)
        ),
        padding=16,
        border_radius=8,
        visible=False
    )

    def process_message(e):
        user_text = input_field.value
        if not user_text:
            status_prompt.value = "ERROR: EMPTY_INPUT"
            page.update()
            return

        status_prompt.value = "STATUS: DECRYPTING_TONE_AND_GENERATING_OPTIONS..."
        page.update()

        prompt_engineering = f"""
        You are an asynchronous communication assistant for neurodivergent individuals. 
        Analyze the following received message and generate exactly THREE short, pragmatic response options without excessive social fluff.
        The options must strictly follow these profiles:
        [DIRECT]: A clear, objective response that resolves the problem in one line.
        [CORDIAL]: A polite response, maintaining a friendly/corporate social filter, but without long blocks of text.
        [EXIT]: A graceful exit to end the interaction politely or ask for time to reply later.

        Received Message: "{user_text}"

        Return the result strictly in plain text format separated by markers, without additional comments:
        DIRECT: <your response here>
        CORDIAL: <your response here>
        EXIT: <your response here>
        """

        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt_engineering,
            )
            
            lines = response.text.split("\n")
            for line in lines:
                if line.startswith("DIRECT:"):
                    generated_responses["direct"] = line.replace("DIRECT:", "").strip()
                elif line.startswith("CORDIAL:"):
                    generated_responses["cordial"] = line.replace("CORDIAL:", "").strip()
                elif line.startswith("EXIT:"):
                    generated_responses["exit"] = line.replace("EXIT:", "").strip()

            status_prompt.value = "STATUS: INTENTS_READY"
            button_container.visible = True
            page.update()

        except Exception as ex:
            status_prompt.value = f"API_ERROR: {str(ex)}"
            page.update()

    def select_option(option):
        final_text = generated_responses[option]
        output_area.value = final_text
        output_container.visible = True
        
        page.set_clipboard(final_text)
        status_prompt.value = f"STATUS: COPIED_TO_CLIPBOARD ({option.upper()})"
        page.update()

    def read_local_clipboard(e):
        copied_text = page.get_clipboard()
        if copied_text:
            input_field.value = copied_text
            page.update()

    btn_paste = ft.Button(
        content=ft.Text("📋", size=18),
        bgcolor="transparent",
        on_click=read_local_clipboard,
        tooltip="Auto-paste from clipboard",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=4),
            padding=0  
        )
    )

    btn_process = ft.Button(
        content=ft.Text("PROCESS_INTENT", color=TEXT_WHITE, font_family="monospace"),
        bgcolor=MAGENTA,
        on_click=process_message,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4))
    )

    button_container = ft.Column(
        visible=False,
        controls=[
            ft.Text("SELECT OUTPUT INTENT:", color=TEXT_WHITE, size=12, font_family="monospace"),
            ft.Button(
                content=ft.Text("[⚡] DIRECT_MODE", color=CYAN, font_family="monospace"),
                bgcolor="transparent",
                on_click=lambda _: select_option("direct"),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4),
                    side=ft.BorderSide(1, CYAN)
                )
            ),
            ft.Button(
                content=ft.Text("[🤝] CORDIAL_MODE", color=CYAN, font_family="monospace"),
                bgcolor="transparent",
                on_click=lambda _: select_option("cordial"),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4),
                    side=ft.BorderSide(1, CYAN)
                )
            ),
            ft.Button(
                content=ft.Text("[🚪] GRACEFUL_EXIT", color=MAGENTA, font_family="monospace"),
                bgcolor="transparent",
                on_click=lambda _: select_option("exit"),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=4),
                    side=ft.BorderSide(1, MAGENTA)
                )
            ),
        ]
    )

    page.add(
        ft.Row([title, btn_paste], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        status_prompt,
        ft.Divider(color=CYAN, height=10, thickness=1),
        ft.Container(height=10), 
        input_field,
        ft.Row([btn_process], alignment=ft.MainAxisAlignment.END),
        ft.Container(height=15), 
        button_container,
        ft.Container(height=15), 
        output_container
    )

if __name__ == "__main__":
    ft.run(main)