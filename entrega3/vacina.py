import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from repositorio_vacina import registrar_vacina, listar_vacinas, excluir_vacina

class VacinaWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gestão Patinhas — Controle de Vacinas (GTK)")
        self.set_border_width(10)
        self.set_default_size(600, 500)

        self.id_selecionado = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        lbl_titulo = Gtk.Label()
        lbl_titulo.set_markup("<b><big>🐾 Controle de Vacinas</big></b>")
        vbox.pack_start(lbl_titulo, False, False, 10)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        vbox.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label(label="ID Animal:"), 0, 0, 1, 1)
        self.entry_animal = Gtk.Entry()
        grid.attach(self.entry_animal, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Nome Vacina:"), 0, 1, 1, 1)
        self.entry_vacina = Gtk.Entry()
        grid.attach(self.entry_vacina, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Data (AAAA-MM-DD):"), 0, 2, 1, 1)
        self.entry_data = Gtk.Entry()
        grid.attach(self.entry_data, 1, 2, 1, 1)

        hbox_botoes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        btn_gravar = Gtk.Button(label="Registrar Vacina")
        btn_gravar.connect("clicked", self.on_gravar_clicked)
        hbox_botoes.pack_start(btn_gravar, True, True, 0)

        btn_excluir = Gtk.Button(label="Excluir")
        btn_excluir.connect("clicked", self.on_excluir_clicked)
        hbox_botoes.pack_start(btn_excluir, True, True, 0)

        vbox.pack_start(hbox_botoes, False, False, 5)

        self.liststore = Gtk.ListStore(int, str, str, str)
        self.atualizar_tabela()

        self.treeview = Gtk.TreeView(model=self.liststore)
        colunas = ["ID", "Animal", "Vacina", "Data"]
        for i, coluna_titulo in enumerate(colunas):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(coluna_titulo, renderer, text=i)
            self.treeview.append_column(column)

        selection = self.treeview.get_selection()
        selection.connect("changed", self.on_tree_selection_changed)

        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(self.treeview)
        vbox.pack_start(scrolledwindow, True, True, 0)

    def atualizar_tabela(self):
        self.liststore.clear()
        try:
            vacinas = listar_vacinas()
            for v in vacinas:
                self.liststore.append([v[0], str(v[1]), v[2], str(v[3])])
        except Exception as e:
            print(f"Erro: {e}")

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_selecionado = model[treeiter][0]
            self.entry_animal.set_text(model[treeiter][1])
            self.entry_vacina.set_text(model[treeiter][2])
            self.entry_data.set_text(model[treeiter][3])

    def on_gravar_clicked(self, widget):
        id_animal = self.entry_animal.get().strip()
        nome_vacina = self.entry_vacina.get().strip()
        data = self.entry_data.get().strip()

        if not id_animal or not nome_vacina or not data:
            return

        try:
            registrar_vacina(id_animal, nome_vacina, data)
            self.entry_animal.set_text("")
            self.entry_vacina.set_text("")
            self.entry_data.set_text("")
            self.atualizar_tabela()
        except Exception as e:
            print(f"Erro: {e}")

    def on_excluir_clicked(self, widget):
        if self.id_selecionado is not None:
            excluir_vacina(self.id_selecionado)
            self.id_selecionado = None
            self.atualizar_tabela()