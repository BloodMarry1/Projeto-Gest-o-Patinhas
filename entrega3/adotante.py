import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from repositorio_adotante import inserir_adotante, listar_adotantes, atualizar_adotante, excluir_adotante

class AdotanteWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gestão Patinhas — Cadastro de Adotantes (GTK)")
        self.set_border_width(10)
        self.set_default_size(600, 500)

        self.id_selecionado = None

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        lbl_titulo = Gtk.Label()
        lbl_titulo.set_markup("<b><big>🐾 Cadastro de Adotantes</big></b>")
        vbox.pack_start(lbl_titulo, False, False, 10)

        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        vbox.pack_start(grid, False, False, 0)

        grid.attach(Gtk.Label(label="Nome:"), 0, 0, 1, 1)
        self.entry_nome = Gtk.Entry()
        grid.attach(self.entry_nome, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Telefone:"), 0, 1, 1, 1)
        self.entry_telefone = Gtk.Entry()
        grid.attach(self.entry_telefone, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Endereço:"), 0, 2, 1, 1)
        self.entry_endereco = Gtk.Entry()
        grid.attach(self.entry_endereco, 1, 2, 1, 1)

        hbox_botoes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        btn_gravar = Gtk.Button(label="Gravar")
        btn_gravar.connect("clicked", self.on_gravar_clicked)
        hbox_botoes.pack_start(btn_gravar, True, True, 0)

        btn_excluir = Gtk.Button(label="Excluir")
        btn_excluir.connect("clicked", self.on_excluir_clicked)
        hbox_botoes.pack_start(btn_excluir, True, True, 0)

        vbox.pack_start(hbox_botoes, False, False, 5)

        self.liststore = Gtk.ListStore(int, str, str, str)
        self.atualizar_tabela()

        self.treeview = Gtk.TreeView(model=self.liststore)
        colunas = ["ID", "Nome", "Telefone", "Endereço"]
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
            adotantes = listar_adotantes()
            for adot in adotantes:
                self.liststore.append([adot[0], adot[1], adot[2], adot[3]])
        except Exception as e:
            print(f"Erro: {e}")

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_selecionado = model[treeiter][0]
            self.entry_nome.set_text(model[treeiter][1])
            self.entry_telefone.set_text(model[treeiter][2])
            self.entry_endereco.set_text(model[treeiter][3])

    def on_gravar_clicked(self, widget):
        nome = self.entry_nome.get().strip()
        telefone = self.entry_telefone.get().strip()
        endereco = self.entry_endereco.get().strip()

        if not nome or not telefone:
            return

        try:
            if self.id_selecionado is None:
                inserir_adotante(nome, telefone, endereco, "Aprovado")
            else:
                atualizar_adotante(self.id_selecionado, nome, telefone, endereco, "Aprovado")
                self.id_selecionado = None

            self.entry_nome.set_text("")
            self.entry_telefone.set_text("")
            self.entry_endereco.set_text("")
            self.atualizar_tabela()
        except Exception as e:
            print(f"Erro: {e}")

    def on_excluir_clicked(self, widget):
        if self.id_selecionado is not None:
            excluir_adotante(self.id_selecionado)
            self.id_selecionado = None
            self.atualizar_tabela()