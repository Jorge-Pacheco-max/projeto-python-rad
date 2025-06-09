import tkinter as tk
import csv
from tkinter import ttk, messagebox
from database import criar_banco, get_connection


def salvar_alunos_txt(alunos):
    with open('alunos.txt', 'w') as file:
        for aluno in alunos:
            file.write(f"{aluno[0]} - {aluno[1]}\n")


def salvar_alunos_csv(alunos):
    with open('alunos.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Matrícula', 'Nome'])
        writer.writerows(alunos)


def salvar_disciplinas_txt(disciplinas):
    with open('disciplinas.txt', 'w') as file:
        for disciplina in disciplinas:
            file.write(f"{disciplina[0]} - {disciplina[1]} - {disciplina[2]} - {disciplina[3]} - {disciplina[4]}\n")


def salvar_disciplinas_csv(disciplinas):
    with open('disciplinas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nome', 'Turma', 'Sala', 'Professor'])
        writer.writerows(disciplinas)


def salvar_notas_txt(notas):
    with open('notas.txt', 'w') as file:
        for nota in notas:
            file.write(f"{nota[0]} - {nota[1]} - {nota[2]}\n")


def salvar_notas_csv(notas):
    with open('notas.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Matrícula', 'ID Disciplina', 'Nota'])
        writer.writerows(notas)

