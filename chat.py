import tkinter as ttk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")  # Modo escuro para uma aparência neutra
ctk.set_default_color_theme("dark-blue")  # Tema de cores padrão

class PaginaJogos:
    def __init__(self, root, on_jogo_selected):
        self.root = root
        self.root.title("Escolha um esporte")
        self.root.geometry("450x650")
        self.root.configure(bg="#2C2F33")

        self.label_titulo = ctk.CTkLabel(root, text="Escolha um esporte", font=('Helvetica', 24, 'bold'), text_color="#7289DA")
        self.label_titulo.pack(pady=20)

        self.botoes_jogos = []

        self.btn_futsal = ctk.CTkButton(root, text="Futsal", command=lambda: on_jogo_selected("Futsal"), font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        self.btn_futsal.pack(pady=5)

        self.btn_basquete = ctk.CTkButton(root, text="Basquete", command=lambda: on_jogo_selected("Basquete"), font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        self.btn_basquete.pack(pady=5)

        self.btn_volei = ctk.CTkButton(root, text="Vôlei", command=lambda: on_jogo_selected("Vôlei"), font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        self.btn_volei.pack(pady=5)

    def adicionar_botao_resultado(self, resultado_num, on_ver_resultados):
        btn_resultado = ctk.CTkButton(self.root, text=f"Resultado {resultado_num}", command=on_ver_resultados, font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        btn_resultado.pack(pady=5)
        self.botoes_jogos.append(btn_resultado)

class PaginaPlacar:
    def __init__(self, root, nome_jogo, on_finalizar_partida):
        self.root = root
        self.nome_jogo = nome_jogo
        self.on_finalizar_partida = on_finalizar_partida
        self.root.title(f"Placar de Pontos - {nome_jogo}")
        self.root.geometry("450x650")
        self.root.configure(bg="#2C2F33")

        self.resultado_num = None  # Número do resultado atual
        self.tempo_pausado = True
        self.pontos_azul = 0
        self.pontos_vermelho = 0

        # Configurações específicas para cada esporte
        if nome_jogo == "Futsal":
            self.tempos = 2
            self.tempo_partida = 1 * 6  # 10 minutos em segundos
            self.tempo_restante_no_periodo = self.tempo_partida
            self.periodo_atual = 1
        elif nome_jogo == "Basquete":
            self.tempos = 4
            self.tempo_partida = 1 * 6  # 10 minutos em segundos
            self.tempo_restante_no_periodo = self.tempo_partida
            self.periodo_atual = 1
        elif nome_jogo == "Vôlei":
            self.tempo_partida = None  # Sem cronômetro
            self.sets_azul = 0
            self.sets_vermelho = 0
            self.pontos_set_atual_azul = 0
            self.pontos_set_atual_vermelho = 0

        if nome_jogo in ["Futsal", "Basquete"]:
            self.label_tempo = ctk.CTkLabel(root, text=self.formatar_tempo(), font=('Digital-7 Mono', 48, 'bold'), text_color="#FF5555")
            self.label_tempo.pack(pady=10)
            self.btn_play_pause = ctk.CTkButton(root, text="Play", command=self.toggle_play_pause, font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
            self.btn_play_pause.pack(pady=5)
            self.atualizar_tempo()

        # Frame para organizar os times lado a lado
        self.frame_times = ctk.CTkFrame(root)
        self.frame_times.pack(pady=10, fill='x')

        # Frame do time azul
        self.frame_azul = ctk.CTkFrame(self.frame_times)
        self.frame_azul.pack(side='left', expand=True, fill='both', padx=10)

        self.label_azul = ctk.CTkLabel(self.frame_azul, text="Time Azul", font=('Helvetica', 20, 'bold'), text_color="#7289DA")
        self.label_azul.pack(pady=5)

        self.btn_add_azul = ctk.CTkButton(self.frame_azul, text="+ 1 Azul", command=lambda: self.add_ponto_azul(1), font=('Helvetica', 16, 'bold'), text_color="#7289DA")
        self.btn_add_azul.pack(pady=5)

        if nome_jogo == "Basquete":
            self.btn_add_azul_2 = ctk.CTkButton(self.frame_azul, text="+ 2 Azul", command=lambda: self.add_ponto_azul(2), font=('Helvetica', 16, 'bold'), text_color="#7289DA")
            self.btn_add_azul_2.pack(pady=5)

            self.btn_add_azul_3 = ctk.CTkButton(self.frame_azul, text="+ 3 Azul", command=lambda: self.add_ponto_azul(3), font=('Helvetica', 16, 'bold'), text_color="#7289DA")
            self.btn_add_azul_3.pack(pady=5)

        self.btn_remove_azul = ctk.CTkButton(self.frame_azul, text="- Azul", command=self.remove_ponto_azul, font=('Helvetica', 16, 'bold'), text_color="#7289DA")
        self.btn_remove_azul.pack(pady=5)

        # Frame do time vermelho
        self.frame_vermelho = ctk.CTkFrame(self.frame_times)
        self.frame_vermelho.pack(side='right', expand=True, fill='both', padx=10)

        self.label_vermelho = ctk.CTkLabel(self.frame_vermelho, text="Time Vermelho", font=('Helvetica', 20, 'bold'), text_color="#FF5555")
        self.label_vermelho.pack(pady=5)

        self.btn_add_vermelho = ctk.CTkButton(self.frame_vermelho, text="+ 1 Vermelho", command=lambda: self.add_ponto_vermelho(1), font=('Helvetica', 16, 'bold'), text_color="#FF5555")
        self.btn_add_vermelho.pack(pady=5)

        if nome_jogo == "Basquete":
            self.btn_add_vermelho_2 = ctk.CTkButton(self.frame_vermelho, text="+ 2 Vermelho", command=lambda: self.add_ponto_vermelho(2), font=('Helvetica', 16, 'bold'), text_color="#FF5555")
            self.btn_add_vermelho_2.pack(pady=5)

            self.btn_add_vermelho_3 = ctk.CTkButton(self.frame_vermelho, text="+ 3 Vermelho", command=lambda: self.add_ponto_vermelho(3), font=('Helvetica', 16, 'bold'), text_color="#FF5555")
            self.btn_add_vermelho_3.pack(pady=5)

        self.btn_remove_vermelho = ctk.CTkButton(self.frame_vermelho, text="- Vermelho", command=self.remove_ponto_vermelho, font=('Helvetica', 16, 'bold'), text_color="#FF5555")
        self.btn_remove_vermelho.pack(pady=5)

        # Placar de pontos corridos
        self.label_placar_pontos = ctk.CTkLabel(root, text="Pontos - Time Azul: 0 | Time Vermelho: 0", font=('Helvetica', 20, 'bold'), text_color="#7289DA")
        self.label_placar_pontos.pack(pady=10)

        if nome_jogo == "Vôlei":
            self.label_placar_sets = ctk.CTkLabel(root, text="Sets - Time Azul: 0 | Time Vermelho: 0", font=('Helvetica', 20, 'bold'), text_color="#7289DA")
            self.label_placar_sets.pack(pady=10)
            self.tempo_pausado = False  # Começar diretamente

        self.btn_finalizar_partida = ctk.CTkButton(root, text="Finalizar Partida", command=self.finalizar_partida, font=('Helvetica', 16, 'bold'), text_color="#99AAB5")
        self.btn_finalizar_partida.pack(pady=10)

        self.atualizar_placar()

    def formatar_tempo(self):
        if self.tempo_restante_no_periodo is not None:
            minutos = self.tempo_restante_no_periodo // 60
            segundos = self.tempo_restante_no_periodo % 60
            return f"{minutos:02}:{segundos:02}"
        return "00:00"

    def toggle_play_pause(self):
        self.tempo_pausado = not self.tempo_pausado
        self.btn_play_pause.configure(text="Pause" if not self.tempo_pausado else "Play")

    def add_ponto_azul(self, pontos):
        if self.nome_jogo == "Vôlei":
            self.pontos_set_atual_azul += pontos
            if self.pontos_set_atual_azul >= 25:
                self.sets_azul += 1
                self.pontos_set_atual_azul = 0
                self.pontos_set_atual_vermelho = 0
                if self.sets_azul == 3:
                    self.finalizar_partida()
        else:
            self.pontos_azul += pontos
        self.atualizar_placar()

    def remove_ponto_azul(self):
        if self.nome_jogo == "Vôlei" and self.pontos_set_atual_azul > 0:
            self.pontos_set_atual_azul -= 1
        elif self.pontos_azul > 0:
            self.pontos_azul -= 1
        self.atualizar_placar()

    def add_ponto_vermelho(self, pontos):
        if self.nome_jogo == "Vôlei":
            self.pontos_set_atual_vermelho += pontos
            if self.pontos_set_atual_vermelho >= 25:
                self.sets_vermelho += 1
                self.pontos_set_atual_azul = 0
                self.pontos_set_atual_vermelho = 0
                if self.sets_vermelho == 3:
                    self.finalizar_partida()
        else:
            self.pontos_vermelho += pontos
        self.atualizar_placar()

    def remove_ponto_vermelho(self):
        if self.nome_jogo == "Vôlei" and self.pontos_set_atual_vermelho > 0:
            self.pontos_set_atual_vermelho -= 1
        elif self.pontos_vermelho > 0:
            self.pontos_vermelho -= 1
        self.atualizar_placar()

    def atualizar_placar(self):
        if self.nome_jogo == "Vôlei":
            self.label_placar_pontos.configure(text=f"Pontos - Time Azul: {self.pontos_set_atual_azul} | Time Vermelho: {self.pontos_set_atual_vermelho}")
            self.label_placar_sets.configure(text=f"Sets - Time Azul: {self.sets_azul} | Time Vermelho: {self.sets_vermelho}")
        else:
            self.label_placar_pontos.configure(text=f"Pontos - Time Azul: {self.pontos_azul} | Time Vermelho: {self.pontos_vermelho}")

    def atualizar_tempo(self):
        if not self.tempo_pausado and self.tempo_partida is not None:
            if self.tempo_restante_no_periodo > 0:
                self.tempo_restante_no_periodo -= 1
                self.label_tempo.configure(text=self.formatar_tempo())
            else:
                self.tempo_restante_no_periodo = 0
                self.tempo_pausado = True
                self.btn_play_pause.configure(text="Play")
                if self.periodo_atual < self.tempos:
                    self.periodo_atual += 1
                    self.tempo_restante_no_periodo = self.tempo_partida
                else:
                    self.finalizar_partida()
        self.root.after(1000, self.atualizar_tempo)

    def finalizar_partida(self):
        global resultados
        if self.resultado_num is None:  # Se for o primeiro resultado
            self.resultado_num = len(resultados) + 1  # Incrementa o contador
        resultados.append({'nome_jogo': self.nome_jogo, 'azul': self.pontos_azul, 'vermelho': self.pontos_vermelho})
        salvar_resultados(resultados, self.resultado_num)  # Salva o resultado com o número correspondente
        self.root.destroy()  # Fecha a janela de placar

class PaginaResultados:
    def __init__(self, root, resultado):
        self.root = root
        self.root.title(f"Resultados - {resultado['nome_jogo']}")
        self.root.geometry("350x200")
        self.root.configure(bg="#2C2F33")

        self.label_titulo = ctk.CTkLabel(root, text=f"Resultados - {resultado['nome_jogo']}", font=('Helvetica', 24, 'bold'), text_color="#7289DA")
        self.label_titulo.pack(pady=20)

        ctk.CTkLabel(root, text=f"Time Azul: {resultado['azul']} | Time Vermelho: {resultado['vermelho']}", font=('Helvetica', 16, 'bold'), text_color="#99AAB5").pack(pady=5)

def salvar_resultados(resultados, num_resultado):
    with open(f"RESULTADO_{num_resultado}.txt", "w") as file:  # Salva o resultado com o número correspondente
        resultado = resultados[-1]  # Pega o último resultado
        file.write(f"Resultado {num_resultado}:\n")
        file.write(f"Jogo: {resultado['nome_jogo']}\n")
        file.write(f"Pontos Azul: {resultado['azul']}\n")
        file.write(f"Pontos Vermelho: {resultado['vermelho']}\n\n")

def selecionar_jogo(jogo):
    root_page.withdraw()
    root_placar = ctk.CTk()
    placar_app = PaginaPlacar(root_placar, jogo, 'finalizar_partida')
    root_placar.mainloop()

def ver_resultados(index):
    root_resultados = ctk.CTk()
    resultado = resultados[index]
    resultados_app = PaginaResultados(root_resultados, resultado)
    root_resultados.mainloop()

resultados = []
root_page = ctk.CTk()
pagina_jogos = PaginaJogos(root_page, selecionar_jogo)
root_page.mainloop()