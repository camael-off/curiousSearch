import customtkinter as ctk
from tkcalendar import Calendar
from datetime import date
import webbrowser
import urllib.parse
import json
import os

# --- CONFIGURATION DU DESIGN ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Palette de couleurs "Pro"
COLORS = {
    "bg_root": "#0f0f0f",
    "bg_card": "#1a1a1a",
    "header_card": "#252525",
    "border_card": "#333333",
    "accent": "#3498db",
    "danger": "#e74c3c",
    "danger_hover": "#c0392b",
    "success": "#27ae60",
    "text_main": "#ecf0f1",
    "text_dim": "#95a5a6",
    "launch_btn": "#3ca4ff"
}

# Données des continents (Extensions principales)
CONTINENT_TLDS = {
    "Europe": [".fr", ".de", ".uk", ".it", ".es", ".pl", ".nl", ".be", ".se", ".ch", ".at", ".pt", ".gr", ".dk", ".fi", ".no", ".ie", ".cz", ".ro", ".hu", ".ua", ".ru"],
    "North America": [".us", ".ca", ".mx"],
    "South America": [".br", ".ar", ".co", ".cl", ".pe", ".ve", ".uy", ".ec"],
    "Asia": [".cn", ".jp", ".in", ".kr", ".id", ".vn", ".th", ".ph", ".my", ".sg", ".pk", ".bd", ".il", ".ae", ".sa", ".tr", ".hk", ".tw"],
    "Oceania": [".au", ".nz"],
    "Africa": [".za", ".ng", ".eg", ".ke", ".ma", ".dz", ".gh", ".tn", ".sn"]
}

