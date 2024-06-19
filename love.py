import random
import re
from collections import Counter
from typing import Tuple
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window

# Set window size
Window.size = (600, 1200)

# Constants for vowels, consonants, and alphabet values
CONSONANTS = "bcdfghjklmnprstvwxyz"
VOWELS = "aeiou"
ALPHABET_VALUES = {char: idx for idx, char in enumerate("abcdefghijklmnopqrstuvwxyz", start=1)}

# Functions for counting vowels and consonants
def count_vowels(name: str) -> int:
    return sum(Counter(re.findall(f'[{VOWELS}]', name.lower())).values())

def count_consonants(name: str) -> int:
    return sum(Counter(re.findall(f'[{CONSONANTS}]', name.lower())).values())

# Function to calculate love score
def calculate_love_score(name1: str, name2: str) -> int:
    love_score = 0
    vowels_count1, vowels_count2 = count_vowels(name1), count_vowels(name2)
    consonants_count1, consonants_count2 = count_consonants(name1), count_consonants(name2)

    if vowels_count1 == vowels_count2:
        love_score += random.randint(10, 30)
    if consonants_count1 == consonants_count2:
        love_score += random.randint(20, 40)
    if name1.strip().lower()[0] == name2.strip().lower()[0]:
        love_score += random.randint(10, 30)
    if len(name1.strip()) == len(name2.strip()):
        love_score += random.randint(1, 10)
    love_score += random.randint(10, 50)

    return min(love_score, 100)

# Numerology functions
def numerology_value(name: str) -> int:
    value = sum(ALPHABET_VALUES.get(char, 0) for char in name.lower() if char.isalpha())
    return reduce_to_digit(value)

def reduce_to_digit(number: int) -> int:
    while number > 9 and number not in {11, 22}:
        number = sum(int(digit) for digit in str(number))
    return number

def calculate_numerology(name: str) -> Tuple[int, int, int, int]:
    cleaned_name = re.sub(r'[^a-z]', '', name.lower())

    destiny_number = numerology_value(cleaned_name)
    soul_urge_number = numerology_value(''.join([char for char in cleaned_name if char in VOWELS]))
    personality_number = numerology_value(''.join([char for char in cleaned_name if char in CONSONANTS]))

    life_path_number = destiny_number  # Simplified for this context

    return life_path_number, destiny_number, soul_urge_number, personality_number

def numerology_description(number: int) -> str:
    descriptions = {
        1: "Leadership, independence, and originality.",
        2: "Cooperation, balance, and sensitivity.",
        3: "Creativity, social interaction, and optimism.",
        4: "Practicality, hard work, and stability.",
        5: "Freedom, adventure, and dynamic energy.",
        6: "Responsibility, care, and community.",
        7: "Introspection, spiritual development, and wisdom.",
        8: "Ambition, business acumen, and material success.",
        9: "Humanitarianism, compassion, and idealism.",
        11: "Spiritual insight, intuition, and inspiration.",
        22: "Master builder, large-scale endeavors, and practical idealism."
    }
    return descriptions.get(number, "Unique and special qualities.")