class SistemaEscolar:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Escolar")
        self.root.geometry("1000x700")

        # Garantir que o banco existe
        criar_banco()

        # Criar abas
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Abas do sistema
        self.criar_aba_alunos()
        self.criar_aba_disciplinas()
        self.criar_aba_notas()

    # -------------------------------------------------------------------------------------

    def criar_aba_alunos(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Alunos")

        # Frame do formulário
        form_frame = ttk.LabelFrame(frame, text="Dados do Aluno", padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Alinhamento dos campos
        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)  # Nome
        self.entry_nome_aluno = ttk.Entry(form_frame, width=30)
        self.entry_nome_aluno.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Data Nascimento:").grid(row=1, column=0, sticky=tk.W)  # Data de Nascimento
        self.entry_dt_nascimento = ttk.Entry(form_frame, width=30)
        self.entry_dt_nascimento.grid(row=1, column=1, padx=5, pady=5)

        # Frame de botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=10)

        # Organizando botões
        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_aluno).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_aluno).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_aluno).grid(row=0, column=2, padx=5)
        # ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos_aluno).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Salvar em TXT", command=self.salvar_alunos_txt).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Salvar em CSV", command=self.salvar_alunos_csv).grid(row=0, column=5, padx=5)

        # Treeview para listar alunos
        self.tree_alunos = ttk.Treeview(frame, columns=('Matrícula', 'Nome', 'Nascimento'), show='headings')
        self.tree_alunos.heading('Matrícula', text='Matrícula')
        self.tree_alunos.heading('Nome', text='Nome')
        self.tree_alunos.heading('Nascimento', text='Data Nascimento')

        # Configurar largura das colunas
        self.tree_alunos.column('Matrícula', width=100)
        self.tree_alunos.column('Nome', width=250)
        self.tree_alunos.column('Nascimento', width=100)

        self.tree_alunos.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Carregar alunos
        self.carregar_alunos()

    def carregar_alunos(self):
        # Limpar treeview
        for item in self.tree_alunos.get_children():
            self.tree_alunos.delete(item)

        # Buscar alunos no banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome, dt_nascimento FROM alunos")
        rows = cursor.fetchall()
        conn.close()

        # Adicionar à treeview
        for row in rows:
            matricula= f"{row[0]:012d}"  # Formatar matrícula para 12 dígitos
            self.tree_alunos.insert('', tk.END, values=(matricula, row[1], row[2]))

    def adicionar_aluno(self):
        # Obter dados do formulário
        nome = self.entry_nome_aluno.get()
        dt_nascimento = self.entry_dt_nascimento.get()

        # Validar campos
        if not nome:
            messagebox.showerror("Erro", "O nome é obrigatório!")
            return

        # Inserir no banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO alunos (nome, dt_nascimento)
                       VALUES (?, ?)
                       """, (nome, dt_nascimento))
        conn.commit()
        conn.close()

        # Atualizar interface
        self.carregar_alunos()
        self.limpar_campos_aluno()
        messagebox.showinfo("Sucesso", "Aluno adicionado com sucesso!")

    def editar_aluno(self):
        # Verificar se há aluno selecionado
        selected = self.tree_alunos.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um aluno para editar!")
            return

        # Obter matrícula do aluno selecionado
        item = self.tree_alunos.item(selected[0])
        matricula = item['values'][0]

        # Obter novos dados do formulário
        nome = self.entry_nome_aluno.get()
        dt_nascimento = self.entry_dt_nascimento.get()

        # Validar campos
        if not nome:
            messagebox.showerror("Erro", "O nome é obrigatório!")
            return

        # Atualizar no banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE alunos
                       SET nome=?,
                           dt_nascimento=?
                       WHERE matricula = ?
                       """, (nome, dt_nascimento, matricula))
        conn.commit()
        conn.close()

        # Atualizar interface
        self.carregar_alunos()
        messagebox.showinfo("Sucesso", "Aluno atualizado com sucesso!")

    def excluir_aluno(self):
        # Verificar seleção
        selected = self.tree_alunos.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione um aluno para excluir!")
            return

        # Confirmar exclusão
        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este aluno?"):
            return

        # Obter matrícula
        item = self.tree_alunos.item(selected[0])
        matricula = item['values'][0]

        # Verificar se o aluno tem notas cadastradas
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM notas WHERE matricula_aluno=?", (matricula,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Este aluno possui notas cadastradas e não pode ser excluído!")
            conn.close()
            return

        # Excluir do banco
        cursor.execute("DELETE FROM alunos WHERE matricula=?", (matricula,))
        conn.commit()
        conn.close()

        # Atualizar interface
        self.carregar_alunos()
        self.limpar_campos_aluno()
        messagebox.showinfo("Sucesso", "Aluno excluído com sucesso!")

    def selecionar_aluno(self, event):
        # Preencher formulário com aluno selecionado
        selected = self.tree_alunos.selection()
        if selected:
            item = self.tree_alunos.item(selected[0])
            self.limpar_campos_aluno()
            self.entry_matricula.config(state='normal')
            self.entry_matricula.delete(0, tk.END)
            self.entry_matricula.insert(0, item['values'][0])
            self.entry_matricula.config(state='readonly')
            self.entry_nome_aluno.insert(0, item['values'][1])
            self.entry_dt_nascimento.insert(0, item['values'][2] if len(item['values']) > 2 else "")

    # def limpar_campos_aluno(self):
    #    self.entry_matricula.config(state='normal')
    #   self.entry_matricula.delete(0, tk.END)
    #    self.entry_matricula.config(state='readonly')
    #    self.entry_nome_aluno.delete(0, tk.END)
    #    self.entry_dt_nascimento.delete(0, tk.END)

    def salvar_alunos_txt(self):
        alunos = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome FROM alunos")
        alunos = cursor.fetchall()
        conn.close()

        # Chama a função para salvar em TXT
        salvar_alunos_txt(alunos)
        messagebox.showinfo("Sucesso", "Alunos salvos em alunos.txt")

    def salvar_alunos_csv(self):
        alunos = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome FROM alunos")
        alunos = cursor.fetchall()
        conn.close()

        # Chama a função para salvar em CSV
        salvar_alunos_csv(alunos)
        messagebox.showinfo("Sucesso", "Alunos salvos em alunos.csv")

    # ---------------------------------------------------------------------

    def criar_aba_disciplinas(self):
        # Frame da aba
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Disciplinas")

        # Frame do formulário
        form_frame = ttk.LabelFrame(frame, text="Dados da Disciplina", padding=10)
        form_frame.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        # Campos do formulário

        tk.Label(form_frame, text="Disciplina:").grid(row=1, column=0, sticky=tk.W)  # Nome
        self.entry_nome_disc = ttk.Entry(form_frame, width=30)
        self.entry_nome_disc.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Turma:").grid(row=2, column=0, sticky=tk.W)  # Turma
        self.entry_turma = ttk.Entry(form_frame, width=30)
        self.entry_turma.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Sala:").grid(row=3, column=0, sticky=tk.W)  # Sala
        self.entry_sala = ttk.Entry(form_frame, width=30)
        self.entry_sala.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Professor:").grid(row=4, column=0, sticky=tk.W)  # Professor
        self.entry_professor = ttk.Entry(form_frame, width=30)
        self.entry_professor.grid(row=4, column=1, padx=5, pady=5)

        # Frame de botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=1, column=0, pady=10)

        ttk.Button(btn_frame, text="Adicionar", command=self.adicionar_disciplina).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Editar", command=self.editar_disciplina).grid(row=0, column=1, padx=5)
        ttk.Button(btn_frame, text="Excluir", command=self.excluir_disciplina).grid(row=0, column=2, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_campos_disciplina).grid(row=0, column=3, padx=5)
        ttk.Button(btn_frame, text="Salvar em TXT", command=self.salvar_disciplinas_txt).grid(row=0, column=4, padx=5)
        ttk.Button(btn_frame, text="Salvar em CSV", command=self.salvar_disciplinas_csv).grid(row=0, column=5, padx=5)

        # Treeview para listar disciplinas
        self.tree_disciplinas = ttk.Treeview(frame, columns=('ID', 'Nome', 'Turma', 'Sala', 'Professor'),
                                             show='headings')
        self.tree_disciplinas.heading('ID', text='ID')
        self.tree_disciplinas.heading('Nome', text='Nome')
        self.tree_disciplinas.heading('Turma', text='Turma')
        self.tree_disciplinas.heading('Sala', text='Sala')
        self.tree_disciplinas.heading('Professor', text='Professor')

        # largura das colunas
        self.tree_disciplinas.column('ID', width=50)
        self.tree_disciplinas.column('Nome', width=150)
        self.tree_disciplinas.column('Turma', width=80)
        self.tree_disciplinas.column('Sala', width=80)
        self.tree_disciplinas.column('Professor', width=150)

        # Treeview deve usar grid
        self.tree_disciplinas.grid(row=2, column=0, padx=10, pady=10, sticky=tk.NSEW)

        # Carregar disciplinas
        self.carregar_disciplinas()

    def carregar_disciplinas(self):
        # Limpar treeview
        for item in self.tree_disciplinas.get_children():
            self.tree_disciplinas.delete(item)

        # Buscar disciplinas no banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, turma, sala, professor FROM disciplinas")

        # Adicionar à treeview
        for row in cursor.fetchall():
            self.tree_disciplinas.insert('', tk.END, values=row)

        conn.close()

    def adicionar_disciplina(self):
        nome = self.entry_nome_disc.get()
        turma = self.entry_turma.get()
        sala = self.entry_sala.get()
        professor = self.entry_professor.get()

        if not nome:
            messagebox.showerror("Erro", "O nome da disciplina é obrigatório!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO disciplinas (nome, turma, sala, professor)
                       VALUES (?, ?, ?, ?)
                       """, (nome, turma, sala, professor))
        conn.commit()
        conn.close()

        self.carregar_disciplinas()
        self.limpar_campos_disciplina()
        messagebox.showinfo("Sucesso", "Disciplina adicionada com sucesso!")

    def editar_disciplina(self):
        selected = self.tree_disciplinas.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma disciplina para editar!")
            return

        disciplina_id = self.tree_disciplinas.item(selected[0])['values'][0]
        nome = self.entry_nome_disc.get()
        turma = self.entry_turma.get()
        sala = self.entry_sala.get()
        professor = self.entry_professor.get()

        if not nome:
            messagebox.showerror("Erro", "O nome da disciplina é obrigatório!")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE disciplinas
                       SET 
                           nome=?,
                           turma=?,
                           sala=?,
                           professor=?
                       WHERE id = ?
                       """, (nome, turma, sala, professor, disciplina_id))
        conn.commit()
        conn.close()

        self.carregar_disciplinas()
        messagebox.showinfo("Sucesso", "Disciplina atualizada com sucesso!")

    def excluir_disciplina(self):
        selected = self.tree_disciplinas.selection()
        if not selected:
            messagebox.showerror("Erro", "Selecione uma disciplina para excluir!")
            return

        if not messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta disciplina?"):
            return

        disciplina_id = self.tree_disciplinas.item(selected[0])['values'][0]

        # Verificar se a disciplina tem notas vinculadas
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM notas WHERE disciplina_id=?", (disciplina_id,))
        if cursor.fetchone()[0] > 0:
            messagebox.showerror("Erro", "Esta disciplina possui notas vinculadas e não pode ser excluída!")
            conn.close()
            return

        cursor.execute("DELETE FROM disciplinas WHERE id=?", (disciplina_id,))
        conn.commit()
        conn.close()

        self.carregar_disciplinas()
        self.limpar_campos_disciplina()
        messagebox.showinfo("Sucesso", "Disciplina excluída com sucesso!")

    def selecionar_disciplina(self, event):
        selected = self.tree_disciplinas.selection()
        if selected:
            item = self.tree_disciplinas.item(selected[0])
            self.limpar_campos_disciplina()

            valores = item['values']
            self.entry_nome_disc.insert(0, valores[1])
            self.entry_turma.insert(0, valores[2] if len(valores) > 2 else "")
            self.entry_sala.insert(0, valores[3] if len(valores) > 3 else "")
            self.entry_professor.insert(0, valores[4] if len(valores) > 4 else "")

    def limpar_campos_disciplina(self):
        self.entry_nome_disc.delete(0, tk.END)
        self.entry_turma.delete(0, tk.END)
        self.entry_sala.delete(0, tk.END)
        self.entry_professor.delete(0, tk.END)

    def salvar_disciplinas_txt(self):
        disciplinas = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, turma, sala, professor FROM disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()

        # Chama a função para salvar em TXT
        salvar_disciplinas_txt(disciplinas)
        messagebox.showinfo("Sucesso", "Disciplinas salvas em disciplinas.txt")

    def salvar_disciplinas_csv(self):
        disciplinas = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, turma, sala, professor FROM disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()

        # Chama a função para salvar em CSV
        salvar_disciplinas_csv(disciplinas)
        messagebox.showinfo("Sucesso", "Disciplinas salvas em disciplinas.csv")

