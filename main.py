import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
import subprocess
import requests
# TASARIM AYARLARI
COLLAPSED_SIZE = 65  
EXPANDED_WIDTH = 360
EXPANDED_HEIGHT = 140 
OPACITY_INACTIVE = 0.85
OPACITY_ACTIVE = 1.0

CSS = """
window {
    background-color: #121212;
    border-radius: 35px; 
}
#logo_collapsed {
    color: #1DB954;
    font-size: 50px; 
}
#logo_panel {
    color: #1DB954;
    font-size: 32px;
}
label { 
    color: #FFFFFF; 
    font-family: "Noto Sans", sans-serif;
}
button {
    background: transparent;
    color: #b3b3b3;
    border: none;
    box-shadow: none;
    text-shadow: none;
    background-image: none;
    outline: none;
    font-size: 22px;
}
button:hover { 
    color: #ffffff; 
}
button:focus {
    box-shadow: none;
    background: transparent;
}

#shuffle.active { color: #1DB954; }
progressbar trough { background-color: #333333; border-radius: 5px; min-height: 5px; }
progressbar progress { background-color: #1DB954; border-radius: 5px; }
scale contents trough highlight { background-color: #1DB954; }
"""

class SpotifyWidget(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
        
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(CSS.encode('utf-8'))
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), style_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        self.set_decorated(False)
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_above(True)
        self.set_opacity(OPACITY_INACTIVE)
        self.set_skip_taskbar_hint(True)

        self.expanded = False
        self.current_cover_url = ""

        #Ana Kutu Event içinde sürüklenmek için
        self.drag_area = Gtk.EventBox()
        self.add(self.drag_area)
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.drag_area.add(self.main_box)

        # Logo Panel
        self.collapsed_box = Gtk.Box()
        self.logo_label = Gtk.Label(label="")
        self.logo_label.set_name("logo_collapsed")
        self.logo_label.set_size_request(COLLAPSED_SIZE, COLLAPSED_SIZE)
        self.collapsed_box.pack_start(self.logo_label, True, True, 0)
        self.main_box.pack_start(self.collapsed_box, False, False, 0)

        # Açık Panel
        self.panel = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.panel.set_margin_start(12)
        self.panel.set_margin_end(12)
        self.panel.set_margin_top(12)
        self.panel.set_margin_bottom(12)

        header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        self.panel_logo = Gtk.Label(label="")
        self.panel_logo.set_name("logo_panel")
        header.pack_start(self.panel_logo, False, False, 0)

        info_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.song_label = Gtk.Label()
        self.song_label.set_xalign(0)
        self.song_label.set_ellipsize(3)
        info_vbox.pack_start(self.song_label, True, True, 0)
        header.pack_start(info_vbox, True, True, 0)

        self.cover_art = Gtk.Image()
        header.pack_end(self.cover_art, False, False, 0)
        self.panel.pack_start(header, False, False, 0)

        self.progress = Gtk.ProgressBar()
        self.panel.pack_start(self.progress, False, False, 0)

        controls_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.btn_box = Gtk.Box(spacing=15)
        self.btn_box.set_halign(Gtk.Align.CENTER)
        
        self.shuffle_btn = Gtk.Button(label="")
        self.shuffle_btn.set_name("shuffle")
        self.prev_btn = Gtk.Button(label="⏮")
        self.play_btn = Gtk.Button(label="▶") 
        self.play_btn.set_name("play_pause")
        self.next_btn = Gtk.Button(label="⏭")
        
        for btn in [self.shuffle_btn, self.prev_btn, self.play_btn, self.next_btn]:
            self.btn_box.pack_start(btn, False, False, 0)
        controls_row.pack_start(self.btn_box, True, True, 0)

        vol_box = Gtk.Box(spacing=5)
        vol_box.pack_start(Gtk.Label(label="🔈"), False, False, 0)
        self.vol_slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 1, 0.05)
        self.vol_slider.set_size_request(70, -1)
        
        # Baslangicta mevcut ses seviyesini cek (eger alinamazsa %50)
        try:
            initial_vol = float(subprocess.check_output("playerctl volume", shell=True, stderr=subprocess.DEVNULL).decode().strip())
            self.vol_slider.set_value(initial_vol)
        except:
            self.vol_slider.set_value(0.5)
            
        vol_box.pack_start(self.vol_slider, True, True, 0)
        controls_row.pack_end(vol_box, False, False, 5)

        self.panel.pack_start(controls_row, False, False, 0)
        self.main_box.pack_start(self.panel, True, True, 0)
        self.panel.hide()

        # Olay Bağlantıları (Sürükleme ve Tıklama)
        self.drag_area.connect("button-press-event", self.on_button_press)
        
        self.shuffle_btn.connect("clicked", lambda _: subprocess.run("playerctl shuffle toggle", shell=True))
        self.prev_btn.connect("clicked", lambda _: subprocess.run("playerctl previous", shell=True))
        self.play_btn.connect("clicked", lambda _: subprocess.run("playerctl play-pause", shell=True))
        self.next_btn.connect("clicked", lambda _: subprocess.run("playerctl next", shell=True))
        self.vol_slider.connect("value-changed", lambda s: subprocess.run(f"playerctl volume {s.get_value()}", shell=True))

        self.connect("focus-out-event", lambda w,e: self.toggle(False) if self.expanded else False)
        GLib.timeout_add(1000, self.update)
        self.show_all()

    def update(self):
        try:
            artist = subprocess.check_output("playerctl metadata artist", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            title = subprocess.check_output("playerctl metadata title", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            self.song_label.set_markup(f"<b>{title}</b>\n<span color='#b3b3b3'>{artist}</span>")
            status = subprocess.check_output("playerctl status", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            self.play_btn.set_label("||" if status == "Playing" else "▶")
            cover_url = subprocess.check_output("playerctl metadata mpris:artUrl", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if cover_url != self.current_cover_url:
                self.update_cover(cover_url)
                self.current_cover_url = cover_url
            pos = float(subprocess.check_output("playerctl position", shell=True, stderr=subprocess.DEVNULL).decode())
            length = float(subprocess.check_output("playerctl metadata mpris:length", shell=True, stderr=subprocess.DEVNULL).decode()) / 1000000
            self.progress.set_fraction(pos / length if length > 0 else 0)
            shuf = subprocess.check_output("playerctl shuffle", shell=True, stderr=subprocess.DEVNULL).decode().strip()
            if shuf == "On": self.shuffle_btn.get_style_context().add_class("active")
            else: self.shuffle_btn.get_style_context().remove_class("active")
        except: pass
        return True

    def update_cover(self, url):
        try:
            if url.startswith("file://"): url = url[7:]
            if url.startswith("http"):
                r = requests.get(url, timeout=5)
                loader = GdkPixbuf.PixbufLoader()
                loader.write(r.content)
                loader.close()
                pixbuf = loader.get_pixbuf()
            else: pixbuf = GdkPixbuf.Pixbuf.new_from_file(url)
            pixbuf = pixbuf.scale_simple(50, 50, GdkPixbuf.InterpType.BILINEAR)
            self.cover_art.set_from_pixbuf(pixbuf)
        except: pass

    def on_button_press(self, widget, event):
        if event.button == 1: # Sol tık: Sürükle
            self.begin_move_drag(event.button, int(event.x_root), int(event.y_root), event.time)
        elif event.button == 3: # Sağ tık: Panel Aç/Kapat
            self.toggle(not self.expanded)
        return True

    def toggle(self, state):
        self.expanded = state
        if self.expanded:
            self.collapsed_box.hide()
            self.panel.show_all()
            self.resize(EXPANDED_WIDTH, EXPANDED_HEIGHT)
        else:
            self.panel.hide()
            self.collapsed_box.show_all()
            self.resize(COLLAPSED_SIZE, COLLAPSED_SIZE)

if __name__ == "__main__":
    win = SpotifyWidget()
    # İlk açılışta sağ alt köşeye taşı
    screen = Gdk.Screen.get_default()
    monitor = screen.get_monitor_geometry(screen.get_primary_monitor())
    win.move(monitor.width - 100, monitor.height - 150)
    win.connect("destroy", Gtk.main_quit)
    Gtk.main()