"""
Ana Oyun Ekranı - Sürüm seçimi, Oyna, Skin
"""
import customtkinter as ctk
from tkinter import messagebox
import threading
from pathlib import Path

from src.core.version_manager import VersionManager
from src.core.launcher import MinecraftLauncher
from src.gui.skin_market import SkinMarket

class GameScreen:
    def __init__(self, parent, user_data):
        self.parent = parent
        self.user_data = user_data
        self.frame = None
        self.version_manager = VersionManager()
        self.launcher = MinecraftLauncher()
        self.selected_version = None
        self.versions = []
        
    def show(self):
        """Ana ekranı göster"""
        # Ana frame - Modern gradient
        self.frame = ctk.CTkFrame(
            self.parent,
            fg_color=("#F0F8FF", "#0A0E27")
        )
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        # Üst bar
        self.create_top_bar()
        
        # Sol panel - Sürüm listesi
        self.create_version_panel()
        
        # Orta panel - Ana içerik
        self.create_main_panel()
        
        # Sağ panel - Skin önizleme
        self.create_skin_panel()
        
        # Versiyonları yükle
        self.load_versions()
    
    def create_top_bar(self):
        """Üst menü çubuğu"""
        top_bar = ctk.CTkFrame(
            self.frame,
            height=60,
            fg_color=("#00D9FF", "#001F3F"),
            corner_radius=0
        )
        top_bar.pack(fill="x", side="top")
        top_bar.pack_propagate(False)
        
        # Logo
        logo = ctk.CTkLabel(
            top_bar,
            text="TencenT",
            font=("Arial Black", 24, "bold"),
            text_color="#FFFFFF"
        )
        logo.pack(side="left", padx=20)
        
        # Kullanıcı bilgisi
        user_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        user_frame.pack(side="right", padx=20)
        
        user_label = ctk.CTkLabel(
            user_frame,
            text=f"👤 {self.user_data['username']}",
            font=("Arial", 14),
            text_color="#FFFFFF"
        )
        user_label.pack(side="left", padx=10)
        
        # Ayarlar butonu
        settings_btn = ctk.CTkButton(
            user_frame,
            text="⚙️",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=("#00B8DD", "#003366"),
            font=("Arial", 20),
            command=self.open_settings
        )
        settings_btn.pack(side="left")
    
    def create_version_panel(self):
        """Sol panel - Versiyon listesi"""
        left_panel = ctk.CTkFrame(
            self.frame,
            width=250,
            fg_color=("#FFFFFF", "#0F1535"),
            corner_radius=0
        )
        left_panel.pack(fill="y", side="left")
        left_panel.pack_propagate(False)
        
        # Başlık
        title = ctk.CTkLabel(
            left_panel,
            text="Minecraft Sürümleri",
            font=("Arial Bold", 16),
            text_color=("#000000", "#FFFFFF")
        )
        title.pack(pady=20, padx=10)
        
        # Filtre butonları
        filter_frame = ctk.CTkFrame(left_panel, fg_color="transparent")
        filter_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.filter_var = ctk.StringVar(value="all")
        
        filters = [
            ("Tümü", "all"),
            ("Release", "release"),
            ("Snapshot", "snapshot")
        ]
        
        for text, value in filters:
            btn = ctk.CTkRadioButton(
                filter_frame,
                text=text,
                variable=self.filter_var,
                value=value,
                font=("Arial", 12),
                command=self.filter_versions
            )
            btn.pack(anchor="w", padx=5, pady=2)
        
        # Versiyon listesi (scrollable)
        self.version_list_frame = ctk.CTkScrollableFrame(
            left_panel,
            fg_color="transparent"
        )
        self.version_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    def create_main_panel(self):
        """Orta panel - Ana içerik"""
        main_panel = ctk.CTkFrame(
            self.frame,
            fg_color="transparent"
        )
        main_panel.pack(fill="both", expand=True, side="left", padx=20, pady=20)
        
        # Seçili versiyon bilgisi
        self.version_info_frame = ctk.CTkFrame(
            main_panel,
            fg_color=("#FFFFFF", "#1A1F3A"),
            corner_radius=15
        )
        self.version_info_frame.pack(fill="x", pady=(0, 20))
        
        self.version_title = ctk.CTkLabel(
            self.version_info_frame,
            text="Bir sürüm seçin",
            font=("Arial Bold", 28),
            text_color=("#000000", "#FFFFFF")
        )
        self.version_title.pack(pady=20)
        
        self.version_desc = ctk.CTkLabel(
            self.version_info_frame,
            text="Sol panelden oynamak istediğiniz Minecraft sürümünü seçin",
            font=("Arial", 14),
            text_color=("#666666", "#AAAAAA")
        )
        self.version_desc.pack(pady=(0, 20))
        
        # Oyna butonu
        self.play_button = ctk.CTkButton(
            main_panel,
            text="OYNA",
            font=("Arial Black", 32, "bold"),
            height=100,
            fg_color=("#00D9FF", "#00A8CC"),
            hover_color=("#00B8DD", "#008899"),
            corner_radius=15,
            state="disabled",
            command=self.play_game
        )
        self.play_button.pack(fill="x", pady=20)
        
        # İndirme progress (gizli)
        self.download_frame = ctk.CTkFrame(
            main_panel,
            fg_color=("#FFFFFF", "#1A1F3A"),
            corner_radius=15
        )
        
        self.download_label = ctk.CTkLabel(
            self.download_frame,
            text="İndiriliyor...",
            font=("Arial Bold", 16),
            text_color=("#000000", "#FFFFFF")
        )
        self.download_label.pack(pady=10)
        
        self.download_progress = ctk.CTkProgressBar(
            self.download_frame,
            width=400,
            height=20
        )
        self.download_progress.pack(pady=10, padx=20)
        self.download_progress.set(0)
        
        self.download_status = ctk.CTkLabel(
            self.download_frame,
            text="",
            font=("Arial", 12),
            text_color=("#666666", "#AAAAAA")
        )
        self.download_status.pack(pady=(0, 10))
    
    def create_skin_panel(self):
        """Sağ panel - Skin önizleme"""
        right_panel = ctk.CTkFrame(
            self.frame,
            width=200,
            fg_color=("#FFFFFF", "#0F1535"),
            corner_radius=0
        )
        right_panel.pack(fill="y", side="right")
        right_panel.pack_propagate(False)
        
        # Başlık
        title = ctk.CTkLabel(
            right_panel,
            text="Karakteriniz",
            font=("Arial Bold", 16),
            text_color=("#000000", "#FFFFFF")
        )
        title.pack(pady=20)
        
        # Skin önizleme alanı
        skin_preview = ctk.CTkFrame(
            right_panel,
            width=150,
            height=200,
            fg_color=("#E0E0E0", "#1A1F3A"),
            corner_radius=10
        )
        skin_preview.pack(pady=10)
        skin_preview.pack_propagate(False)
        
        # Placeholder
        skin_placeholder = ctk.CTkLabel(
            skin_preview,
            text="👤",
            font=("Arial", 80),
            text_color=("#00D9FF", "#00A8CC")
        )
        skin_placeholder.place(relx=0.5, rely=0.5, anchor="center")
        
        # Kullanıcı adı
        username_label = ctk.CTkLabel(
            right_panel,
            text=self.user_data['username'],
            font=("Arial Bold", 14),
            text_color=("#000000", "#FFFFFF")
        )
        username_label.pack(pady=10)
        
        # Skin değiştir butonu
        change_skin_btn = ctk.CTkButton(
            right_panel,
            text="🎨 Skin Değiştir",
            font=("Arial", 12),
            height=40,
            fg_color=("#00D9FF", "#00A8CC"),
            hover_color=("#00B8DD", "#008899"),
            corner_radius=10,
            command=self.open_skin_market
        )
        change_skin_btn.pack(pady=10, padx=10, fill="x")
        
        # Skin bilgisi
        info = ctk.CTkLabel(
            right_panel,
            text="Binlerce ücretsiz skin\narasından seçim yapın",
            font=("Arial", 10),
            text_color=("#999999", "#666666"),
            justify="center"
        )
        info.pack(pady=10)
    
    def load_versions(self):
        """Minecraft versiyonlarını yükle"""
        def load():
            self.versions = self.version_manager.fetch_versions()
            self.parent.after(0, self.display_versions)
        
        threading.Thread(target=load, daemon=True).start()
    
    def display_versions(self):
        """Versiyonları listele"""
        # Listeyi temizle
        for widget in self.version_list_frame.winfo_children():
            widget.destroy()
        
        # Filtre uygula
        filter_type = self.filter_var.get()
        filtered_versions = self.versions
        
        if filter_type != "all":
            filtered_versions = [v for v in self.versions if v.get('type') == filter_type]
        
        # Versiyonları ekle
        for version in filtered_versions[:50]:  # İlk 50 versiyon
            self.create_version_button(version)
    
    def create_version_button(self, version):
        """Versiyon butonu oluştur"""
        version_id = version.get('id', 'Unknown')
        version_type = version.get('type', 'release')
        
        # Renk seçimi
        if version_type == 'release':
            color = ("#00D9FF", "#00A8CC")
        elif version_type == 'snapshot':
            color = ("#FFA500", "#FF8C00")
        else:
            color = ("#888888", "#666666")
        
        btn = ctk.CTkButton(
            self.version_list_frame,
            text=version_id,
            font=("Arial", 12),
            height=35,
            fg_color=color,
            hover_color=("#00B8DD", "#008899"),
            corner_radius=8,
            command=lambda v=version: self.select_version(v)
        )
        btn.pack(fill="x", pady=3)
    
    def filter_versions(self):
        """Versiyon filtresini uygula"""
        self.display_versions()
    
    def select_version(self, version):
        """Versiyon seç"""
        self.selected_version = version
        version_id = version.get('id', 'Unknown')
        
        # UI güncelle
        self.version_title.configure(text=f"Minecraft {version_id}")
        self.version_desc.configure(
            text=f"Sürüm Tipi: {version.get('type', 'Unknown').title()}"
        )
        
        # Oyna butonunu aktifleştir
        self.play_button.configure(state="normal")
        
        # İndirilmiş mi kontrol et
        if not self.launcher.is_version_installed(version_id):
            self.play_button.configure(text="İNDİR VE OYNA")
        else:
            self.play_button.configure(text="OYNA")
    
    def play_game(self):
        """Oyunu başlat"""
        if not self.selected_version:
            return
        
        version_id = self.selected_version.get('id')
        
        # İndirilmiş mi kontrol et
        if not self.launcher.is_version_installed(version_id):
            self.download_version(version_id)
        else:
            self.launch_game(version_id)
    
    def download_version(self, version_id):
        """Versiyon indir - YENİ SİSTEM"""
        # UI güncelle
        self.play_button.configure(state="disabled")
        self.download_frame.pack(fill="x", pady=20)
        
        def download():
            try:
                from src.core.minecraft_downloader import MinecraftDownloader
                
                # Downloader oluştur
                downloader = MinecraftDownloader(self.launcher.minecraft_dir)
                
                # Progress callback
                def progress(percent, status=""):
                    self.parent.after(0, lambda: self.update_download_progress(percent, status))
                
                # İndir
                success = downloader.download_version(version_id, progress_callback=progress)
                
                if success:
                    # İndirme tamamlandı
                    self.parent.after(0, lambda: self.on_download_complete(version_id))
                else:
                    self.parent.after(0, lambda: self.on_download_error("İndirme başarısız!"))
                
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.parent.after(0, lambda: self.on_download_error(str(e)))
        
        threading.Thread(target=download, daemon=True).start()
    
    def update_download_progress(self, progress, status=""):
        """İndirme ilerlemesini güncelle"""
        self.download_progress.set(progress / 100)
        if status:
            self.download_status.configure(text=status)
        else:
            self.download_status.configure(text=f"İndiriliyor... {progress}%")
    
    def on_download_complete(self, version_id):
        """İndirme tamamlandı"""
        self.download_frame.pack_forget()
        self.play_button.configure(state="normal", text="OYNA")
        
        # Otomatik başlatma mesajı
        response = messagebox.askyesno(
            "İndirme Tamamlandı",
            f"Minecraft {version_id} başarıyla indirildi!\n\nŞimdi oyunu başlatmak ister misiniz?"
        )
        
        if response:
            self.launch_game(version_id)
    
    def on_download_error(self, error):
        """İndirme hatası"""
        self.download_frame.pack_forget()
        self.play_button.configure(state="normal")
        messagebox.showerror("Hata", f"İndirme sırasında hata oluştu:\n{error}")
    
    def launch_game(self, version_id):
        """Oyunu başlat - PORTABLEMC İLE"""
        try:
            from src.core.working_launcher import WorkingLauncher
            
            launcher = WorkingLauncher()
            username = self.user_data['username']
            
            # Mesaj göster
            response = messagebox.askyesno(
                "Minecraft Başlatılıyor",
                f"Minecraft {version_id} başlatılacak.\n\n"
                f"PortableMC kullanılacak (kanıtlanmış çözüm).\n"
                f"İlk çalıştırmada biraz sürebilir.\n\n"
                f"Devam edilsin mi?"
            )
            
            if not response:
                return
            
            # Yeni thread'de başlat
            def launch_thread():
                try:
                    launcher.launch(version_id, username)
                except Exception as e:
                    self.parent.after(0, lambda: messagebox.showerror(
                        "Hata",
                        f"Başlatma hatası:\n{str(e)}"
                    ))
            
            import threading
            thread = threading.Thread(target=launch_thread, daemon=True)
            thread.start()
            
            messagebox.showinfo(
                "Başlatıldı",
                "Minecraft başlatılıyor!\n\n"
                "Console çıktısını launcher penceresinde görebilirsin."
            )
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Hata", f"Hata:\n\n{str(e)}")
    
    def open_skin_market(self):
        """Skin marketini aç"""
        skin_market = SkinMarket(self.parent, self.user_data)
        skin_market.show()
    
    def open_settings(self):
        """Ayarları aç"""
        messagebox.showinfo("Ayarlar", "Ayarlar ekranı yakında eklenecek!")
