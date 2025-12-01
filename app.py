from shiny import ui, render, App

app_ui = ui.page_fluid(
    ui.input_slider(
        "sleep",
        "How many hours of sleep do you get normally?",
        min=0, max=10, value=5
    ),
    ui.input_slider(
        "mindfulness",
        "How many minutes of mindfulness do you practice a day?",
        min=0, max=60, value=30
    ),
      ui.input_slider(
        "hydration" ,
        "How many litres of water do you drink a day?",
        min=0.5, max=5, value=1
    ),
    ui.output_text_verbatim("value"),
)

def server(input, output, session):
    @render.text
    def value():
        return f"Sleep: {input.sleep()}, Mindfulness: {input.mindfulness()}, Hydration: {input.hydration()}"

app = App(app_ui, server)