#---------------------------------------------------------------------------

    def criar_aba_notas(self):
        # Frame da aba
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Notas")

        # selecionar aluno
        tk.Label(frame, text="Aluno:").grid(row=0, column=0, sticky=tk.W)
        self.combo_aluno = ttk.Combobox(frame, width=30)
        self.combo_aluno.grid(row=0, column=1, padx=5, pady=5)
        self.carregar_alunos_combo()

        # selecionar disciplina
        tk.Label(frame, text="Disciplina:").grid(row=1, column=0, sticky=tk.W)
        self.combo_disciplina = ttk.Combobox(frame, width=30)
        self.combo_disciplina.grid(row=1, column=1, padx=5, pady=5)
        self.carregar_disciplinas_combo()

        # Entrar a Nota
        tk.Label(frame, text="Nota:").grid(row=2, column=0, sticky=tk.W)
        self.entry_nota = tk.Entry(frame, width=10)
        self.entry_nota.grid(row=2, column=1, padx=5, pady=5)

        # Frame de botões
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Adicionar Nota", command=self.adicionar_nota).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Editar Nota", command=self.editar_nota).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Remover Nota", command=self.excluir_nota).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.limpar_campos).grid(row=0, column=3, padx=5)
        tk.Button(btn_frame, text="Salvar em TXT", command=self.salvar_notas_txt).grid(row=0, column=4, padx=5)
        tk.Button(btn_frame, text="Salvar em CSV", command=self.salvar_notas_csv).grid(row=0, column=5, padx=5)

        # Treeview para mostrar notas
        self.tree_notas = ttk.Treeview(frame, columns=('Matrícula', 'ID Disciplina', 'Nota'), show='headings')
        self.tree_notas.heading('Matrícula', text='Matrícula')
        self.tree_notas.heading('ID Disciplina', text='ID Disciplina')
        self.tree_notas.heading('Nota', text='Nota')

        # Configurar largura das colunas
        self.tree_notas.column('Matrícula', width=100)
        self.tree_notas.column('ID Disciplina', width=100)
        self.tree_notas.column('Nota', width=80)

        # Grid para o Treeview
        self.tree_notas.grid(row=4, column=0, padx=10, pady=10, sticky=tk.NSEW)

        self.carregar_notas()

    def carregar_alunos_combo(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT matricula, nome FROM alunos")
        alunos = cursor.fetchall()
        conn.close()

        self.combo_aluno['values'] = [f"{matricula} - {nome}" for matricula, nome in alunos]
        if alunos:  # Preencher a combobox com um valor padrão, se houver alunos
            self.combo_aluno.current(0)

    def carregar_disciplinas_combo(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome FROM disciplinas")
        disciplinas = cursor.fetchall()
        conn.close()

        self.combo_disciplina['values'] = [f"{id} - {nome}" for id, nome in disciplinas]

    def carregar_notas(self):
        # Limpar treeview
        for item in self.tree_notas.get_children():
            self.tree_notas.delete(item)

        # Buscar notas com JOIN para pegar matrículas e ID da disciplina
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT a.matricula, n.disciplina_id, n.valor
                       FROM notas n
                                JOIN alunos a ON n.matricula_aluno = a.matricula
                       """)
        notas = cursor.fetchall()
        conn.close()

        # Adicionar à treeview
        for nota in notas:
            matricula_formatada = f"{nota[0]:012d}"  # Formatar matrícula para 12 dígitos
            self.tree_notas.insert('', tk.END, values=(matricula_formatada, nota[1], nota[2]))

    def adicionar_nota(self):
        # Validar seleções
        if not self.combo_aluno.get() or not self.combo_disciplina.get():
            messagebox.showerror("Erro", "Selecione um aluno e uma disciplina!")
            return

        try:
            # Extrair a matrícula do aluno selecionado corretamente
            matricula = int(self.combo_aluno.get().split(" - ")[0])  #matrícula correta
        except ValueError:
            messagebox.showerror("Erro", "Seleção de aluno inválida!")
            return

        try:
            nota = float(self.entry_nota.get())
            if nota < 0 or nota > 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida! Deve ser entre 0 e 10.")
            return

        # Extrair o ID da disciplina selecionada
        disciplina_id = int(self.combo_disciplina.get().split(" - ")[0])

        # Inserir no banco
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       INSERT INTO notas (valor, matricula_aluno, disciplina_id)
                       VALUES (?, ?, ?)
                       """, (nota, matricula, disciplina_id))
        conn.commit()
        conn.close()

        # Atualizar interface
        self.carregar_notas()
        self.entry_nota.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Nota adicionada com sucesso!")

    def editar_nota(self):
        # Verificar se uma nota está selecionada
        selected_item = self.tree_notas.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma nota para editar!")
            return

        # Obter os valores da nota selecionada
        item = self.tree_notas.item(selected_item[0])
        matricula = item['values'][0]  # Matrícula do aluno
        disciplina_id = item['values'][1]  # ID da disciplina
        valor_nota = item['values'][2]  # Valor da nota

        # Verifica se o campo de nota está preenchido
        if not self.entry_nota.get():
            messagebox.showerror("Erro", "Digite o novo valor da nota!")
            return

        try:
            nova_nota = float(self.entry_nota.get())
            if nova_nota < 0 or nova_nota > 10:
                raise ValueError("Nota deve estar entre 0 e 10.")
        except ValueError:
            messagebox.showerror("Erro", "Nota inválida!")
            return

        # Atualiza a nota no banco de dados
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       UPDATE notas
                       SET valor = ?
                       WHERE matricula_aluno = ?
                         AND disciplina_id = ?
                         AND valor = ? -- Muda a condição conforme necessário
                       """, (nova_nota, matricula, disciplina_id, valor_nota))
        conn.commit()
        conn.close()

        # Atualiza a interface
        self.carregar_notas()
        self.entry_nota.delete(0, tk.END)
        messagebox.showinfo("Sucesso", "Nota atualizada com sucesso!")

    def excluir_nota(self):
        # Verificar se uma nota está selecionada
        selected_item = self.tree_notas.selection()
        if not selected_item:
            messagebox.showerror("Erro", "Selecione uma nota para excluir!")
            return

        # Obter os valores da nota selecionada
        item = self.tree_notas.item(selected_item[0])
        matricula = item['values'][0]  # Matrícula do aluno
        disciplina_id = item['values'][1]  # ID da disciplina

        # Confirmar exclusão
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir esta nota?"):
            # Excluir a nota do banco de dados
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                           DELETE
                           FROM notas
                           WHERE matricula_aluno = ?
                             AND disciplina_id = ?
                           """, (matricula, disciplina_id))
            conn.commit()
            conn.close()

            # Atualiza a interface
            self.carregar_notas()
            messagebox.showinfo("Sucesso", "Nota excluída com sucesso!")

    def limpar_campos(self):
        self.combo_aluno.set('')
        self.combo_disciplina.set('')
        self.entry_nota.delete(0, tk.END)

    def salvar_notas_txt(self):
        notas = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT a.matricula, n.disciplina_id, n.valor
                       FROM notas n
                                JOIN alunos a ON n.matricula_aluno = a.matricula
                       """)
        notas = cursor.fetchall()
        conn.close()

        with open('notas.txt', 'w') as file:
            for nota in notas:
                file.write(f"{nota[0]} - {nota[1]} - {nota[2]}\n")

        messagebox.showinfo("Sucesso", "Notas salvas em notas.txt")

    def salvar_notas_csv(self):
        notas = []
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT a.matricula, n.disciplina_id, n.valor
                       FROM notas n
                                JOIN alunos a ON n.matricula_aluno = a.matricula
                       """)
        notas = cursor.fetchall()
        conn.close()

        with open('notas.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Matrícula', 'ID Disciplina', 'Nota'])  # Cabeçalho
            writer.writerows(notas)

        messagebox.showinfo("Sucesso", "Notas salvas em notas.csv")

if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaEscolar(root)
    root.mainloop()

