import tkinter as tk
import numpy as np
import pickle
from PIL import Image, ImageDraw, ImageOps

with open("hand_written_digit_recognizer.pkl", "rb") as file:
    print("loading model...")
    model = pickle.load(file)
    print("model loaded successfully.")

def predict_digit(img):
    img = img.resize((28, 28))
    img = ImageOps.grayscale(img)
    img = np.array(img)
    img = np.invert(img)
    img = img.reshape(1, 28, 28, 1)
    img = img / 255.0
    prediction = model.predict([img])
    return np.argmax(prediction)

class DigitPredictor:
    
    BOX_SIZE = 200
    
    def __init__(self):
        print("running...")
        self.window = tk.Tk()
        self.window.geometry("480x300")
        self.window.resizable(False, False)
        self.window.title("Hand Written Digit Predictor")
        
        self.canvas = tk.Canvas(self.window, width=self.BOX_SIZE, height=self.BOX_SIZE, bg="white", highlightbackground="#adacac", highlightthickness=1)
        self.canvas.grid(row=0, column=0, padx=25, pady=15)

        
        self.digit_frame = tk.Frame(self.window, width=self.BOX_SIZE, height=self.BOX_SIZE, bg="white", highlightbackground="#adacac", highlightthickness=1)
        self.digit_frame.grid(row=0, column=1)
        
        self.prediction_label = tk.Label(self.digit_frame, font=("Arial", 96), foreground="black", bg="white")
        self.prediction_label.place(x=65, y=25)
        
        self.btn_frame = tk.Frame(self.window, width=self.BOX_SIZE, height=50)
        self.btn_frame.grid(row=1, column=0)
        
        self.predict_btn = tk.Button(self.btn_frame, width=13, height=2, text="predict digit", command=self.predict)
        self.predict_btn.grid(row=0, column=0, pady=5)
        
        self.clear_btn = tk.Button(self.btn_frame, width=13, height=2, text="clear screen", command=self.clear_canvas)
        self.clear_btn.grid(row=0, column=1, pady=5)
        
        self.prediction_text = tk.Label(self.window, text="Model Prediction", font=("Arial", 12), foreground="black")
        self.prediction_text.grid(row=1, column=1)
        
        self.canvas.bind("<B1-Motion>", self.paint)
        
        self.image = Image.new("RGB", (self.BOX_SIZE, self.BOX_SIZE), 'white')
        self.draw = ImageDraw.Draw(self.image)
        
        self.window.mainloop()
      
    def paint(self, event):
        x, y = event.x, event.y
        radius = 5
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, fill='black')
        self.draw.ellipse([x-radius, y-radius, x+radius, y+radius], fill='black')
        
    def clear_canvas(self):
        self.canvas.delete("all")
        self.draw.rectangle([0, 0, self.BOX_SIZE, self.BOX_SIZE], fill='white')
        
    def predict(self):
        img = self.image.copy()
        digit = predict_digit(img)
        self.prediction_label.config(text=f"{digit}")


digit_predictor = DigitPredictor()