import sys
import csv
import datetime
from googletrans import Translator
from gtts import gTTS
import os
import pyperclip
import pygame  # Added pygame for audio playback
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, \
    QTextEdit, QComboBox, QGroupBox, QFormLayout, QListWidget, QFileDialog, QMenuBar, QAction, QMenu
from PyQt5.QtCore import Qt

# Define available languages (Expanded List)
languages = {
    'en': 'English',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'ml': 'Malayalam',
    'bn': 'Bengali',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'pa': 'Punjabi',
    'mr': 'Marathi',
    'or': 'Odia',
    'as': 'Assamese',
    'ur': 'Urdu',
    'ne': 'Nepali',
    'sd': 'Sindhi',
    'kok': 'Konkani',
    'ks': 'Kashmiri',
    'sa': 'Sanskrit',
    'mai': 'Maithili',
    'sat': 'Santali',
    'si': 'Sinhala',  # Sinhala
    'my': 'Burmese',  # Burmese
    'ar': 'Arabic',  # Arabic
    'fr': 'French',  # French
    'de': 'German',  # German
    'es': 'Spanish',  # Spanish
    'pt': 'Portuguese',  # Portuguese
    'it': 'Italian',  # Italian
    'ja': 'Japanese',  # Japanese
    'zh-cn': 'Chinese Simplified',  # Chinese Simplified
    'zh-tw': 'Chinese Traditional',  # Chinese Traditional
    'ko': 'Korean',  # Korean
    'ru': 'Russian',  # Russian
    'tr': 'Turkish',  # Turkish
    'pl': 'Polish',  # Polish
    'nl': 'Dutch',  # Dutch
    'sv': 'Swedish',  # Swedish
    'no': 'Norwegian',  # Norwegian
    'fi': 'Finnish',  # Finnish
    'da': 'Danish',  # Danish
    'cs': 'Czech',  # Czech
    'ro': 'Romanian',  # Romanian
    'hu': 'Hungarian',  # Hungarian
    'he': 'Hebrew',  # Hebrew
    'el': 'Greek',  # Greek
    'uk': 'Ukrainian',  # Ukrainian
    'th': 'Thai',  # Thai
    'vi': 'Vietnamese',  # Vietnamese
    'ms': 'Malay',  # Malay
    'sw': 'Swahili',  # Swahili
    'tl': 'Tagalog',  # Tagalog
    'id': 'Indonesian'  # Indonesian
}

# Reverse map for dropdowns
lang_names_to_codes = {v: k for k, v in languages.items()}


