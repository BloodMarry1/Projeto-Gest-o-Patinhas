# -*- coding: utf-8 -*-
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from repositorio_animal import inserir_animal, listar_animais, atualizar_animal, excluir_animal

class AnimalApp(Gtk.Window):
    """Classe principal da interface gráfica em GTK 3 para o sistema Gestão Patinhas."""
    
    def __init__(self):
        super().__init__(title="Gestão Patinhas — Cadastro de Animais")
        self.set_default_size(550, 500)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)

        self.id_selecionado = None

        vbox_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        vbox_principal.set_margin_start(16)
        vbox_principal.set_margin_end(16)
        vbox_principal.set_margin_top(16)
        vbox_principal.set_margin_bottom(16)
        self.add(vbox_principal)
        
        lbl_titulo = Gtk.Label(xalign=0)
        lbl_titulo.set_markup("<b><big>🐾 Cadastro e Gestão de Animais</big></b>")
        vbox_principal.pack_start(lbl_titulo, False, False, 0)

        grid = Gtk.Grid()
        grid.set_row_spacing(8)
        grid.set_column_spacing(12)
        vbox_principal.pack_start(grid, False, False, 0)

        # Nome
        grid.attach(Gtk.Label(label="Nome:", xalign=0), 0, 0, 1, 1)
        self.ent_nome = Gtk.Entry()
        self.ent_nome.set_hexpand(True)
        self.ent_nome.set_placeholder_text("Ex.: Mel")
        grid.attach(self.ent_nome, 1, 0, 1, 1)

        # Espécie
        grid.attach(Gtk.Label(label="Espécie:", xalign=0), 0, 1, 1, 1)
        self.ent_especie = Gtk.Entry()
        self.ent_especie.set_placeholder_text("Ex.: Cão / Gato")
        grid.attach(self.ent_especie, 1, 1, 1, 1)

        # Raça
        grid.attach(Gtk.Label(label="Raça:", xalign=0), 0, 2, 1, 1)
        self.ent_raca = Gtk.Entry()
        self.ent_raca.set_placeholder_text("Ex.: SRD")
        grid.attach(self.ent_raca, 1, 2, 1, 1)

        # Porte
        grid.attach(Gtk.Label(label="Porte:", xalign=0), 0, 3, 1, 1)
        self.ent_porte = Gtk.Entry()
        self.ent_porte.set_placeholder_text("Ex.: Pequeno / Médio")
        grid.attach(self.ent_porte, 1, 3, 1, 1)

        box_botoes = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        box_botoes.set_homogeneous(True)
        vbox_principal.pack_start(box_botoes, False, False, 0)

        btn_gravar = Gtk.Button(label="Gravar")
        btn_gravar.connect("clicked", self.on_gravar_clicked)
        box_botoes.pack_start(btn_gravar, True, True, 0)

        btn_excluir = Gtk.Button(label="Excluir Selecionado")
        btn_excluir.connect("clicked", self.on_excluir_clicked)
        box_botoes.pack_start(btn_excluir, True, True, 0)

        self.lbl_mensagem = Gtk.Label(label="Preencha os dados e clique em Gravar.", xalign=0)
        vbox_principal.pack_start(self.lbl_mensagem, False, False, 0)

        self.list_animais = Gtk.ListStore(int, str, str, str, str)
        self.tvw_animais = Gtk.TreeView(model=self.list_animais)
        
        for i, titulo in enumerate(["ID", "Nome", "Espécie", "Raça", "Porte"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(titulo, renderer, text=i)
            self.tvw_animais.append_column(column)
            
        selecao = self.tvw_animais.get_selection()
        selecao.connect("changed", self.on_tabela_selected)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        scrolled.add(self.tvw_animais)
        vbox_principal.pack_start(scrolled, True, True, 0)

        self.atualizar_tabela()
        self.show_all()

    def atualizar_tabela(self):
        """Busca os animais no banco de dados e atualiza a exibição na tabela."""
        try:
            self.list_animais.clear()
            animais = listar_animais()
            for anim in animais:
                self.list_animais.append([anim[0], anim[1], anim[2], anim[3], anim[4]])
        except Exception as e:
            self.lbl_mensagem.set_text(f"Erro ao carregar dados: {e}")

    def on_tabela_selected(self, selection):
        """Captura o item selecionado na tabela para permitir edição ou exclusão."""
        model, treeiter = selection.get_selected()
        if treeiter != None:
            self.id_selecionado = model[treeiter][0]
            self.ent_nome.set_text(model[treeiter][1])
            self.ent_especie.set_text(model[treeiter][2])
            self.ent_raca.set_text(model[treeiter][3])
            self.ent_porte.set_text(model[treeiter][4])

    def on_gravar_clicked(self, button):
        """Executa a inserção ou atualização de um animal com tratamento de erros."""
        nome = self.ent_nome.get_text().strip()
        especie = self.ent_especie.get_text().strip()
        raca = self.ent_raca.get_text().strip()
        porte = self.ent_porte.get_text().strip()

        if not nome or not especie:
            self.lbl_mensagem.set_text("Erro: Preencha os campos obrigatórios (Nome e Espécie).")
            return

        try:
            if self.id_selecionado is None:
                inserir_animal(nome, especie, raca, porte, None, "Não", "Disponível")
                self.lbl_mensagem.set_text("Animal cadastrado com sucesso!")
            else:
                atualizar_animal(self.id_selecionado, nome, especie, raca, porte, None, "Não", "Disponível")
                self.lbl_mensagem.set_text("Animal atualizado com sucesso!")
                self.id_selecionado = None

            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            self.lbl_mensagem.set_text(f"Erro ao salvar: {e}")

    def on_excluir_clicked(self, button):
        """Exclui o animal selecionado na tabela."""
        if self.id_selecionado is None:
            self.lbl_mensagem.set_text("Selecione um animal na tabela para excluir.")
            return
        try:
            excluir_animal(self.id_selecionado)
            self.lbl_mensagem.set_text("Animal excluído com sucesso!")
            self.id_selecionado = None
            self.limpar_campos()
            self.atualizar_tabela()
        except Exception as e:
            self.lbl_mensagem.set_text(f"Erro ao excluir: {e}")

    def limpar_campos(self):
        """Limpa as caixas de texto do formulário."""
        self.ent_nome.set_text("")
        self.ent_especie.set_text("")
        self.ent_raca.set_text("")
        self.ent_porte.set_text("")

if __name__ == "__main__":
    app = AnimalApp()
    Gtk.main()


