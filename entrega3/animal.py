import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from repositorio_animal import inserir_animal, listar_animais, atualizar_animal, excluir_animal

class AnimalWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Gestão Patinhas — Cadastro de Animais (GTK)")
        self.set_border_width(10)
        self.set_default_size(600, 500)

        self.id_selecionado = None

        # Layout Principal (Vertical)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Título
        lbl_titulo = Gtk.Label()
        lbl_titulo.set_markup("<b><big>🐾 Cadastro e Gestão de Animais</big></b>")
        vbox.pack_start(lbl_titulo, False, False, 10)

        # Grid do Formulário
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        vbox.pack_start(grid, False, False, 0)

        # Campos
        grid.attach(Gtk.Label(label="Nome:"), 0, 0, 1, 1)
        self.entry_nome = Gtk.Entry()
        grid.attach(self.entry_nome, 1, 0, 1, 1)

        grid.attach(Gtk.Label(label="Espécie:"), 0, 1, 1, 1)
        self.entry_especie = Gtk.Entry()
        grid.attach(self.entry_especie, 1, 1, 1, 1)

        grid.attach(Gtk.Label(label="Raça:"), 0, 2, 1, 1)
        self.entry_raca = Gtk.Entry()
        grid.attach(self.entry_raca, 1, 2, 1, 1)

        grid.attach(Gtk.Label(label="Porte:"), 0, 3, 1, 1)
        self.entry_porte = Gtk.Entry()
        grid.attach(self.entry_porte, 1, 3, 1, 1)

        # Botões de Ação
        hbox_botoes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        
        btn_gravar = Gtk.Button(label="Gravar")
        btn_gravar.connect("clicked", self.on_gravar_clicked)
        hbox_botoes.pack_start(btn_gravar, True, True, 0)

        btn_excluir = Gtk.Button(label="Excluir")
        btn_excluir.connect("clicked", self.on_excluir_clicked)
        hbox_botoes.pack_start(btn_excluir, True, True, 0)

        vbox.pack_start(hbox_botoes, False, False, 5)

        # Tabela (ListStore e TreeView)
        # ID, Nome, Espécie, Raça, Porte
        self.liststore = Gtk.ListStore(int, str, str, str, str)
        self.atualizar_tabela()

        self.treeview = Gtk.TreeView(model=self.liststore)
        
        colunas = ["ID", "Nome", "Espécie", "Raça", "Porte"]
        for i, coluna_titulo in enumerate(colunas):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(coluna_titulo, renderer, text=i)
            self.treeview.append_column(column)

        # Evento de clique na tabela
        selection = self.treeview.get_selection()
        selection.connect("changed", self.on_tree_selection_changed)

        # Scroll para a tabela
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_vexpand(True)
        scrolledwindow.add(self.treeview)
        vbox.pack_start(scrolledwindow, True, True, 0)

    def atualizar_tabela(self):
        self.liststore.clear()
        try:
            animais = listar_animais()
            for anim in animais:
                self.liststore.append([anim[0], anim[1], anim[2], anim[3], anim[4]])
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")

    def on_tree_selection_changed(self, selection):
        model, treeiter = selection.get_selected()
        if treeiter is not None:
            self.id_selecionado = model[treeiter][0]
            self.entry_nome.set_text(model[treeiter][1])
            self.entry_especie.set_text(model[treeiter][2])
            self.entry_raca.set_text(model[treeiter][3])
            self.entry_porte.set_text(model[treeiter][4])

    def on_gravar_clicked(self, widget):
        nome = self.entry_nome.get().strip()
        especie = self.entry_especie.get().strip()
        raca = self.entry_raca.get().strip()
        porte = self.entry_porte.get().strip()

        if not nome or not especie:
            self.mostrar_aviso("Preencha os campos obrigatórios (Nome e Espécie).")
            return

        try:
            if self.id_selecionado is None:
                inserir_animal(nome, especie, raca, porte, None, "Não", "Disponível")
            else:
                atualizar_animal(self.id_selecionado, nome, especie, raca, porte, None, "Não", "Disponível")
                self.id_selecionado = None

            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            self.mostrar_aviso(f"Erro ao salvar no banco: {e}")

    def on_excluir_clicked(self, widget):
        if self.id_selecionado is None:
            self.mostrar_aviso("Selecione um animal na tabela para excluir.")
            return

        try:
            excluir_animal(self.id_selecionado)
            self.id_selecionado = None
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            self.mostrar_aviso(f"Erro ao excluir: {e}")

    def limpar_campos(self):
        self.entry_nome.set_text("")
        self.entry_especie.set_text("")
        self.entry_raca.set_text("")
        self.entry_porte.set_text("")

    def mostrar_aviso(self, mensagem):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK,
            text=mensagem
        )
        dialog.run()
        dialog.destroy()

if __name__ == "__main__":
    win = AnimalWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()