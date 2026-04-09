import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageEnhance
from backend import WeatherBackend
import os


class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aesthetic Weather App")
        self.root.geometry("430x860")
        self.root.resizable(False, False)

        self.backend = WeatherBackend()

        self.canvas = tk.Canvas(self.root, width=430, height=860, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.set_background()

        self.main_frame = tk.Frame(self.root, bg="#101424")
        self.canvas.create_window(215, 430, window=self.main_frame, width=410, height=840)

        self.build_ui()
        self.search_weather()

    def set_background(self):
        image_path = os.path.join("assets", "bg.jpg")

        if os.path.exists(image_path):
            bg = Image.open(image_path).resize((430, 860))
            bg = ImageEnhance.Brightness(bg).enhance(0.45)
            self.bg_photo = ImageTk.PhotoImage(bg)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        else:
            self.canvas.configure(bg="#101424")

    def create_card(self, parent, width=120, height=110, bg="#ffffff", fg="white"):
        frame = tk.Frame(parent, bg=bg, width=width, height=height, highlightthickness=0)
        frame.pack_propagate(False)
        return frame

    def build_ui(self):
        top_bar = tk.Frame(self.main_frame, bg="#101424")
        top_bar.pack(fill="x", pady=(10, 6), padx=10)

        self.location_label = tk.Label(
            top_bar, text="Noida",
            font=("Arial", 20, "bold"),
            fg="white", bg="#101424"
        )
        self.location_label.pack(side="left")

        search_wrap = tk.Frame(self.main_frame, bg="#101424")
        search_wrap.pack(fill="x", padx=10, pady=(0, 10))

        self.city_entry = tk.Entry(
            search_wrap,
            font=("Arial", 13),
            bg="#20263a",
            fg="white",
            insertbackground="white",
            relief="flat"
        )
        self.city_entry.pack(side="left", fill="x", expand=True, ipady=9, padx=(0, 10))
        self.city_entry.insert(0, "Noida")

        self.search_btn = tk.Button(
            search_wrap,
            text="Search",
            font=("Arial", 11, "bold"),
            bg="#ffffff",
            fg="#111111",
            relief="flat",
            activebackground="#ffffff",
            activeforeground="#111111",
            command=self.search_weather
        )
        self.search_btn.pack(side="right", ipadx=10, ipady=7)

        self.city_entry.bind("<Return>", lambda event: self.search_weather())

        center = tk.Frame(self.main_frame, bg="#101424")
        center.pack(fill="x", padx=10, pady=(4, 14))

        self.temp_label = tk.Label(
            center, text="24°",
            font=("Arial", 44, "bold"),
            fg="white", bg="#101424"
        )
        self.temp_label.pack()

        self.condition_label = tk.Label(
            center, text="⛅ Partly cloudy",
            font=("Arial", 18),
            fg="#dce3ff", bg="#101424"
        )
        self.condition_label.pack(pady=(0, 10))

        self.pollen_label = tk.Label(
            center, text="Pollen: Moderate",
            font=("Arial", 13, "bold"),
            fg="#ffd66b", bg="#101424"
        )
        self.pollen_label.pack()

        grid_wrap = tk.Frame(self.main_frame, bg="#101424")
        grid_wrap.pack(padx=10, pady=8)

        self.uv_card = self.make_info_card(grid_wrap, "UV", "0", "row=0,col=0")
        self.feels_card = self.make_info_card(grid_wrap, "Feels like", "24°", "row=0,col=1")
        self.humidity_card = self.make_info_card(grid_wrap, "Humidity", "50%", "row=0,col=2")
        self.wind_card = self.make_info_card(grid_wrap, "Wind", "Breeze", "row=1,col=0")
        self.pressure_card = self.make_info_card(grid_wrap, "Air pressure", "1014 hPa", "row=1,col=1")
        self.visibility_card = self.make_info_card(grid_wrap, "Visibility", "4 km", "row=1,col=2")

        self.uv_card.grid(row=0, column=0, padx=6, pady=6)
        self.feels_card.grid(row=0, column=1, padx=6, pady=6)
        self.humidity_card.grid(row=0, column=2, padx=6, pady=6)
        self.wind_card.grid(row=1, column=0, padx=6, pady=6)
        self.pressure_card.grid(row=1, column=1, padx=6, pady=6)
        self.visibility_card.grid(row=1, column=2, padx=6, pady=6)

        self.sun_frame = tk.Frame(self.main_frame, bg="#252c44", width=380, height=130)
        self.sun_frame.pack(padx=10, pady=10)
        self.sun_frame.pack_propagate(False)

        top_sun = tk.Frame(self.sun_frame, bg="#252c44")
        top_sun.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(top_sun, text="Sunset", fg="white", bg="#252c44",
                 font=("Arial", 12, "bold")).pack(side="left")
        tk.Label(top_sun, text="Sunrise", fg="white", bg="#252c44",
                 font=("Arial", 12, "bold")).pack(side="right")

        self.sun_bar = tk.Canvas(self.sun_frame, width=330, height=28, bg="#252c44", highlightthickness=0)
        self.sun_bar.pack()
        self.sun_bar.create_line(12, 14, 318, 14, fill="#8390d8", width=6, capstyle="round")
        self.sun_bar.create_text(165, 14, text="🌙", fill="white", font=("Arial", 16))

        bottom_sun = tk.Frame(self.sun_frame, bg="#252c44")
        bottom_sun.pack(fill="x", padx=16, pady=(8, 0))

        self.sunset_label = tk.Label(bottom_sun, text="6:43 pm", fg="white", bg="#252c44",
                                     font=("Arial", 17, "bold"))
        self.sunset_label.pack(side="left")

        self.sunrise_label = tk.Label(bottom_sun, text="6:01 am", fg="white", bg="#252c44",
                                      font=("Arial", 17, "bold"))
        self.sunrise_label.pack(side="right")

        self.tip_frame = tk.Frame(self.main_frame, bg="#1f2740", width=380, height=210)
        self.tip_frame.pack(padx=10, pady=12)
        self.tip_frame.pack_propagate(False)

        title_row = tk.Frame(self.tip_frame, bg="#1f2740")
        title_row.pack(fill="x", padx=16, pady=(12, 6))

        tk.Label(title_row, text="Lifestyle tips", fg="white", bg="#1f2740",
                 font=("Arial", 14, "bold")).pack(side="left")

        self.tips_container = tk.Frame(self.tip_frame, bg="#1f2740")
        self.tips_container.pack(fill="both", expand=True, padx=12, pady=6)

        self.tip_labels = []
        for i in range(6):
            lbl = tk.Label(
                self.tips_container,
                text="Tip",
                fg="white",
                bg="#1f2740",
                font=("Arial", 11),
                wraplength=100,
                justify="center"
            )
            lbl.grid(row=i // 3, column=i % 3, padx=8, pady=16)
            self.tip_labels.append(lbl)

    def make_info_card(self, parent, title, value, tag):
        frame = tk.Frame(parent, bg="#252c44", width=118, height=108)
        frame.pack_propagate(False)

        title_label = tk.Label(
            frame, text=title,
            font=("Arial", 11),
            fg="#d8dcf0", bg="#252c44"
        )
        title_label.pack(anchor="w", padx=10, pady=(16, 4))

        value_label = tk.Label(
            frame, text=value,
            font=("Arial", 20, "bold"),
            fg="white", bg="#252c44"
        )
        value_label.pack(anchor="w", padx=10)

        frame.title_label = title_label
        frame.value_label = value_label
        return frame

    def build_tips(self, data):
        tips = []

        uv = data["uv_index"] if isinstance(data["uv_index"], (int, float)) else 0
        if uv >= 6:
            tips.append("☂ Moderate/High UV")
        else:
            tips.append("🌤 Low UV")

        pollen = data["pollen_level"]
        if pollen in ["High", "Very High"]:
            tips.append("🌼 High pollen count")
        elif pollen == "Moderate":
            tips.append("😷 Moderate pollen")
        else:
            tips.append("✅ Low pollen")

        if data["humidity"] >= 70:
            tips.append("💧 Humid weather")
        else:
            tips.append("🧴 Oil-control friendly")

        if isinstance(data["visibility"], (int, float)) and data["visibility"] >= 5:
            tips.append("🚗 Good traffic conditions")
        else:
            tips.append("🚦 Low visibility outside")

        if "Rain" in data["condition"] or "drizzle" in data["condition"].lower():
            tips.append("☔ Carry umbrella")
        else:
            tips.append("🏃 Good for outdoor walk")

        if data["temperature"] >= 32:
            tips.append("🥤 Stay hydrated")
        else:
            tips.append("🏠 Comfortable indoors")

        for lbl, text in zip(self.tip_labels, tips):
            lbl.config(text=text)

    def search_weather(self):
        city = self.city_entry.get().strip()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return

        try:
            data = self.backend.get_weather_data(city)

            self.location_label.config(text=data["location"])
            self.temp_label.config(text=f'{data["temperature"]}°')
            self.condition_label.config(text=f'{data["emoji"]} {data["condition"]}')

            pollen_text = f'Pollen: {data["pollen_level"]}'
            if data["pollen_value"] != "N/A":
                pollen_text += f' ({data["pollen_value"]})'
            self.pollen_label.config(text=pollen_text)

            self.uv_card.value_label.config(text=str(data["uv_index"]))
            self.feels_card.value_label.config(text=f'{data["feels_like"]}°')
            self.humidity_card.value_label.config(text=f'{data["humidity"]}%')
            self.wind_card.value_label.config(text=f'{data["wind_direction"]} {data["wind_speed"]} km/h')
            self.pressure_card.value_label.config(text=f'{data["pressure"]} hPa')
            self.visibility_card.value_label.config(text=f'{data["visibility"]} km' if data["visibility"] != "N/A" else "N/A")

            self.sunset_label.config(text=data["sunset"])
            self.sunrise_label.config(text=data["sunrise"])

            self.build_tips(data)

        except Exception as e:
            messagebox.showerror("Weather Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()