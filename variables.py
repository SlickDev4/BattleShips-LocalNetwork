from widgets import Button, Text

"""
    This is a variables file
                            """

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (210, 210, 210)
ORANGE = (255, 128, 0)

menu_buttons = [
    Button(text="New Game", font_size=30, x=425, y=150, width=350, height=100, color=BLACK, text_color=WHITE),
    Button(text="Exit", font_size=30, x=425, y=400, width=350, height=100, color=BLACK, text_color=WHITE)
]

texts = [
    Text(text="You", size=40, color=GREEN, x=190, y=5),
    Text(text="Ships left", size=25, color=WHITE, x=35, y=75),
    Text(text="Moves left", size=25, color=WHITE, x=175, y=75),
    Text(text="Ships killed", size=25, color=WHITE, x=330, y=75),
    Text(text="20", size=25, color=WHITE, x=75, y=120),
    Text(text="50", size=25, color=WHITE, x=215, y=120),
    Text(text="0", size=25, color=WHITE, x=380, y=120),

    Text(text="Enemy", size=40, color=RED, x=880, y=5),
    Text(text="Ships left", size=25, color=WHITE, x=735, y=75),
    Text(text="Moves left", size=25, color=WHITE, x=875, y=75),
    Text(text="Ships killed", size=25, color=WHITE, x=1030, y=75),
    Text(text="20", size=25, color=WHITE, x=775, y=120),
    Text(text="50", size=25, color=WHITE, x=915, y=120),
    Text(text="0", size=25, color=WHITE, x=1080, y=120)
]

waiting_text = Text(text="Waiting for another player...", size=50, color=WHITE, x=250, y=250)

end_texts = [
    Text(text="You Won", size=70, color=GREEN, x=300, y=200),
    Text(text="You Lost", size=70, color=RED, x=300, y=200),
    Text(text="Tie Match!", size=70, color=GRAY, x=300, y=200)
]

back_to_menu_btn = Button(
    text="Back to Menu", font_size=30, x=425, y=400, width=350, height=100, color=GRAY, text_color=BLACK)

field_background_pos = [[25, 175, 443, 443], [725, 175, 443, 443]]
stats_text_background_pos = [[25, 5, 443, 160], [725, 5, 443, 160]]
