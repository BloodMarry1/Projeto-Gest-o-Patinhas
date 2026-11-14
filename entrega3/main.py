import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from animal import AnimalWindow
from adotante import AdotanteWindow
from vacina import VacinaWindow
from adocao import AdocaoWindow

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gestão Patinhas — Menu Principal (GTK)")
        self.set_border_width(20)
        self.set_default_size(350, 300)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=15)
        self.add(vbox)

        lbl_titulo = Gtk.Label()
        lbl_titulo.set_markup("<b><big>🐾 Gestão Patinhas</big></b>")
        vbox.pack_start(lbl_titulo, False, False, 10)

        btn_animal = Gtk.Button(label="1. Gerenciar Animais")
        btn_animal.connect("clicked", lambda w: AnimalWindow().show_all())
        vbox.pack_start(btn_animal, True, True, 0)

        btn_adotante = Gtk.Button(label="2. Gerenciar Adotantes")
        btn_adotante.connect("clicked", lambda w: AdotanteWindow().show_all())
        vbox.pack_start(btn_adotante, True, True, 0)

        btn_vacina = Gtk.Button(label="3. Controle de Vacinas")
        btn_vacina.connect("clicked", lambda w: VacinaWindow().show_all())
        vbox.pack_start(btn_vacina, True, True, 0)

        btn_adocao = Gtk.Button(label="4. Registrar Adoções")
        btn_adocao.connect("clicked", lambda w: AdocaoWindow().show_all())
        vbox.pack_start(btn_adocao, True, True, 0)

if __name__ == "__main__":
    win = MainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()