class LoveCalculatorApp(App):
    def build(self):
        self.title = "Love Harmony Meter"

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        title = Label(text="Love Harmony Meter", font_size=36, size_hint=(1, 0.1))
        layout.add_widget(title)

        self.name1_input = TextInput(
            hint_text='Enter Name 1',
            multiline=False,
            size_hint=(1, 0.1),
            font_size=24
        )
        layout.add_widget(self.name1_input)

        self.name2_input = TextInput(
            hint_text='Enter Name 2',
            multiline=False,
            size_hint=(1, 0.1),
            font_size=24
        )
        layout.add_widget(self.name2_input)

        calculate_button = Button(
            text="Calculate Love Score & Numerology",
            size_hint=(1, 0.2),
            font_size=24,
            background_color=(1, 0.4, 0.4, 1),
            on_press=self.on_calculate
        )
        layout.add_widget(calculate_button)

        # Add buttons for different sections
        self.show_love_button = Button(
            text="Show Love Score",
            size_hint=(1, 0.1),
            font_size=20,
            background_color=(0.5, 0.5, 1, 1),
            on_press=self.show_love_score
        )
        layout.add_widget(self.show_love_button)

        self.show_numerology1_button = Button(
            text="Show Numerology for Name 1",
            size_hint=(1, 0.1),
            font_size=20,
            background_color=(0.5, 1, 0.5, 1),
            on_press=self.show_numerology1
        )
        layout.add_widget(self.show_numerology1_button)

        self.show_numerology2_button = Button(
            text="Show Numerology for Name 2",
            size_hint=(1, 0.1),
            font_size=20,
            background_color=(1, 0.5, 0.5, 1),
            on_press=self.show_numerology2
        )
        layout.add_widget(self.show_numerology2_button)

        self.result_label = Label(
            text="",
            font_size=20,
            size_hint=(1, 0.1),
            color=(0.1, 0.6, 0.6, 1)
        )
        layout.add_widget(self.result_label)

        self.numerology_label = Label(
            text="",
            font_size=16,
            size_hint=(1, 0.4),
            color=(0.2, 0.2, 0.8, 1)
        )
        layout.add_widget(self.numerology_label)

        return layout

    def on_calculate(self, instance):
        self.name1 = self.name1_input.text.strip()
        self.name2 = self.name2_input.text.strip()

        if not self.name1 or not self.name2:
            self.show_popup("Error", "Please enter both names.")
            return

        self.love_score = calculate_love_score(self.name1, self.name2)
        self.numerology1 = calculate_numerology(self.name1)
        self.numerology2 = calculate_numerology(self.name2)

        # Clear the result and numerology labels
        self.result_label.text = ""
        self.numerology_label.text = ""

    def show_love_score(self, instance):
        if hasattr(self, 'love_score'):
            self.result_label.text = f"{self.name1} and {self.name2} have a {self.love_score}% relationship."
        else:
            self.show_popup("Error", "Please calculate first by pressing 'Calculate Love Score & Numerology'.")

    def show_numerology1(self, instance):
        if hasattr(self, 'numerology1'):
            numerology_text = f"Numerology Insights for {self.name1}:\n\n" \
                              f"Life Path Number: {self.numerology1[0]} ({numerology_description(self.numerology1[0])})\n" \
                              f"Destiny Number: {self.numerology1[1]} ({numerology_description(self.numerology1[1])})\n" \
                              f"Soul Urge Number: {self.numerology1[2]} ({numerology_description(self.numerology1[2])})\n" \
                              f"Personality Number: {self.numerology1[3]} ({numerology_description(self.numerology1[3])})\n"
            self.numerology_label.text = numerology_text
        else:
            self.show_popup("Error", "Please calculate first by pressing 'Calculate Love Score & Numerology'.")

    def show_numerology2(self, instance):
        if hasattr(self, 'numerology2'):
            numerology_text = f"Numerology Insights for {self.name2}:\n\n" \
                              f"Life Path Number: {self.numerology2[0]} ({numerology_description(self.numerology2[0])})\n" \
                              f"Destiny Number: {self.numerology2[1]} ({numerology_description(self.numerology2[1])})\n" \
                              f"Soul Urge Number: {self.numerology2[2]} ({numerology_description(self.numerology2[2])})\n" \
                              f"Personality Number: {self.numerology2[3]} ({numerology_description(self.numerology2[3])})\n"
            self.numerology_label.text = numerology_text
        else:
            self.show_popup("Error", "Please calculate first by pressing 'Calculate Love Score & Numerology'.")

    def show_popup(self, title, message):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(Label(text=message, font_size=18))
        close_button = Button(text="Close", size_hint=(1, 0.3), on_press=self.close_popup)
        popup_layout.add_widget(close_button)
        
        self.popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.5))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

if __name__ == '__main__':
    LoveCalculatorApp().run()
