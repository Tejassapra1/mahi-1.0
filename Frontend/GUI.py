from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget, QLineEdit, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
from PyQt5.QtCore import Qt, QSize, QTimer, QUrl
from PyQt5.QtGui import QDesktopServices
from dotenv import dotenv_values
import sys
import os

env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def TempDictonaryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = "\n".join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):

    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "when", "where", "who", "which", "why", "can you", "whom", "whose", "what's", "where's"]

    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "?"
        else:
            new_query += "?"
    
    else:
        if query_words[-1][-1] in [".", "?", "!"]:
            new_query = new_query[:-1] + "."
        else:
            new_query += "."

    return new_query.capitalize()

def SetMicrophoneStatus(Command):
    with open(rf"{TempDirPath}\Mic.data", "w", encoding="utf-8") as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(rf"{TempDirPath}\Mic.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open (rf"{TempDirPath}\Status.data", "w", encoding="utf-8") as file:
        file.write(Status)

def GetAssistantStatus():
    with open (rf"{TempDirPath}\Status.data", "r", encoding="utf-8") as file:
        Status = file.read()
    return Status

def MicButtonInitialed():
    SetMicrophoneStatus("False")

def MicButtonClosed():
    SetMicrophoneStatus("True")

def GraphicsDictonaryPath(Filename):
    Path = rf"{GraphicsDirPath}\{Filename}"
    return Path

def TempDirectoryPath(Filename):
    Path = rf"{TempDirPath}\{Filename}"
    return Path

def ShowTextToScreen(Text):
    with open(rf"{TempDirPath}\Responses.data", "w", encoding="utf-8") as file:
        file.write(Text)

class ChatSection(QWidget):

    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(-10, 40, 40, 100)
        layout.setSpacing(-100)
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
        self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
        # Set chat box background and text color
        self.chat_text_edit.setStyleSheet(
            "background-color: #181818; color: #e0e0e0; border-radius: 8px;"
        )
        layout.addWidget(self.chat_text_edit)
        self.setStyleSheet("background-color: black;")
        layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
        layout.setStretch(1, 1)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
        text_color = QColor(Qt.blue)
        text_color_text = QTextCharFormat()
        text_color_text.setForeground(text_color)
        self.chat_text_edit.setCurrentCharFormat(text_color_text)
        # --- Animation state movies ---
        self.state_movies = {
            "idle": QMovie(GraphicsDictonaryPath("Jarvis_Idle.gif")),
            "listening": QMovie(GraphicsDictonaryPath("Jarvis_Listening.gif")),
            "thinking": QMovie(GraphicsDictonaryPath("Jarvis_Thinking.gif")),
            "speaking": QMovie(GraphicsDictonaryPath("Jarvis_Speaking.gif")),
        }
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("border: none;")
        self.setAnimationState("idle")  # Default state
        layout.addWidget(self.gif_label)
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-right: 195px; border: none; margin-top: -30px;")
        self.label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.label)
        layout.setSpacing(-10)
        layout.addWidget(self.gif_label)
        font = QFont()
        font.setPointSize(13)
        font.setFamily("Orbitron")
        self.chat_text_edit.setFont(font)

        # --- Add chat input box and send button ---
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type your message or command...")
        # Set input box color
        self.input_box.setStyleSheet(
            "background-color: #23272e; color: #ffffff; border-radius: 8px; padding: 6px;"
        )
        self.input_box.returnPressed.connect(self.send_message)
        self.send_button = QPushButton("Send")
        # Set send button color
        self.send_button.setStyleSheet(
            "background-color: #0078d7; color: white; border-radius: 8px; padding: 6px 16px;"
        )
        self.send_button.clicked.connect(self.send_message)
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)
        layout.addLayout(input_layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)
        self.chat_text_edit.viewport().installEventFilter(self)
        self.setStyleSheet("""
                QScrollBar:vertical {
                    border: none;
                    background: black;
                    width: 10px;
                    margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical {
                    background: white;
                    min-height: 20px;
                }
                QScrollBar::add-line:vertical {
                    background: black;
                    subcontrol-position: bottom;
                    subcontrol-origin: margin;
                    height: 10px;
                }
                QScrollBar::sub-line:vertical {
                    background: black;
                    subcontrol-position: top;
                    subcontrol-origin: margin;
                    height: 10px;
                }
                QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {
                    border: none;
                    background: none;
                    color: none;
                }
                QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                    background: none;
                }
            """)

    def send_message(self):
        from main import HandleUserQuery  # Import here to avoid circular imports at module level
        user_text = self.input_box.text().strip()
        if user_text:
            # Show user message in chat
            Username = "User"
            self.chat_text_edit.setTextColor(QColor("green"))
            self.chat_text_edit.append(f"{Username}: {user_text}")
            self.input_box.clear()

            # Unified backend handling (voice & chat)
            HandleUserQuery(user_text)

    def display_image(self, image_path):
        # Display image in chat as a clickable link (or inline if you want)
        if os.path.exists(image_path):
            self.chat_text_edit.append(f'<a href="file:///{image_path}"><img src="file:///{image_path}" width="256"></a>')
            self.chat_text_edit.setOpenExternalLinks(True)

    def get_ai_response(self, user_text):
        # TODO: Replace this with your actual assistant/model logic
        # For demo, just echo the user_text
        # You can integrate your ChatBot, RealtimeSearchEngine, or Automation here
        return f"Echo: {user_text}"

    def generate_images(self, prompt):
        # Dummy implementation: Replace with your actual image generation logic
        # For now, just return a placeholder image path if exists
        placeholder_path = GraphicsDictonaryPath("placeholder.png")
        if os.path.exists(placeholder_path):
            return placeholder_path
        else:
            return None

    def get_weather(self, city):
        # Dummy implementation: Replace with actual weather fetching logic
        if not city:
            return "Please specify a city for the weather."
        return f"Weather information for {city} is currently unavailable."

    def loadMessages(self):
        
        global old_chat_message

        with open(TempDirectoryPath("Responses.data"), "r", encoding="utf-8") as file:
            messages = file.read()

            if None == messages:
                pass

            elif len(messages) <= 1:
                pass

            elif str(old_chat_message)==str(messages):
                pass

            else:
                self.addMessage(message=messages, color="White")
                old_chat_message = messages

    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            status = file.read().strip()
            self.label.setText(status)

            if "Listening" in status:
                self.setAnimationState("listening")
            elif "Thinking" in status:
                self.setAnimationState("thinking")
            elif "Answering" in status or "Speaking" in status:
                self.setAnimationState("speaking")
            else:
                self.setAnimationState("idle")

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):

        if self.toggled:
            self.load_icon(GraphicsDictonaryPath("voice.png"), 60, 60)
            MicButtonInitialed()
        
        else:
            self.load_icon(GraphicsDictonaryPath("mic.png"), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

    def addMessage(self, message, color):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        formatm = QTextBlockFormat()
        formatm.setTopMargin(10)
        formatm.setLeftMargin(10)
        Username = "User"
        if "You:" in message or Username in message:
            format.setForeground(QColor("#39FF14"))  # User: green
        else:
            format.setForeground(QColor("#00FFFF"))  # Assistant: neon cyan
        cursor.setCharFormat(format)
        cursor.setBlockFormat(formatm)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

    def setAnimationState(self, state):
        if state in self.state_movies:
            movie = self.state_movies[state]
            movie.setScaledSize(QSize(480, 270))
            self.gif_label.setMovie(movie)
            movie.start()

class InitialScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        gif_label = QLabel()
        movie = QMovie(GraphicsDictonaryPath("Jarvis.gif"))
        gif_label.setMovie(movie)
        max_gif_size_H = int(screen_width / 16 * 9)
        movie.setScaledSize(QSize(screen_width, max_gif_size_H))
        gif_label.setAlignment(Qt.AlignCenter)
        movie.start()
        gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.icon_label = QLabel()
        pixmap = QPixmap(GraphicsDictonaryPath("Mic_on.png"))
        new_pixmap = pixmap.scaled(60, 60)
        self.icon_label.setPixmap(new_pixmap)
        self.icon_label.setFixedSize(150, 150)
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.toggled = True
        self.toggle_icon()
        self.icon_label.mousePressEvent = self.toggle_icon
        self.label = QLabel("")
        self.label.setStyleSheet("color: white; font-size: 16px; margin-bottom: 0;")
        content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.label, alignment=Qt.AlignCenter)
        content_layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        content_layout.setContentsMargins(0, 0, 0, 150)
        self.setLayout(content_layout)
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)
        self.setStyleSheet("background-color: black;")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(5)

        # --- Background GIF ---
        bg_label = QLabel(self)
        bg_label.setMovie(QMovie("Frontend/Graphics/bg-loop.gif"))
        bg_label.lower()  # Sends behind all widgets

    def SpeechRecogText(self):
        with open(TempDirectoryPath("Status.data"), "r", encoding="utf-8") as file:
            messages = file.read()
            self.label.setText(messages)

    def load_icon(self, path, width=60, height=60):
        pixmap = QPixmap(path)
        new_pixmap = pixmap.scaled(width, height)
        self.icon_label.setPixmap(new_pixmap)

    def toggle_icon(self, event=None):
        
        if self.toggled:
            self.load_icon(GraphicsDictonaryPath("Mic_on.png"), 60, 60)
            MicButtonInitialed()
        
        else:
            self.load_icon(GraphicsDictonaryPath("Mic_off.png"), 60, 60)
            MicButtonClosed()

        self.toggled = not self.toggled