class CuriousSearch(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuration fenêtre
        self.title("CuriousSearch - OSINT Framework")
        self.geometry("1650x1050")
        self.configure(fg_color=COLORS["bg_root"])

        # --- VARIABLES D'ÉTAT ---
        self.current_lang = "EN"
        self.img_mode_var = ctk.BooleanVar(value=False)
        self.open_server_var = ctk.BooleanVar(value=False)
        self.logs_stealer_var = ctk.BooleanVar(value=False)
        self.onion_var = ctk.BooleanVar(value=False)
        self.cloud_var = ctk.BooleanVar(value=False)
        self.config_var = ctk.BooleanVar(value=False)
        
        # Filtre temps actif
        self.active_time_filter = "all" 
        
        self.geo_var = ctk.StringVar(value="All Countries")
        self.kw_list, self.site_list_custom, self.custom_file_list = [], [], []
        self.geo_list_custom = [] 
        self.site_checks_static, self.file_checks, self.nav_checks = [], [], []
        self.continent_checks = [] 
        
        # Sets pour stocker les sélections (Persistance)
        self.selected_sites_include = set()
        self.selected_sites_exclude = set()
        self.selected_continents_include = set() 
        self.selected_continents_exclude = set() 
        
        self.widgets_to_translate = {}
        self.time_checkboxes = []
        self.operator_checkboxes = {} 
        self.profiles_file = "profiles.json"
        self.sites_file = "sites.json"
        self.last_dork = ""

        # Chargement des sites
        self.sites_data = self.load_sites_from_file()
        self.site_categories = ["All"] + list(self.sites_data.keys())

        self.translations = {
            "FR": {
                "title": "curiousSearch", "box1": "MOT CLÉ", "box2": "MOTEURS DE RECHERCHE", "box3": "TYPE DE FICHIER",
                "box4": "DATE & RANG", "box5": "SITE", "box6": "FILTRES EXPERTS", "box7": "MÉTIER", "box8": "ACTIONS",
                "before": "Avant le :", "after": "Après le :",
                "select_all": "Tout sélectionner", "custom_ext": "Extensions personnalisées :",
                "custom_site": "Sites personnalisés :", "popular_site": "Plateformes populaires :",
                "img_mode": "Mode Google Images", "open_server": "Serveurs ouverts (Index of)",
                "logs_stealer": "Logs stealer(Login/MDP)", "dork_ops": "Opérateurs :",
                "exact": "Expression exacte (\" \")", "intext": "Dans le corps (intext:)", "intitle": "Dans le titre (intitle:)",
                "img_filters": "Filtres Images :", "time_filters": "Filtres Temporels :", "verbatim": "Verbatim (Mot à mot)",
                "sort_date": "Trier par date", "period": "Période :", "launch": "START",
                "kw_placeholder": "mot clé (ou URL image)", "site_placeholder": "site (ex: fb.com)", "ext_placeholder": "ext (ex: pdf)",
                "geo_placeholder": "ex: .fr", 
                "geo_custom_label": "Zone / Pays (.fr, .be) :",
                "continents_label": "Continents / Régions :",
                "inurl": "URL (inurl:)", "inanchor": "Liens (inanchor:)", "related": "Similaires (related:)",
                "archive": "Archive (Wayback Machine)", "range_val": "Activer Intervalle",
                "donate": "Soutenir le projet ☕", "profiles": "Profiles", "save_profile": "Sauvegarder",
                "load_profile": "Charger profil...", "copy": "Copier la Dork", "geo_label": "Ciblage Pays :",
                "rev_tools": "Recherche Inversée :", "rev_placeholder": "Coller l'URL de l'image ici...",
                "onion_mode": "Ciblage Onion (Darknet Lite)", "cloud_mode": "S3 Buckets & Clouds", "config_mode": "Fichiers Config (.env, keys)",
                "times": ["Tout le temps", "Dernière heure", "24h", "Semaine", "Mois", "Année"]
            },
            "EN": {
                "title": "curiousSearch", "box1": "KEYWORD", "box2": "SEARCH ENGINES", "box3": "FILE TYPE",
                "box4": "DATE & RANGE", "box5": "SITE", "box6": "EXPERT FILTERS", "box7": "METIER", "box8": "ACTIONS",
                "before": "Before:", "after": "After:", "select_all": "Select all",
                "custom_ext": "Custom extensions:", "custom_site": "Custom sites:",
                "popular_site": "Popular platforms:", "img_mode": "Google Images mode",
                "open_server": "Open servers (Index of)", "logs_stealer": "Logs stealer (Pass/Login)",
                "dork_ops": "Operators:", "exact": "Exact match (\" \")", "intext": "In body (intext:)",
                "intitle": "In title (intitle:)", "img_filters": "Image Filters:",
                "time_filters": "Time Filters:", "verbatim": "Verbatim (Exact word)",
                "sort_date": "Sort by date", "period": "Period:", "launch": "START",
                "kw_placeholder": "keyword (or image URL)", "site_placeholder": "site (ex: fb.com)", "ext_placeholder": "ext (ex: pdf)",
                "geo_placeholder": "ex: .fr",
                "geo_custom_label": "Zone / Country (.fr, .uk) :",
                "continents_label": "Continents / Regions :",
                "inurl": "In URL (inurl:)", "inanchor": "In Links (inanchor:)", "related": "Similar (related:)",
                "archive": "Archive (Wayback Machine)", "range_val": "Enable Interval",
                "donate": "Support the project ☕", "profiles": "Profiles", "save_profile": "Save",
                "load_profile": "Load profile...", "copy": "Copy Dork", "geo_label": "Country Target:",
                "rev_tools": "Reverse Search:", "rev_placeholder": "Paste Image URL here...",
                "onion_mode": "Onion Targeting (Darknet Lite)", "cloud_mode": "S3 Buckets & Clouds", "config_mode": "Config Files (.env, keys)",
                "times": ["All time", "Last hour", "24h", "Week", "Month", "Year"]
            }
        }

        h_cont = ctk.CTkFrame(self, fg_color="transparent")
        h_cont.pack(fill="x", pady=(20, 10), padx=30)
        self.main_title = ctk.CTkLabel(h_cont, text="curiousSearch", font=("Arial", 36, "bold"), text_color=COLORS["text_main"])
        self.main_title.pack(anchor="center")
        
        self.p_frame = ctk.CTkFrame(self, height=50, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border_card"])
        self.p_frame.pack(fill="x", padx=25, pady=5)
        
        left_zone = ctk.CTkFrame(self.p_frame, fg_color="transparent")
        left_zone.pack(side="left", padx=15, pady=8)
        
        self.lbl_profiles = ctk.CTkLabel(left_zone, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_profiles.pack(side="left", padx=(0, 10))
        self.widgets_to_translate["profiles"] = self.lbl_profiles
        
        self.profile_menu = ctk.CTkOptionMenu(left_zone, values=[self.translations["EN"]["load_profile"]], command=self.load_profile_data, 
                                              fg_color=COLORS["header_card"], button_color=COLORS["border_card"], button_hover_color=COLORS["accent"], width=180)
        self.profile_menu.pack(side="left", padx=5)
        
        self.btn_save_p = ctk.CTkButton(left_zone, text="", width=100, fg_color=COLORS["success"], hover_color="#2ecc71", font=("Segoe UI", 12, "bold"), command=self.save_profile_popup)
        self.btn_save_p.pack(side="left", padx=5)
        self.widgets_to_translate["save_profile"] = self.btn_save_p

        self.lang_container = ctk.CTkFrame(self.p_frame, fg_color="transparent")
        self.lang_container.pack(side="right", padx=15)
        for lang in ["FR", "EN"]:
            target = "EN" if lang == "EN" else "FR"
            btn = ctk.CTkButton(self.lang_container, text=lang, width=40, height=28, font=("Segoe UI", 11, "bold"), 
                                fg_color=COLORS["header_card"], hover_color=COLORS["accent"], 
                                command=lambda l=target: self.change_language(l))
            btn.pack(side="left", padx=3)

        grid = ctk.CTkFrame(self, fg_color="transparent")
        grid.pack(padx=20, pady=15, fill="both", expand=True)
        grid.columnconfigure((0, 1, 2, 3), weight=1, uniform="col")
        grid.rowconfigure((0, 1), weight=1, uniform="row")

        # 1. MOT CLÉ
        self.box_keywords = self.create_box(grid, 0, 0, "box1")
        self.add_column_headers(self.box_keywords)
        self.kw_scroll = ctk.CTkScrollableFrame(self.box_keywords, fg_color="transparent")
        self.kw_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.frame_custom_kw = ctk.CTkFrame(self.kw_scroll, fg_color="transparent")
        self.frame_custom_kw.pack(fill="x")
        self.add_keyword_field()
        ctk.CTkButton(self.kw_scroll, text="+", width=30, height=24, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=self.add_keyword_field).pack(pady=5)
        self.kw_check_all = self.create_simple_footer(self.box_keywords, self.toggle_keywords, self.reset_keywords)

        # 2. MOTEURS
        self.box_nav = self.create_box(grid, 0, 1, "box2")
        self.nav_scroll = ctk.CTkScrollableFrame(self.box_nav, fg_color="transparent")
        self.nav_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        for n in ["Google", "Bing", "Yandex", "DuckDuckGo", "Yahoo"]:
            cb = ctk.CTkCheckBox(self.nav_scroll, text=n, border_color=COLORS["border_card"], hover_color=COLORS["accent"], fg_color=COLORS["accent"])
            cb.pack(anchor="w", padx=10, pady=8)
            if n == "Google": cb.select()
            self.nav_checks.append(cb)
        self.check_all_nav = self.create_simple_footer(self.box_nav, self.toggle_navs, self.reset_navs)

        # 3. FICHIERS
        self.box_files = self.create_box(grid, 0, 2, "box3")
        self.add_column_headers(self.box_files)
        self.file_scroll = ctk.CTkScrollableFrame(self.box_files, fg_color="transparent")
        self.file_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        self.lbl_custom_ext = ctk.CTkLabel(self.file_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_custom_ext.pack(anchor="w", padx=5)
        self.widgets_to_translate["custom_ext"] = self.lbl_custom_ext
        self.frame_custom_files = ctk.CTkFrame(self.file_scroll, fg_color="transparent")
        self.frame_custom_files.pack(fill="x")
        self.add_custom_file_field()
        ctk.CTkButton(self.file_scroll, text="+", width=30, height=24, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=self.add_custom_file_field).pack(pady=5)
        ctk.CTkFrame(self.file_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=8)
        for ft in ["pdf", "doc", "docx", "xls", "xlsx", "csv", "txt", "log", "sql", "env", "xml", "json", "py", "php", "ppt", "pptx"]:
            cb = ctk.CTkCheckBox(self.file_scroll, text=ft, border_color=COLORS["border_card"], hover_color=COLORS["accent"], fg_color=COLORS["accent"])
            cb.pack(anchor="w", padx=10, pady=2)
            self.file_checks.append(cb)
        self.file_check_all = self.create_simple_footer(self.box_files, self.toggle_files, self.reset_files)

        # 4. METIER
        self.box_metier = self.create_box(grid, 0, 3, "box7")
        self.metier_scroll = ctk.CTkScrollableFrame(self.box_metier, fg_color="transparent")
        self.metier_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.switch_img = ctk.CTkSwitch(self.metier_scroll, text="", variable=self.img_mode_var, font=("Segoe UI", 12, "bold"), command=self.toggle_img_filters, progress_color=COLORS["accent"])
        self.switch_img.pack(pady=8, anchor="w", padx=10)
        self.widgets_to_translate["img_mode"] = self.switch_img

        self.img_filter_container = ctk.CTkFrame(self.metier_scroll, fg_color="transparent")
        self.lbl_img_f = ctk.CTkLabel(self.img_filter_container, text="", font=("Segoe UI", 11, "bold"), text_color=COLORS["text_dim"])
        self.lbl_img_f.pack(anchor="w", padx=5)
        self.widgets_to_translate["img_filters"] = self.lbl_img_f
        
        for opt in ["type", "color", "size", "res", "rights"]:
            om = ctk.CTkOptionMenu(self.img_filter_container, values=[], height=24, fg_color=COLORS["header_card"], button_color=COLORS["border_card"], width=180)
            om.pack(pady=2, padx=15, anchor="w")
            setattr(self, f"opt_img_{opt}", om)
        
        self.opt_img_type.configure(values=["(Type: None)", "Clipart", "Lineart", "GIF", "Face"])
        self.opt_img_color.configure(values=["(Color: Any)", "Full Color", "B&W", "Transp.", "Red", "Green", "Blue"])
        self.opt_img_size.configure(values=["(Size: Any)", "Icon", "Medium", "Large"])
        self.opt_img_res.configure(values=["(Res: Any)", "> VGA", "> 2MP", "> 8MP"])
        self.opt_img_rights.configure(values=["(Rights: Any)", "Commercial", "Creative Commons"])

        ctk.CTkFrame(self.img_filter_container, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=10)
        self.lbl_rev = ctk.CTkLabel(self.img_filter_container, text="", font=("Segoe UI", 11, "bold"), text_color=COLORS["accent"])
        self.lbl_rev.pack(anchor="w", padx=5)
        self.widgets_to_translate["rev_tools"] = self.lbl_rev
        self.ent_rev_url = ctk.CTkEntry(self.img_filter_container, placeholder_text="", height=28, border_color=COLORS["border_card"], fg_color=COLORS["header_card"])
        self.ent_rev_url.pack(fill="x", padx=5, pady=(0, 5))
        
        for name, cmd in [("Yandex", "yandex"), ("TinEye", "tineye"), ("Bing Visual", "bing"), ("PimEyes", "pimeyes")]:
            if name in ["Yandex", "Bing Visual"]: f = ctk.CTkFrame(self.img_filter_container, fg_color="transparent"); f.pack(fill="x", pady=1)
            btn = ctk.CTkButton(f, text=name, width=80, height=24, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=lambda c=cmd: self.run_reverse(c))
            btn.pack(side="left", padx=2, expand=True, fill="x")
        ctk.CTkFrame(self.img_filter_container, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=10)

        for txt, var, col in [(None, self.open_server_var, "#e67e22"), (None, self.logs_stealer_var, "#9b59b6")]:
            s = ctk.CTkSwitch(self.metier_scroll, text="", variable=var, font=("Segoe UI", 12, "bold"), progress_color=col)
            s.pack(pady=8, anchor="w", padx=10)
            if col == "#e67e22": self.switch_server = s; self.widgets_to_translate["open_server"] = s
            else: self.switch_logs = s; self.widgets_to_translate["logs_stealer"] = s
        
        ctk.CTkFrame(self.metier_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=10)
        for txt, var, col in [(None, self.onion_var, "#8e44ad"), (None, self.cloud_var, "#2980b9"), (None, self.config_var, "#c0392b")]:
            s = ctk.CTkSwitch(self.metier_scroll, text="", variable=var, font=("Segoe UI", 12, "bold"), progress_color=col)
            s.pack(pady=8, anchor="w", padx=10)
            if col == "#8e44ad": self.switch_onion = s; self.widgets_to_translate["onion_mode"] = s
            elif col == "#2980b9": self.switch_cloud = s; self.widgets_to_translate["cloud_mode"] = s
            else: self.switch_config = s; self.widgets_to_translate["config_mode"] = s

        # 5. DATE & RANG
        self.box_date = self.create_box(grid, 1, 0, "box4")
        self.date_scroll = ctk.CTkScrollableFrame(self.box_date, fg_color="transparent")
        self.date_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Section 1: Checkboxes temps
        self.radio_time_frame = ctk.CTkFrame(self.date_scroll, fg_color="transparent")
        self.radio_time_frame.pack(fill="x", pady=(0, 15))
        
        time_values = ["all", "h", "d", "w", "m", "y"]
        for i in range(6):
            r_val = time_values[i]
            cb = ctk.CTkCheckBox(self.radio_time_frame, text="", 
                                 command=lambda v=r_val: self.handle_time_check(v), 
                                 border_color=COLORS["border_card"], 
                                 hover_color=COLORS["accent"], fg_color=COLORS["accent"])
            row = i // 2; col = i % 2
            cb.grid(row=row, column=col, sticky="w", padx=20, pady=5)
            if r_val == "all": cb.select()
            self.time_checkboxes.append((cb, r_val))

        ctk.CTkFrame(self.date_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=5)

        for attr in ["before", "after"]:
            f = ctk.CTkFrame(self.date_scroll, fg_color="transparent")
            f.pack(pady=2)
            cb = ctk.CTkCheckBox(f, text="", width=70, border_color=COLORS["border_card"], hover_color=COLORS["accent"], fg_color=COLORS["accent"], command=self.sync_date_logic)
            cb.pack(side="left")
            ent = ctk.CTkEntry(f, width=110, placeholder_text="YYYY-MM-DD", border_color=COLORS["border_card"], fg_color=COLORS["header_card"])
            ent.pack(side="left", padx=5)
            btn = ctk.CTkButton(f, text="📅", width=30, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=lambda e=ent: self.open_calendar_popup(e))
            btn.pack(side="left")
            setattr(self, f"cb_{attr}", cb); setattr(self, f"ent_{attr}_date", ent); setattr(self, f"btn_cal_{attr}", btn)
            self.widgets_to_translate[attr] = cb
            
        ctk.CTkFrame(self.date_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=15)
        
        self.interval_frame = ctk.CTkFrame(self.date_scroll, fg_color="transparent")
        self.interval_frame.pack(fill="x", padx=5)
        self.cb_interval = ctk.CTkCheckBox(self.interval_frame, text="", font=("Segoe UI", 12, "bold"), 
                                           border_color=COLORS["border_card"], hover_color=COLORS["accent"], 
                                           fg_color=COLORS["accent"], command=self.sync_date_logic)
        self.cb_interval.pack(side="left")
        self.widgets_to_translate["range_val"] = self.cb_interval 
        self.ent_range = ctk.CTkEntry(self.date_scroll, placeholder_text="2000..2025", border_color=COLORS["border_card"], fg_color=COLORS["header_card"])
        self.ent_range.pack(fill="x", padx=10, pady=5)
        
        # 6. SITE (AVEC CATÉGORIES)
        self.box_site = self.create_box(grid, 1, 1, "box5")
        
        self.cat_seg = ctk.CTkSegmentedButton(self.box_site, values=self.site_categories, command=self.update_site_list_display,
                                              fg_color=COLORS["header_card"], selected_color=COLORS["accent"],
                                              selected_hover_color="#2980b9", unselected_color=COLORS["bg_card"],
                                              unselected_hover_color=COLORS["border_card"])
        self.cat_seg.set("All")
        self.cat_seg.pack(fill="x", padx=10, pady=(5,0))

        self.add_column_headers(self.box_site)
        self.site_scroll = ctk.CTkScrollableFrame(self.box_site, fg_color="transparent")
        self.site_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.lbl_custom_site = ctk.CTkLabel(self.site_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_custom_site.pack(anchor="w", padx=5)
        self.widgets_to_translate["custom_site"] = self.lbl_custom_site
        self.frame_custom_sites = ctk.CTkFrame(self.site_scroll, fg_color="transparent")
        self.frame_custom_sites.pack(fill="x")
        self.add_site_field()
        ctk.CTkButton(self.site_scroll, text="+", width=30, height=24, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=self.add_site_field).pack(pady=5)
        ctk.CTkFrame(self.site_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=8)
        
        self.lbl_pop_site = ctk.CTkLabel(self.site_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_pop_site.pack(anchor="w", padx=5)
        self.widgets_to_translate["popular_site"] = self.lbl_pop_site
        
        self.frame_static_sites = ctk.CTkFrame(self.site_scroll, fg_color="transparent")
        self.frame_static_sites.pack(fill="x")
        
        self.update_site_list_display("All")
            
        self.check_all_sites = self.create_simple_footer(self.box_site, self.toggle_sites, self.reset_sites)

        # 7. FILTRES EXPERTS (REORGANISÉ)
        self.box_opt = self.create_box(grid, 1, 2, "box6")
        self.opt_scroll = ctk.CTkScrollableFrame(self.box_opt, fg_color="transparent")
        self.opt_scroll.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 1. DORK OPS (EN PREMIER)
        self.lbl_std = ctk.CTkLabel(self.opt_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_std.pack(anchor="w", padx=5)
        self.widgets_to_translate["dork_ops"] = self.lbl_std
        
        # Groupe Mutuellement Exclusif (Location) + Indépendants
        for name, key in [("Exact match (\" \")", "exact"), 
                          ("In body (intext:)", "intext"),
                          ("In title (intitle:)", "intitle"),
                          ("In URL (inurl:)", "inurl"),
                          ("In Links (inanchor:)", "inanchor"),
                          ("Similar (related:)", "related"),
                          ("Archive (Wayback Machine)", "archive")]:
            
            cb = ctk.CTkCheckBox(self.opt_scroll, text=name, border_color=COLORS["border_card"], hover_color=COLORS["accent"], fg_color=COLORS["accent"])
            
            # Application de la logique d'exclusivité pour le groupe de localisation
            if key in ["intext", "intitle", "inurl", "inanchor", "related"]:
                cb.configure(command=lambda k=key: self.handle_exclusive_operator(k))
                self.operator_checkboxes[key] = cb
                
            cb.pack(pady=2, anchor="w", padx=15)
            setattr(self, f"{key}_m", cb) # self.intext_m, self.exact_m, etc.
            
        ctk.CTkFrame(self.opt_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=10)
        
        # 2. CONTINENTS
        self.lbl_cont = ctk.CTkLabel(self.opt_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_cont.pack(anchor="w", padx=5)
        self.widgets_to_translate["continents_label"] = self.lbl_cont
        self.add_column_headers(self.opt_scroll) 
        self.frame_continents = ctk.CTkFrame(self.opt_scroll, fg_color="transparent")
        self.frame_continents.pack(fill="x")
        for cont_name in CONTINENT_TLDS.keys():
            self.add_continent_row(cont_name)
            
        ctk.CTkFrame(self.opt_scroll, height=1, fg_color=COLORS["border_card"]).pack(fill="x", pady=10)
        
        # 3. COUNTRY ZONE
        self.lbl_custom_geo = ctk.CTkLabel(self.opt_scroll, text="", font=("Segoe UI", 12, "bold"), text_color=COLORS["text_dim"])
        self.lbl_custom_geo.pack(anchor="w", padx=5)
        self.widgets_to_translate["geo_custom_label"] = self.lbl_custom_geo
        self.frame_custom_geo = ctk.CTkFrame(self.opt_scroll, fg_color="transparent")
        self.frame_custom_geo.pack(fill="x")
        self.add_geo_field()
        ctk.CTkButton(self.opt_scroll, text="+", width=30, height=24, fg_color=COLORS["border_card"], hover_color=COLORS["accent"], command=self.add_geo_field).pack(pady=5)

        # 8. ACTIONS
        self.box_action = self.create_box(grid, 1, 3, "box8")
        self.btn_frame = ctk.CTkFrame(self.box_action, fg_color="transparent")
        self.btn_frame.pack(fill="both", expand=True, padx=25, pady=(30, 0))
        self.search_btn = ctk.CTkButton(self.btn_frame, text="", font=("Segoe UI", 18, "bold"), height=55, 
                                        fg_color=COLORS["launch_btn"], hover_color=COLORS["accent"], 
                                        corner_radius=8, command=self.run_investigation)
        self.search_btn.pack(fill="x", pady=(0, 15)); self.widgets_to_translate["launch"] = self.search_btn
        self.copy_btn = ctk.CTkButton(self.btn_frame, text="", font=("Segoe UI", 12, "bold"), height=40, 
                                      fg_color=COLORS["border_card"], hover_color=COLORS["accent"], 
                                      corner_radius=8, command=self.copy_to_clipboard)
        self.copy_btn.pack(fill="x"); self.widgets_to_translate["copy"] = self.copy_btn
        self.footer_action = ctk.CTkFrame(self.box_action, fg_color="transparent", height=40)
        self.footer_action.pack(side="bottom", fill="x", padx=15, pady=15)
        self.btn_donate_final = ctk.CTkButton(self.footer_action, text="", font=("Segoe UI", 11, "bold"), 
                                              fg_color="#e67e22", hover_color="#d35400", height=32, width=130, 
                                              corner_radius=20, command=self.open_donate)
        self.btn_donate_final.pack(side="left"); self.widgets_to_translate["donate"] = self.btn_donate_final
        self.lbl_author = ctk.CTkLabel(self.footer_action, text="by Camael", font=("Segoe UI", 12), text_color=COLORS["text_dim"])
        self.lbl_author.pack(side="right", padx=5)

        # BINDINGS
        self.bind("<Return>", lambda e: self.run_investigation())
        self.bind("<Control-c>", lambda e: self.copy_to_clipboard())
        self.bind("<Control-C>", lambda e: self.copy_to_clipboard())

        self.change_language("EN"); self.toggle_img_filters(); self.refresh_profile_list(); self.sync_date_logic()

    # --- LOGIQUE EXCLUSIVITÉ OPERATORS ---
    def handle_exclusive_operator(self, active_key):
        if getattr(self, f"{active_key}_m").get() == 1:
            for key, widget in self.operator_checkboxes.items():
                if key != active_key: widget.deselect()

    # --- POPUPS & EXTERNAL LINKS ---
    def save_profile_popup(self):
        p = ctk.CTkToplevel(self)
        p.title("Save")
        p.geometry("300x150")
        p.grab_set()
        ctk.CTkLabel(p, text="Preset Name:").pack(pady=10)
        e = ctk.CTkEntry(p, width=200)
        e.pack(pady=5)
        e.focus()
        ctk.CTkButton(p, text="Save", command=lambda: [self.save_current_as_profile(e.get()), p.destroy()]).pack(pady=10)

    def open_donate(self):
        webbrowser.open("https://buymeacoffee.com/camael")

    def open_calendar_popup(self, e):
        t = ctk.CTkToplevel(self); t.grab_set(); t.attributes("-topmost", True)
        cal = Calendar(t, selectmode='day', date_pattern='yyyy-mm-dd'); cal.pack(pady=10)
        def s(): e.delete(0, "end"); e.insert(0, cal.get_date()); t.destroy()
        ctk.CTkButton(t, text="OK", command=s).pack(pady=5)

    def run_reverse(self, tool):
        url_kw = self.ent_rev_url.get().strip()
        if not url_kw and self.kw_list:
            val = self.kw_list[0][0].get().strip()
            if val.startswith("http"): url_kw = val
        encoded_url = urllib.parse.quote(url_kw) if url_kw else ""; target = ""
        if tool == "yandex": target = f"https://yandex.com/images/search?rpt=imageview&url={encoded_url}" if url_kw else "https://yandex.com/images/"
        elif tool == "tineye": target = f"https://tineye.com/search?url={encoded_url}" if url_kw else "https://tineye.com/"
        elif tool == "bing": target = f"https://www.bing.com/images/search?view=detailv2&iss=sbi&form=SBIHMP&sbisrc=UrlPaste&q=imgurl:{encoded_url}" if url_kw else "https://www.bing.com/visualsearch"
        elif tool == "pimeyes": target = "https://pimeyes.com/"
        webbrowser.open(target)

    # --- MÉTHODE DE CHARGEMENT DES SITES ---
    def load_sites_from_file(self):
        default_sites = {
            "Social": ["linkedin.com", "facebook.com", "twitter.com", "instagram.com", "reddit.com", "tiktok.com"],
            "Tech": ["github.com", "stackoverflow.com", "pastebin.com", "gitlab.com"],
            "Cloud/Docs": ["s3.amazonaws.com", "trello.com", "docs.google.com", "notion.so"]
        }
        if not os.path.exists(self.sites_file):
            try:
                with open(self.sites_file, "w") as f: json.dump(default_sites, f, indent=4)
            except: pass
            return default_sites
        else:
            try:
                with open(self.sites_file, "r") as f:
                    data = json.load(f)
                    if isinstance(data, list): return {"General": data}
                    return data
            except:
                return default_sites

    # --- HELPERS DESIGN ---
    def create_box(self, p, r, c, k):
        f = ctk.CTkFrame(p, fg_color=COLORS["bg_card"], corner_radius=10, border_width=1, border_color=COLORS["border_card"])
        f.grid(row=r, column=c, sticky="nsew", padx=10, pady=10)
        h = ctk.CTkFrame(f, fg_color=COLORS["header_card"], corner_radius=10, height=40)
        h.pack(fill="x", side="top", padx=1, pady=1) 
        ctk.CTkLabel(h, text="", font=("Segoe UI", 13, "bold"), text_color=COLORS["text_main"]).pack(pady=8)
        return f

    def create_simple_footer(self, p, t, r):
        f = ctk.CTkFrame(p, fg_color="transparent", height=45)
        f.pack(fill="x", side="bottom")
        container = ctk.CTkFrame(f, fg_color="transparent")
        container.pack(anchor="center")
        chk = ctk.CTkCheckBox(container, text="select all", text_color=COLORS["accent"], 
                              border_color=COLORS["border_card"], hover_color=COLORS["accent"], fg_color=COLORS["accent"],
                              font=("Segoe UI", 11), command=t)
        chk.pack(side="left", padx=(0, 10))
        btn = ctk.CTkButton(container, text="Reset", width=60, height=22, 
                            fg_color=COLORS["border_card"], hover_color=COLORS["danger"], text_color=COLORS["text_main"],
                            font=("Segoe UI", 10, "bold"), command=r)
        btn.pack(side="left")
        return chk

    def add_column_headers(self, p):
        h = ctk.CTkFrame(p, fg_color="transparent", height=30)
        h.pack(fill="x", padx=10, pady=(5,0))
        ctk.CTkLabel(h, text="INCLUDE", width=60, font=("Segoe UI", 10, "bold"), text_color=COLORS["success"]).pack(side="left", padx=2)
        ctk.CTkLabel(h, text="EXCLUDE", width=60, font=("Segoe UI", 10, "bold"), text_color=COLORS["danger"]).pack(side="left", padx=2)
        ctk.CTkLabel(h, text="").pack(side="left", fill="x", expand=True)

    def create_toggle_btn(self, p, t):
        color = COLORS["success"] if t == "in" else COLORS["danger"]
        b = ctk.CTkButton(p, text="", width=22, height=22, fg_color=COLORS["border_card"], hover_color=color, corner_radius=6)
        b.is_checked = False; b.btn_type = t
        return b

    def toggle_selection(self, c, o):
        active_color = COLORS["success"] if c.btn_type=="in" else COLORS["danger"]
        if c.is_checked: 
            c.configure(fg_color=COLORS["border_card"], text=""); c.is_checked = False
        else:
            c.configure(fg_color=active_color, text="✓", font=("Segoe UI", 12, "bold"))
            c.is_checked = True
            o.configure(fg_color=COLORS["border_card"], text=""); o.is_checked = False

    def auto_check_smart(self, en, bi, bo):
        if len(en.get()) > 0:
            if not bo.is_checked and not bi.is_checked:
                bi.configure(fg_color=COLORS["success"], text="✓", font=("Segoe UI", 12, "bold")); bi.is_checked = True
        else:
            for b in [bi, bo]: b.configure(fg_color=COLORS["border_card"], text=""); b.is_checked = False

    def add_dynamic_row(self, p_f, l_s, pk):
        r = ctk.CTkFrame(p_f, fg_color="transparent"); r.pack(fill="x", pady=2)
        bi, bo = self.create_toggle_btn(r, "in"), self.create_toggle_btn(r, "out")
        bi.pack(side="left", padx=15); bo.pack(side="left", padx=25) 
        bi.configure(command=lambda b1=bi, b2=bo: self.toggle_selection(b1, b2))
        bo.configure(command=lambda b1=bo, b2=bi: self.toggle_selection(b1, b2))
        btn_del = ctk.CTkButton(r, text="×", width=24, height=24, fg_color="transparent", hover_color=COLORS["danger"], text_color=COLORS["text_dim"], command=lambda: self.remove_dynamic_row(d, l_s))
        btn_del.pack(side="right", padx=5)
        ent = ctk.CTkEntry(r, placeholder_text=self.translations[self.current_lang][pk], border_color=COLORS["border_card"], fg_color=COLORS["bg_root"])
        ent.pack(side="left", padx=5, fill="x", expand=True)
        ent.bind("<KeyRelease>", lambda e, b1=bi, b2=bo, en=ent: self.auto_check_smart(en, b1, b2))
        d = (ent, bi, bo, r); l_s.append(d)

    def update_site_list_display(self, category):
        for widget in self.frame_static_sites.winfo_children(): widget.destroy()
        self.site_checks_static.clear()
        sites_to_show = []
        if category == "All":
            for cat_sites in self.sites_data.values(): sites_to_show.extend(cat_sites)
            sites_to_show = sorted(list(set(sites_to_show)))
        else:
            sites_to_show = self.sites_data.get(category, [])
        for s in sites_to_show: self.add_static_site_row(s)

    def add_static_site_row(self, s):
        r = ctk.CTkFrame(self.frame_static_sites, fg_color="transparent"); r.pack(fill="x", pady=1)
        bi, bo = self.create_toggle_btn(r, "in"), self.create_toggle_btn(r, "out")
        bi.pack(side="left", padx=15); bo.pack(side="left", padx=25)
        bi.configure(command=lambda b1=bi, b2=bo, site=s: self.toggle_site_persistent(b1, b2, site, "in"))
        bo.configure(command=lambda b1=bo, b2=bi, site=s: self.toggle_site_persistent(b1, b2, site, "out"))
        ctk.CTkLabel(r, text=s, font=("Segoe UI", 12)).pack(side="left", padx=10)
        if s in self.selected_sites_include: bi.configure(fg_color=COLORS["success"], text="✓", font=("Segoe UI", 12, "bold")); bi.is_checked = True
        if s in self.selected_sites_exclude: bo.configure(fg_color=COLORS["danger"], text="✓", font=("Segoe UI", 12, "bold")); bo.is_checked = True
        self.site_checks_static.append((bi, bo, s))

    def toggle_site_persistent(self, c, o, site, mode):
        self.toggle_selection(c, o)
        if c.is_checked:
            if mode == "in": self.selected_sites_include.add(site); self.selected_sites_exclude.discard(site)
            else: self.selected_sites_exclude.add(site); self.selected_sites_include.discard(site)
        else:
            if mode == "in": self.selected_sites_include.discard(site)
            else: self.selected_sites_exclude.discard(site)

    def add_continent_row(self, s):
        r = ctk.CTkFrame(self.frame_continents, fg_color="transparent"); r.pack(fill="x", pady=1)
        bi, bo = self.create_toggle_btn(r, "in"), self.create_toggle_btn(r, "out")
        bi.pack(side="left", padx=15); bo.pack(side="left", padx=25)
        bi.configure(command=lambda b1=bi, b2=bo, c=s: self.toggle_continent_persistent(b1, b2, c, "in"))
        bo.configure(command=lambda b1=bo, b2=bi, c=s: self.toggle_continent_persistent(b1, b2, c, "out"))
        ctk.CTkLabel(r, text=s, font=("Segoe UI", 12)).pack(side="left", padx=10)
        self.continent_checks.append((bi, bo, s))

    def toggle_continent_persistent(self, c, o, cont, mode):
        self.toggle_selection(c, o)
        if c.is_checked:
            if mode == "in": self.selected_continents_include.add(cont); self.selected_continents_exclude.discard(cont)
            else: self.selected_continents_exclude.add(cont); self.selected_continents_include.discard(cont)
        else:
            if mode == "in": self.selected_continents_include.discard(cont)
            else: self.selected_continents_exclude.discard(cont)

    # --- LOGIQUE MÉTIER ---
    def remove_dynamic_row(self, d, l): d[3].destroy(); l.remove(d)
    def add_keyword_field(self): self.add_dynamic_row(self.frame_custom_kw if hasattr(self, 'frame_custom_kw') else self.kw_scroll, self.kw_list, "kw_placeholder")
    def add_site_field(self): self.add_dynamic_row(self.frame_custom_sites, self.site_list_custom, "site_placeholder")
    def add_custom_file_field(self): self.add_dynamic_row(self.frame_custom_files, self.custom_file_list, "ext_placeholder")
    def add_geo_field(self): self.add_dynamic_row(self.frame_custom_geo, self.geo_list_custom, "geo_placeholder")

    def handle_time_check(self, value):
        if self.active_time_filter == value: self.active_time_filter = None
        else: self.active_time_filter = value
        for cb, val in self.time_checkboxes:
            if val == self.active_time_filter: cb.select()
            else: cb.deselect()
        self.sync_date_logic()

    def sync_date_logic(self):
        has_preset = (self.active_time_filter is not None)
        
        for a in ["before", "after"]:
            if hasattr(self, f"cb_{a}"):
                getattr(self, f"cb_{a}").configure(state="normal" if not has_preset else "disabled")
                is_active = (not has_preset) and getattr(self, f"cb_{a}").get()
                getattr(self, f"ent_{a}_date").configure(state="normal" if is_active else "disabled")
                getattr(self, f"btn_cal_{a}").configure(state="normal" if is_active else "disabled")

        if hasattr(self, "cb_interval"):
            if has_preset:
                self.cb_interval.configure(state="disabled")
                self.ent_range.configure(state="disabled")
            else:
                is_ba_active = False
                for a in ["before", "after"]:
                    if hasattr(self, f"cb_{a}") and getattr(self, f"cb_{a}").get():
                        is_ba_active = True
                        break
                
                if is_ba_active:
                    self.cb_interval.configure(state="disabled")
                    self.ent_range.configure(state="disabled")
                else:
                    self.cb_interval.configure(state="normal")
                    self.ent_range.configure(state="normal" if self.cb_interval.get() else "disabled")

        is_custom_active = False
        if not has_preset:
            if hasattr(self, "cb_interval") and self.cb_interval.get(): is_custom_active = True
            for a in ["before", "after"]:
                if hasattr(self, f"cb_{a}") and getattr(self, f"cb_{a}").get(): is_custom_active = True
        
        for cb, _ in self.time_checkboxes:
            if is_custom_active: cb.configure(state="disabled")
            else: cb.configure(state="normal")
            
        if has_preset:
            for cb, _ in self.time_checkboxes: cb.configure(state="normal")

    def toggle_keywords(self):
        s = self.kw_check_all.get()
        for row in self.kw_list:
            v = s and len(row[0].get())>0 and not row[2].is_checked
            active_col = COLORS["success"]
            row[1].configure(fg_color=active_col if v else COLORS["border_card"], text="✓" if v else ""); row[1].is_checked = v

    def toggle_navs(self):
        s = self.check_all_nav.get()
        for cb in self.nav_checks:
            if cb.cget("state") == "normal": cb.select() if s else cb.deselect()

    def toggle_files(self):
        s = self.file_check_all.get()
        for cb in self.file_checks: cb.select() if s else cb.deselect()
        for row in self.custom_file_list:
            v = s and len(row[0].get())>0 and not row[2].is_checked
            active_col = COLORS["success"]
            row[1].configure(fg_color=active_col if v else COLORS["border_card"], text="✓" if v else ""); row[1].is_checked = v

    def toggle_sites(self):
        s = self.check_all_sites.get()
        for bi, bo, site in self.site_checks_static:
            v = s and not bo.is_checked
            active_col = COLORS["success"]
            bi.configure(fg_color=active_col if v else COLORS["border_card"], text="✓" if v else ""); bi.is_checked = v
            if v: self.selected_sites_include.add(site); self.selected_sites_exclude.discard(site)
            else: self.selected_sites_include.discard(site)
        for row in self.site_list_custom:
            v = s and len(row[0].get())>0 and not row[2].is_checked
            active_col = COLORS["success"]
            row[1].configure(fg_color=active_col if v else COLORS["border_card"], text="✓" if v else ""); row[1].is_checked = v

    def reset_keywords(self):
        for row in self.kw_list:
            row[0].delete(0, "end"); row[1].configure(fg_color=COLORS["border_card"], text=""); row[1].is_checked=False
            row[2].configure(fg_color=COLORS["border_card"], text=""); row[2].is_checked=False
        self.kw_check_all.deselect()

    def reset_navs(self):
        for cb in self.nav_checks: cb.deselect()
        self.check_all_nav.deselect()

    def reset_files(self):
        for cb in self.file_checks: cb.deselect()
        for row in self.custom_file_list:
            row[0].delete(0, "end"); row[1].configure(fg_color=COLORS["border_card"], text=""); row[1].is_checked=False
            row[2].configure(fg_color=COLORS["border_card"], text=""); row[2].is_checked=False
        self.file_check_all.deselect()

    def reset_sites(self):
        self.selected_sites_include.clear()
        self.selected_sites_exclude.clear()
        self.update_site_list_display(self.cat_seg.get())
        for row in self.site_list_custom:
            row[0].delete(0, "end"); row[1].configure(fg_color=COLORS["border_card"], text=""); row[1].is_checked=False
            row[2].configure(fg_color=COLORS["border_card"], text=""); row[2].is_checked=False
        self.check_all_sites.deselect()

    def load_profile_data(self, name):
        if name == self.translations[self.current_lang]["load_profile"]: return
        if not os.path.exists(self.profiles_file): return
        with open(self.profiles_file, "r") as f:
            profiles = json.load(f); data = profiles.get(name)
            if not data: return
        for l in [self.kw_list, self.site_list_custom, self.custom_file_list]:
            for row in l: row[3].destroy()
            l.clear()
        for val, bi_s, bo_s in data.get("keywords", []):
            self.add_keyword_field(); row = self.kw_list[-1]; row[0].insert(0, val)
            if bi_s: self.toggle_selection_simple(row[1], row[2], True)
            if bo_s: self.toggle_selection_simple(row[2], row[1], True)
        for val, bi_s, bo_s in data.get("sites_custom", []):
            self.add_site_field(); row = self.site_list_custom[-1]; row[0].insert(0, val)
            if bi_s: self.toggle_selection_simple(row[1], row[2], True)
            if bo_s: self.toggle_selection_simple(row[2], row[1], True)
        
        self.selected_sites_include = set(data.get("sites_include", []))
        self.selected_sites_exclude = set(data.get("sites_exclude", []))
        self.update_site_list_display(self.cat_seg.get())
        
        self.selected_continents_include = set(data.get("continents_include", []))
        self.selected_continents_exclude = set(data.get("continents_exclude", []))
        for bi, bo, c in self.continent_checks:
            if c in self.selected_continents_include: bi.configure(fg_color=COLORS["success"], text="✓", font=("Segoe UI", 12, "bold")); bi.is_checked = True
            elif c in self.selected_continents_exclude: bo.configure(fg_color=COLORS["danger"], text="✓", font=("Segoe UI", 12, "bold")); bo.is_checked = True
            else: bi.configure(fg_color=COLORS["border_card"], text=""); bi.is_checked = False; bo.configure(fg_color=COLORS["border_card"], text=""); bo.is_checked = False
        
        for i, checked in enumerate(data.get("file_checks", [])):
            if i < len(self.file_checks):
                if checked: self.file_checks[i].select()
                else: self.file_checks[i].deselect()
        sw = data.get("switches", {})
        self.img_mode_var.set(sw.get("img", False))
        self.open_server_var.set(sw.get("server", False))
        self.logs_stealer_var.set(sw.get("logs", False))
        self.onion_var.set(sw.get("onion", False))
        self.cloud_var.set(sw.get("cloud", False))
        self.config_var.set(sw.get("config", False))
        self.geo_var.set(data.get("geo", "All Countries"))
        
        tf = data.get("time_filter", "all")
        self.handle_time_check(tf) 
        
        # Load operators mutual exclusivity
        for key in ["exact", "intext", "intitle", "inurl", "inanchor", "related", "archive"]:
            cb = getattr(self, f"{key}_m")
            if sw.get(key, False): cb.select()
            else: cb.deselect()
            
        self.toggle_img_filters(); self.sync_date_logic()

    def toggle_selection_simple(self, c, o, force_on=False):
        if force_on:
            color = COLORS["success"] if c.btn_type == "in" else COLORS["danger"]
            c.configure(fg_color=color, text="✓", font=("Segoe UI", 12, "bold"))
            c.is_checked = True
            o.configure(fg_color=COLORS["border_card"], text=""); o.is_checked = False

    def save_current_as_profile(self, name):
        data = {
            "keywords": [(row[0].get(), row[1].is_checked, row[2].is_checked) for row in self.kw_list],
            "sites_custom": [(row[0].get(), row[1].is_checked, row[2].is_checked) for row in self.site_list_custom],
            "sites_include": list(self.selected_sites_include),
            "sites_exclude": list(self.selected_sites_exclude),
            "continents_include": list(self.selected_continents_include),
            "continents_exclude": list(self.selected_continents_exclude),
            "file_checks": [cb.get() for cb in self.file_checks],
            "geo": self.geo_var.get(),
            "time_filter": self.active_time_filter,
            "switches": {
                "img": self.img_mode_var.get(), "server": self.open_server_var.get(), "logs": self.logs_stealer_var.get(),
                "onion": self.onion_var.get(), "cloud": self.cloud_var.get(), "config": self.config_var.get(),
                "exact": self.exact_m.get(), "intext": self.intext_m.get(), "intitle": self.intitle_m.get(),
                "inurl": self.inurl_m.get(), "inanchor": self.inanchor_m.get(), "related": self.related_m.get(), "archive": self.archive_m.get()
            }
        }
        profiles = {}
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, "r") as f:
                try: profiles = json.load(f)
                except: profiles = {}
        profiles[name] = data
        with open(self.profiles_file, "w") as f: json.dump(profiles, f, indent=4)
        self.refresh_profile_list()

    def refresh_profile_list(self):
        vals = [self.translations[self.current_lang]["load_profile"]]
        if os.path.exists(self.profiles_file):
            with open(self.profiles_file, "r") as f:
                try: vals.extend(list(json.load(f).keys()))
                except: pass
        self.profile_menu.configure(values=vals)

    def toggle_img_filters(self):
        if self.img_mode_var.get():
            self.img_filter_container.pack(after=self.switch_img, fill="x", pady=5)
            for cb in self.nav_checks:
                if cb.cget("text") == "Google": cb.select(); cb.configure(state="normal")
                else: cb.deselect(); cb.configure(state="disabled")
        else:
            self.img_filter_container.pack_forget()
            for cb in self.nav_checks: cb.configure(state="normal")

    def copy_to_clipboard(self):
        if self.last_dork:
            self.clipboard_clear(); self.clipboard_append(self.last_dork)
            self.copy_btn.configure(fg_color=COLORS["success"], text="COPIED!")
            self.after(1000, lambda: self.copy_btn.configure(fg_color=COLORS["border_card"], text=self.translations[self.current_lang]["copy"]))

    def run_investigation(self):
        final = []
        if self.open_server_var.get(): final.append('intitle:"index of"')
        kw_in = [e.get().strip() for e, bi, bo, _ in self.kw_list if e.get().strip() and bi.is_checked]
        kw_out = [f'-"{e.get().strip()}"' for e, bi, bo, _ in self.kw_list if e.get().strip() and bo.is_checked]
        if self.archive_m.get() and kw_in: 
            self.last_dork = f"Wayback: {kw_in[0]}"; webbrowser.open(f"https://web.archive.org/web/*/{kw_in[0]}"); return
        if kw_in:
            q = " ".join([f'"{x}"' if self.exact_m.get() else x for x in kw_in])
            if self.logs_stealer_var.get(): q = f'({q}) (intext:"password" OR intext:"login" OR intext:"credentials") (filetype:log OR filetype:sql OR filetype:env)'
            if self.onion_var.get(): q = f'({q}) (site:onion.link OR site:tor2web.org OR intext:".onion")'
            if self.cloud_var.get(): q = f'({q}) (site:s3.amazonaws.com OR site:storage.googleapis.com OR site:blob.core.windows.net)'
            if self.config_var.get(): q = f'({q}) (filetype:env OR filetype:yaml OR filetype:json "DB_PASSWORD" OR "AWS_ACCESS_KEY_ID")'
            if self.intitle_m.get(): q = f'intitle:{q}'
            if self.intext_m.get(): q = f'intext:{q}'
            if self.inurl_m.get(): q = f'inurl:{q}'
            if self.inanchor_m.get(): q = f'inanchor:{q}'
            if self.related_m.get(): q = f'related:{kw_in[0]}'
            final.append(q)
        final.extend(kw_out)
        
        si_in = list(self.selected_sites_include) + [e.get().strip() for e, bi, bo, _ in self.site_list_custom if e.get().strip() and bi.is_checked]
        if si_in:
            if len(si_in) == 1: final.append(f"site:{si_in[0]}")
            else: final.append(f"({' OR '.join(['site:'+s for s in si_in])})")
        
# 1. Custom Geo : On récupère les inclusions manuelles
        geo_in = [e.get().strip() for e, bi, bo, _ in self.geo_list_custom if e.get().strip() and bi.is_checked]
        
        # 2. On récupère la liste des exclusions manuelles pour le filtrage (ex: [".fr"])
        custom_excludes_list = [e.get().strip() for e, bi, bo, _ in self.geo_list_custom if e.get().strip() and bo.is_checked]
        
        # 3. On construit la partie dork négative (-site:.fr)
        geo_out = [f'-site:{e}' for e in custom_excludes_list]
        
        # 4. Continents (Avec filtrage intelligent)
        for cont_name in self.selected_continents_include:
            tlds = CONTINENT_TLDS.get(cont_name, [])
            if tlds:
                # CRUCIAL : On retire les TLDs exclus manuellement de la liste du continent
                filtered_tlds = [t for t in tlds if t not in custom_excludes_list]
                
                if filtered_tlds:
                    or_part = " OR ".join([f"site:{tld}" for tld in filtered_tlds])
                    geo_in.append(f"({or_part})")
        
        for cont_name in self.selected_continents_exclude:
            tlds = CONTINENT_TLDS.get(cont_name, [])
            if tlds:
                for tld in tlds: geo_out.append(f"-site:{tld}")

        if geo_in: final.append(f"({' OR '.join(geo_in)})" if len(geo_in) > 1 else geo_in[0])
        if geo_out: final.extend(geo_out)
            
        fi_in = [cb.cget("text") for cb in self.file_checks if cb.get()] + [e.get().strip() for e, bi, bo, _ in self.custom_file_list if e.get().strip() and bi.is_checked]
        if fi_in:
            if len(fi_in) == 1: final.append(f"filetype:{fi_in[0]}")
            else: final.append(f"({' OR '.join(['filetype:'+f for f in fi_in])})")
        
        if self.active_time_filter is None:
            if self.cb_interval.get() == 1 and self.ent_range.cget("state") == "normal":
                v = self.ent_range.get().strip()
                if v: final.append(v)
            else:
                for a in ["after", "before"]:
                    if hasattr(self, f"cb_{a}") and getattr(self, f"cb_{a}").get() == 1:
                        val = getattr(self, f"ent_{a}_date").get()
                        if val: final.append(f"{a}:{val}")
        
        self.last_dork = " ".join([f for f in final if f.strip()])
        encoded = urllib.parse.quote_plus(self.last_dork)
        
        tbs = []
        if self.active_time_filter and self.active_time_filter != "all":
            tbs.append(f"qdr:{self.active_time_filter}")
            
        if self.img_mode_var.get():
            tm = {"Clipart":"itp:clipart","Lineart":"itp:lineart","GIF":"itp:animated","Face":"itp:face"}
            if self.opt_img_type.get() in tm: tbs.append(tm[self.opt_img_type.get()])
        
        tbs_str = f"&tbs={','.join(tbs)}" if tbs else ""
        tbm = "&tbm=isch" if self.img_mode_var.get() else ""
        
        for cb in self.nav_checks:
            if cb.get() and cb.cget("state") == "normal":
                n = cb.cget("text")
                url = f"https://www.google.com/search?q={encoded}{tbm}{tbs_str}" if n=="Google" else f"https://www.{n.lower()}.com/search?q={encoded}"
                webbrowser.open(url)

    def change_language(self, lang):
        self.current_lang = lang
        d = self.translations[lang]
        for k, w in self.widgets_to_translate.items(): w.configure(text=d[k])
        self.ent_rev_url.configure(placeholder_text=d["rev_placeholder"])
        for i, box in enumerate([self.box_keywords, self.box_nav, self.box_files, self.box_date, self.box_site, self.box_opt, self.box_metier, self.box_action]):
            box.winfo_children()[0].winfo_children()[0].configure(text=d[f"box{i+1}"])
        for c in [self.kw_check_all, self.check_all_nav, self.file_check_all, self.check_all_sites]:
            if c: c.configure(text=d["select_all"])
        
        for i, (cb, val) in enumerate(self.time_checkboxes): 
            cb.configure(text=d["times"][i])
            
        self.refresh_profile_list()

if __name__ == "__main__":
    CuriousSearch().mainloop()