class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Translator & TTS App")
        self.setGeometry(100, 100, 600, 500)

        self.audio_file = None  # Audio file will be generated for each translation dynamically
        self.translator = Translator()

        self.default_font = "Arial"
        self.malayalam_font = "Karthika"

        self.recent_languages = []
        self.translation_history = []

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)

        # Input section
        self.input_text = QTextEdit(self)
        self.input_text.setPlaceholderText("Enter Text...")
        self.input_text.setStyleSheet(
            """background-color: #f4f7fc; border: 1px solid #b0c4de; border-radius: 5px; padding: 10px; color: #333333; font-size: 14px; font-family: 'Arial';""")
        main_layout.addWidget(QLabel("Enter Text:"))
        main_layout.addWidget(self.input_text)

        # Buttons (Paste, Speak, Translate, Clear)
        button_layout = QHBoxLayout()

        paste_button = QPushButton("Paste", self)
        paste_button.setStyleSheet(
            """background-color: #1e90ff; color: white; border-radius: 5px; padding: 10px 20px;""")
        paste_button.clicked.connect(self.paste_text)
        button_layout.addWidget(paste_button)

        speak_button = QPushButton("Speak", self)
        speak_button.setStyleSheet(
            """background-color: #1e90ff; color: white; border-radius: 5px; padding: 10px 20px;""")
        speak_button.clicked.connect(self.speech_to_text)
        button_layout.addWidget(speak_button)

        translate_button = QPushButton("Translate", self)
        translate_button.setStyleSheet(
            """background-color: #32cd32; color: white; border-radius: 5px; padding: 10px 20px;""")
        translate_button.clicked.connect(self.translate_text)
        button_layout.addWidget(translate_button)

        clear_button = QPushButton("Clear Text", self)
        clear_button.setStyleSheet(
            """background-color: #ff6347; color: white; border-radius: 5px; padding: 10px 20px;""")
        clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(clear_button)

        main_layout.addLayout(button_layout)

        # Language selection dropdowns
        self.source_lang_combobox = QComboBox(self)
        self.source_lang_combobox.addItems(languages.values())
        self.source_lang_combobox.setStyleSheet(
            """background-color: #f4f7fc; border: 1px solid #b0c4de; border-radius: 5px; padding: 10px;""")
        main_layout.addWidget(QLabel("Source Language:"))
        main_layout.addWidget(self.source_lang_combobox)

        self.target_lang_combobox = QComboBox(self)
        self.target_lang_combobox.addItems(languages.values())
        self.target_lang_combobox.setStyleSheet(
            """background-color: #f4f7fc; border: 1px solid #b0c4de; border-radius: 5px; padding: 10px;""")
        main_layout.addWidget(QLabel("Target Language:"))
        main_layout.addWidget(self.target_lang_combobox)

        # Output section
        self.output_text = QTextEdit(self)
        self.output_text.setPlaceholderText("Translated Text...")
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet(
            """background-color: #f4f7fc; border: 1px solid #b0c4de; border-radius: 5px; padding: 10px; color: #333333; font-size: 14px; font-family: 'Arial';""")
        main_layout.addWidget(QLabel("Translated Text:"))
        main_layout.addWidget(self.output_text)

        # Translation history
        self.history_listbox = QListWidget(self)
        self.history_listbox.setStyleSheet(
            """background-color: #f4f7fc; border: 1px solid #b0c4de; border-radius: 5px; padding: 10px;""")
        main_layout.addWidget(QLabel("Translation History:"))
        main_layout.addWidget(self.history_listbox)

        # Footer buttons (Copy, Play Audio, Download Audio)
        footer_layout = QHBoxLayout()

        copy_button = QPushButton("Copy to Clipboard", self)
        copy_button.setStyleSheet(
            """background-color: #1e90ff; color: white; border-radius: 5px; padding: 10px 20px;""")
        copy_button.clicked.connect(self.copy_text)
        footer_layout.addWidget(copy_button)

        play_button = QPushButton("Play Audio", self)
        play_button.setStyleSheet(
            """background-color: #1e90ff; color: white; border-radius: 5px; padding: 10px 20px;""")
        play_button.clicked.connect(self.play_audio)
        footer_layout.addWidget(play_button)

        download_button = QPushButton("Download Audio", self)
        download_button.setStyleSheet(
            """background-color: #1e90ff; color: white; border-radius: 5px; padding: 10px 20px;""")
        download_button.clicked.connect(self.download_audio)
        footer_layout.addWidget(download_button)

        main_layout.addLayout(footer_layout)

        # Set window styles
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                color: #444444;
                font-size: 16px;
                font-family: 'Arial';
            }
            QComboBox, QTextEdit, QPushButton {
                font-family: 'Arial';
            }
        """)

        # Initialize pygame mixer
        pygame.mixer.init()

        # Create Menu Bar
        self.create_menu()

    def translate_text(self):
        input_text = self.input_text.toPlainText().strip()
        if not input_text:
            print("Please enter text to translate.")
            return

        src_lang = lang_names_to_codes.get(self.source_lang_combobox.currentText(), 'en')
        tgt_lang = lang_names_to_codes.get(self.target_lang_combobox.currentText(), 'en')

        if src_lang == tgt_lang:
            print("Source and Target languages cannot be the same.")
            return

        try:
            result = self.translator.translate(input_text, src=src_lang, dest=tgt_lang)
            translated_text = result.text
            self.output_text.setPlainText(translated_text)

            # Add to translation history in QListWidget
            history_item = f"From {languages[src_lang]} to {languages[tgt_lang]}: {translated_text}"
            self.history_listbox.addItem(history_item)

            # Save translation to CSV
            self.save_translation_to_csv(input_text, translated_text, src_lang, tgt_lang)

            # Generate a new unique audio file for each translation
            self.audio_file = f"translated_output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
            tts = gTTS(translated_text, lang=tgt_lang)
            tts.save(self.audio_file)
            print("Translation complete, audio is ready.")
        except Exception as e:
            print(f"Translation failed: {str(e)}")

    def save_translation_to_csv(self, input_text, translated_text, src_lang, tgt_lang):
        date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        translation_entry = [date_str, input_text, translated_text, src_lang, tgt_lang]
        self.translation_history.append(translation_entry)

        # Save to CSV
        try:
            with open("translations.csv", mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(translation_entry)
            print("Translation saved to CSV.")
        except Exception as e:
            print(f"Error saving to CSV: {e}")

    def copy_text(self):
        # Copy translated text to clipboard
        pyperclip.copy(self.output_text.toPlainText())
        print("Text copied to clipboard.")

    def play_audio(self):
        # Play the saved audio file (updated for each new translation)
        try:
            if self.audio_file and os.path.exists(self.audio_file):
                pygame.mixer.music.load(self.audio_file)
                pygame.mixer.music.play()
                print("Audio is now playing.")
            else:
                print("Audio file not found.")
        except Exception as e:
            print(f"Error playing audio: {e}")

    def download_audio(self):
        # Save the translated speech as an audio file
        try:
            filename, _ = QFileDialog.getSaveFileName(self, "Save Audio File", "", "MP3 Files (*.mp3)")
            if filename:
                tts = gTTS(self.output_text.toPlainText())
                tts.save(filename)
                print("Audio file saved successfully.")
        except Exception as e:
            print(f"Error saving audio: {e}")

    def speech_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Please speak something...")
            audio = recognizer.listen(source)
            try:
                spoken_text = recognizer.recognize_google(audio)
                print(f"You said: {spoken_text}")
                self.input_text.setPlainText(spoken_text)
            except Exception as e:
                print(f"Could not recognize speech: {str(e)}")

    def paste_text(self):
        # Paste text from clipboard
        clipboard_text = pyperclip.paste()
        self.input_text.setPlainText(clipboard_text)

    def clear_text(self):
        # Clear all fields
        self.input_text.clear()
        self.output_text.clear()

    def create_menu(self):
        menubar = self.menuBar()
        file_menu = QMenu("File", self)
        file_menu.addAction("Exit", self.close)
        menubar.addMenu(file_menu)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TranslatorApp()
    window.show()
    sys.exit(app.exec_())
