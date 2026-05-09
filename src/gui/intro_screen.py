"""
Intro Ekranı - Video veya Animasyon
"""
import customtkinter as ctk
from tkinter import Canvas
from PIL import Image, ImageTk
import threading
import time
from pathlib import Path
import sys
import os

class IntroScreen:
    def __init__(self, parent, on_complete):
        self.parent = parent
        self.on_complete = on_complete
        self.frame = None
        self.animation_running = True
        self.video_path = self.find_intro_video()
        
    def find_intro_video(self):
        """intro.mp4 dosyasını bul"""
        # Olası konumlar
        if getattr(sys, 'frozen', False):
            base_path = Path(sys._MEIPASS)
        else:
            base_path = Path(__file__).parent.parent.parent
        
        possible_paths = [
            base_path / "intro.mp4",
            base_path / "assets" / "intro.mp4",
            Path.cwd() / "intro.mp4",
            Path.cwd() / "assets" / "intro.mp4"
        ]
        
        for path in possible_paths:
            if path.exists():
                return path
        return None
    
    def play(self):
        """Intro'yu oynat"""
        # Ana frame
        self.frame = ctk.CTkFrame(self.parent, fg_color="#0A0E27")
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Video varsa oynat, yoksa animasyon göster
        if self.video_path:
            self.play_video()
        else:
            self.play_animation()
    
    def play_video(self):
        """intro.mp4 videosunu oynat"""
        try:
            import cv2
            
            # Video container
            video_label = ctk.CTkLabel(self.frame, text="")
            video_label.place(relx=0.5, rely=0.5, anchor="center")
            
            # Skip butonu
            skip_btn = ctk.CTkButton(
                self.frame,
                text="Atla ⏭",
                width=100,
                height=30,
                fg_color="#00D9FF",
                hover_color="#00B8DD",
                command=self.finish
            )
            skip_btn.place(relx=0.95, rely=0.05, anchor="ne")
            
            def play_frames():
                cap = cv2.VideoCapture(str(self.video_path))
                fps = cap.get(cv2.CAP_PROP_FPS)
                delay = int(1000 / fps) if fps > 0 else 33
                
                while self.animation_running:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    # BGR to RGB
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    
                    # Resize to fit window
                    frame = cv2.resize(frame, (1100, 700))
                    
                    # Convert to PhotoImage
                    img = Image.fromarray(frame)
                    photo = ImageTk.PhotoImage(image=img)
                    
                    # Update label
                    self.parent.after(0, lambda p=photo: video_label.configure(image=p))
                    video_label.image = photo
                    
                    time.sleep(delay / 1000)
                
                cap.release()
                self.parent.after(0, self.finish)
            
            threading.Thread(target=play_frames, daemon=True).start()
            
        except ImportError:
            # opencv-python yüklü değil, animasyon göster
            print("opencv-python bulunamadı, animasyon gösteriliyor...")
            self.play_animation()
        except Exception as e:
            print(f"Video oynatma hatası: {e}")
            self.play_animation()
    
    def play_animation(self):
        """Animasyonlu intro (video yoksa)"""
        # Logo container
        logo_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        logo_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # TencenT Logo (animasyonlu)
        self.logo_label = ctk.CTkLabel(
            logo_frame,
            text="TencenT",
            font=("Arial Black", 72, "bold"),
            text_color="#00D9FF"
        )
        self.logo_label.pack(pady=10)
        
        # Launcher alt yazı
        self.subtitle = ctk.CTkLabel(
            logo_frame,
            text="LAUNCHER",
            font=("Arial", 28),
            text_color="#FFFFFF"
        )
        self.subtitle.pack()
        
        # Yükleme çubuğu
        self.progress = ctk.CTkProgressBar(
            logo_frame,
            width=300,
            height=4,
            fg_color="#1A1F3A",
            progress_color="#00D9FF"
        )
        self.progress.pack(pady=30)
        self.progress.set(0)
        
        # Yükleme metni
        self.loading_text = ctk.CTkLabel(
            logo_frame,
            text="Yükleniyor...",
            font=("Arial", 12),
            text_color="#888888"
        )
        self.loading_text.pack()
        
        # Skip butonu
        skip_btn = ctk.CTkButton(
            self.frame,
            text="Atla ⏭",
            width=100,
            height=30,
            fg_color="#00D9FF",
            hover_color="#00B8DD",
            command=self.finish
        )
        skip_btn.place(relx=0.95, rely=0.05, anchor="ne")
        
        # Animasyonu başlat
        threading.Thread(target=self.animate, daemon=True).start()
    
    def animate(self):
        """Intro animasyonu"""
        # Fade in
        for i in range(0, 101, 5):
            if not self.animation_running:
                return
            self.progress.set(i / 100)
            
            # Yükleme metni animasyonu
            dots = "." * ((i // 10) % 4)
            self.loading_text.configure(text=f"Yükleniyor{dots}")
            
            time.sleep(0.05)
        
        # Kısa bekleme
        time.sleep(0.5)
        
        # Fade out
        self.loading_text.configure(text="Hazır!")
        time.sleep(0.3)
        
        # Intro'yu kapat ve devam et
        self.parent.after(0, self.finish)
    
    def finish(self):
        """Intro'yu bitir"""
        self.animation_running = False
        if self.frame:
            self.frame.destroy()
        self.on_complete()