class MessageScreen(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        layout = QVBoxLayout()
        label = QLabel("")
        layout.addWidget(label)
        chat_section = ChatSection()
        layout.addWidget(chat_section)
        self.setLayout(layout)
        self.setStyleSheet("background-color: black;")
        self.setFixedHeight(screen_height)
        self.setFixedWidth(screen_width)

class CustomTopBar(QWidget):

    def __init__(self, parent, stack_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen = None
        self.stack_widget = stack_widget

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon = QIcon(GraphicsDictonaryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("  Home")
        home_button.setStyleSheet("height:40px; line-height:40px ; background-color:white ; color: black")
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDictonaryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("  Chat")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white ; color: black")
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDictonaryPath("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white")
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDictonaryPath("Maximize.png"))
        self.restore_icon = QIcon(GraphicsDictonaryPath("Minimize.png"))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:white")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button = QPushButton()
        close_icon = QIcon(GraphicsDictonaryPath("Close.png"))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:white")
        close_button.clicked.connect(self.close_window)
        line_frame = QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setFrameShadow(QFrame.Sunken)
        line_frame.setStyleSheet("border-color: black;")
        title_label = QLabel(f" {str(Assistantname).capitalize()}  AI  ")
        title_label.setStyleSheet("color: black; font-size: 18px;; background-color: white")
        home_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stack_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable = True
        self.offset = None
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.white)
        super().paintEvent(event)

    def minimizeWindow(self):
        self.parent().showMinimized()

    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.maximize_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)

    def close_window(self):
        self.parent().close()

    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset
            self.parent().move(new_pos)

    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen = message_screen

    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()

        intial_screen = InitialScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(intial_screen)
        self.current_screen = intial_screen
        
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        desktop = QApplication.desktop()
        screeen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen()
        message_screen = MessageScreen()
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0, 0, screeen_width, screen_height)
        self.setStyleSheet("background-color: black;")
        top_bar = CustomTopBar(self, stacked_widget)
        self.setMenuWidget(top_bar)
        self.setCentralWidget(stacked_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    GraphicalUserInterface()