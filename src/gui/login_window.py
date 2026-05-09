"""
Giriş Ekranı - Microsoft ve Offline
"""
import customtkinter as ctk
from tkinter import messagebox

class LoginWindow:
    def __init__(self, parent, on_login):
        self.parent = parent
        self.on_login = on_login
        self.frame = None
    
    def show(self):
        """Giriş ekranını göster"""
        # Ana frame - Gradient arka plan efekti
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=("#E8F4F8", "#0A0E27")
        )
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Sol panel - Dekoratif
        left_panel = ctk.CTkFrame(
            self.frame,
            fg_color=("#00D9FF", "#001F3F"),
            corner_radius=0
        )
        left_panel.place(relx=0, rely=0, relwidth=0.4, relheight=1)
        
        # Logo
        logo = ctk.CTkLabel(
            left_panel,
            text="TencenT",
            font=("Arial Black", 48, "bold"),
            text_color="#FFFFFF"
        )
        logo.place(relx=0.5, rely=0.4, anchor="center")
        
        subtitle = ctk.CTkLabel(
            left_panel,
            text="Minecraft Launcher",
            font=("Arial", 18),
            text_color="#CCCCCC"
        )
        subtitle.place(relx=0.5, rely=0.5, anchor="center")
        
        # Sağ panel - Giriş formu
        right_panel = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        right_panel.place(relx=0.4, rely=0, relwidth=0.6, relheight=1)
        
        # Giriş container
        login_container = ctk.CTkFrame(
            right_panel,
            fg_color="transparent"
        )
        login_container.place(relx=0.5, rely=0.5, anchor="center")
        
        # Başlık
        title = ctk.CTkLabel(
            login_container,
            text="Hoş Geldiniz",
            font=("Arial Bold", 32),
            text_color=("#000000", "#FFFFFF")
        )
        title.pack(pady=(0, 10))
        
        desc = ctk.CTkLabel(
            login_container,
            text="Devam etmek için giriş yapın",
            font=("Arial", 14),
            text_color=("#666666", "#AAAAAA")
        )
        desc.pack(pady=(0, 40))
        
        # Microsoft giriş butonu
        microsoft_btn = ctk.CTkButton(
            login_container,
            text="🔐 Microsoft ile Giriş Yap",
            font=("Arial Bold", 16),
            height=50,
            width=350,
            fg_color="#00A4EF",
            hover_color="#0078D4",
            corner_radius=10,
            command=self.login_microsoft
        )
        microsoft_btn.pack(pady=10)
        
        # Ayırıcı
        separator_frame = ctk.CTkFrame(
            login_container,
            fg_color="transparent"
        )
        separator_frame.pack(pady=20, fill="x")
        
        ctk.CTkLabel(
            separator_frame,
            text="veya",
            font=("Arial", 12),
            text_color=("#999999", "#666666")
        ).pack()
        
        # Offline giriş
        offline_frame = ctk.CTkFrame(
            login_container,
            fg_color="transparent"
        )
        offline_frame.pack(pady=10)
        
        ctk.CTkLabel(
            offline_frame,
            text="Kullanıcı Adı:",
            font=("Arial", 12),
            text_color=("#333333", "#CCCCCC")
        ).pack(anchor="w", pady=(0, 5))
        
        self.username_entry = ctk.CTkEntry(
            offline_frame,
            width=350,
            height=40,
            placeholder_text="Minecraft kullanıcı adınız",
            font=("Arial", 14),
            corner_radius=10
        )
        self.username_entry.pack(pady=(0, 10))
        
        offline_btn = ctk.CTkButton(
            offline_frame,
            text="🎮 Offline Oyna",
            font=("Arial Bold", 16),
            height=50,
            width=350,
            fg_color=("#00D9FF", "#00A8CC"),
            hover_color=("#00B8DD", "#008899"),
            corner_radius=10,
            command=self.login_offline
        )
        offline_btn.pack()
        
        # Alt bilgi
        info = ctk.CTkLabel(
            login_container,
            text="Offline modda çevrimiçi özelliklere erişemezsiniz",
            font=("Arial", 10),
            text_color=("#999999", "#666666")
        )
        info.pack(pady=(20, 0))
    
    def login_microsoft(self):
        """Microsoft ile giriş"""
        # TODO: Microsoft OAuth implementasyonu
        messagebox.showinfo(
            "Geliştirme Aşamasında",
            "Microsoft girişi yakında eklenecek!\nŞimdilik Offline modunu kullanın."
        )
    
    def login_offline(self):
        """Offline giriş"""
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Hata", "Lütfen bir kullanıcı adı girin!")
            return
        
        if len(username) < 3:
            messagebox.showerror("Hata", "Kullanıcı adı en az 3 karakter olmalı!")
            return
        
        # Kullanıcı verisi
        user_data = {
            "username": username,
            "type": "offline",
            "uuid": f"offline-{username}",
            "skin_url": None
        }
        
        # Giriş ekranını kapat
        if self.frame:
            self.frame.destroy()
        
        # Callback'i çağır
        self.on_login(user_data)
