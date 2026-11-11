import tkinter as tk
from tkinter import ttk, messagebox
from repositorio_animal import inserir_animal, listar_animais, atualizar_animal, excluir_animal

class AnimalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestão Patinhas — Cadastro de Animais")
        self.root.geometry("550x500")
        self.root.config(bg="#f4f4f4")
        
        self.id_selecionado = None

        # Título
        lbl_titulo = tk.Label(root, text="🐾 Cadastro e Gestão de Animais", font=("Arial", 14, "bold"), bg="#f4f4f4", fg="#333")
        lbl_titulo.pack(pady=15)

        # Frame do Formulário
        frame_form = tk.Frame(root, bg="#f4f4f4")
        frame_form.pack(pady=5)

        tk.Label(frame_form, text="Nome:", bg="#f4f4f4", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.ent_nome = tk.Entry(frame_form, width=35, font=("Arial", 10))
        self.ent_nome.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Espécie:", bg="#f4f4f4", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.ent_especie = tk.Entry(frame_form, width=35, font=("Arial", 10))
        self.ent_especie.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Raça:", bg="#f4f4f4", font=("Arial", 10)).grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ent_raca = tk.Entry(frame_form, width=35, font=("Arial", 10))
        self.ent_raca.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Porte:", bg="#f4f4f4", font=("Arial", 10)).grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.ent_porte = tk.Entry(frame_form, width=35, font=("Arial", 10))
        self.ent_porte.grid(row=3, column=1, padx=5, pady=5)

        # Botões de Ação
        frame_botoes = tk.Frame(root, bg="#f4f4f4")
        frame_botoes.pack(pady=10)

        btn_gravar = tk.Button(frame_botoes, text="Gravar", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=12, command=self.on_gravar)
        btn_gravar.pack(side=tk.LEFT, padx=5)

        btn_excluir = tk.Button(frame_botoes, text="Excluir", bg="#f44336", fg="white", font=("Arial", 10, "bold"), width=12, command=self.on_excluir)
        btn_excluir.pack(side=tk.LEFT, padx=5)

        # Tabela (Treeview)
        self.tree = ttk.Treeview(root, columns=("ID", "Nome", "Espécie", "Raça", "Porte"), show="headings", height=8)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Espécie", text="Espécie")
        self.tree.heading("Raça", text="Raça")
        self.tree.heading("Porte", text="Porte")
        
        self.tree.column("ID", width=40)
        self.tree.column("Nome", width=100)
        self.tree.column("Espécie", width=90)
        self.tree.column("Raça", width=100)
        self.tree.column("Porte", width=90)
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        self.atualizar_tabela()

    def atualizar_tabela(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        try:
            animais = listar_animais()
            for anim in animais:
                self.tree.insert("", tk.END, values=(anim[0], anim[1], anim[2], anim[3], anim[4]))
        except Exception as e:
            messagebox.showerror("Erro de Conexão", f"Não foi possível carregar os dados:\n{e}")

    def on_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            values = self.tree.item(selected_item[0], "values")
            self.id_selecionado = values[0]
            self.ent_nome.delete(0, tk.END)
            self.ent_nome.insert(0, values[1])
            self.ent_especie.delete(0, tk.END)
            self.ent_especie.insert(0, values[2])
            self.ent_raca.delete(0, tk.END)
            self.ent_raca.insert(0, values[3])
            self.ent_porte.delete(0, tk.END)
            self.ent_porte.insert(0, values[4])

    def on_gravar(self):
        nome = self.ent_nome.get().strip()
        especie = self.ent_especie.get().strip()
        raca = self.ent_raca.get().strip()
        porte = self.ent_porte.get().strip()

        if not nome or not especie:
            messagebox.showwarning("Aviso", "Preencha os campos obrigatórios (Nome e Espécie).")
            return

        try:
            if self.id_selecionado is None:
                inserir_animal(nome, especie, raca, porte, None, "Não", "Disponível")
                messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")
            else:
                atualizar_animal(self.id_selecionado, nome, especie, raca, porte, None, "Não", "Disponível")
                messagebox.showinfo("Sucesso", "Animal atualizado com sucesso!")
                self.id_selecionado = None
            
            self.limpar()
            self.atualizar_tabela()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar no banco:\n{e}")

    def on_excluir(self):
        if self.id_selecionado is None:
            messagebox.showwarning("Aviso", "Selecione um animal na tabela para excluir.")
            return
        
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este animal?"):
            try:
                excluir_animal(self.id_selecionado)
                messagebox.showinfo("Sucesso", "Animal excluído com sucesso!")
                self.id_selecionado = None
                self.limpar()
                self.atualizar_tabela()
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir:\n{e}")

    def limpar(self):
        self.ent_nome.delete(0, tk.END)
        self.ent_especie.delete(0, tk.END)
        self.ent_raca.delete(0, tk.END)
        self.ent_porte.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnimalApp(root)
    root.mainloop()