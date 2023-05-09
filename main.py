from PIL import Image, ImageDraw, ImageFont
import os

from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QLabel, QVBoxLayout, QPushButton, QHBoxLayout, \
    QLineEdit, QListWidget


class WatermarkApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Text Adder")
        self.setGeometry(100, 100, 600, 400)

        self.img_dir = ''
        self.modified_dir = ''

        # Widgets
        self.img_label = QLabel()
        self.img_label.setAlignment(Qt.AlignCenter)

        self.img_list = QListWidget()

        self.img_select_button = QPushButton("Select Image Directory")
        self.img_select_button.clicked.connect(self.select_img_dir)

        self.textbox = QLineEdit()
        self.textbox.setPlaceholderText("Enter Text to Add")

        self.add_text_button = QPushButton("Add Text to Images")
        self.add_text_button.clicked.connect(self.add_text_to_images)

        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)

        # Layout
        vbox = QVBoxLayout()

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.img_label)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.img_select_button)
        hbox2.addWidget(self.img_list)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.textbox)

        hbox4 = QHBoxLayout()
        hbox4.addWidget(self.add_text_button)
        hbox4.addWidget(self.quit_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)

        self.setLayout(vbox)


    def select_img_dir(self):
        self.img_dir = QFileDialog.getExistingDirectory(self, "Select Image Directory")
        self.modified_dir = os.path.join(self.img_dir, "modified images")
        os.makedirs(self.modified_dir, exist_ok=True)

        for file_name in os.listdir(self.img_dir):
            if file_name.lower().endswith(('.jpg', '.jpeg', '.png')):
                self.img_list.addItem(file_name)

    def add_text_to_images(self):
        text = self.textbox.text()

        for i in range(self.img_list.count()):
            file_name = self.img_list.item(i).text()
            image_path = os.path.join(self.img_dir, file_name)

            # Open the image
            img = Image.open(image_path)

            # Get the image size
            width, height = img.size

            # Create a font
            font_size = int(width / 10)  # set the font size based on the width of the image
            font = ImageFont.truetype('arial.ttf', font_size)

            # Create a draw object
            draw = ImageDraw.Draw(img)

            # Get the text size
            text_width, text_height = draw.textsize(text, font)

            # Calculate the position for the text
            text_x = width - text_width - 10
            text_y = height - text_height - 10

            # Draw the text
            draw.text((text_x, text_y), text, font=font, fill=(255, 255, 255, 128))

            # Save the modified image
            modified_file_name = "modified_" + file_name
            modified_image_path = os.path.join(self.modified_dir, modified_file_name)
            img.save(modified_image_path)

            # Add the modified image name to the list
            self.img_list.addItem(modified_file_name)




if __name__ == "__main__":
    # Create the application and show the window
    app = QApplication([])
    window = WatermarkApp()

    window.show()
    style_file = QFile("stylesheet.qss")
    style_file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(style_file)
    app.setStyleSheet(stream.readAll())
    app.exec_()
