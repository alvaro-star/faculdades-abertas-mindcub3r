#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait

ganho_extra = 21

class RoboGirador:
    def __init__(self, ev3_instance):
        self.ev3 = ev3_instance

        # Definindo motores
        self.motor_prancha = Motor(Port.B)
        self.motor_braco = Motor(Port.A)

        # Estado do braço: 'ABERTO', 'FECHADO', 'RETRAIDO'
        self.estado_braco = 'ABERTO'

    def retrair_braco(self):        
        if self.estado_braco == 'FECHADO':
            self.prim_girar_braco(90 + ganho_extra)
        elif self.estado_braco == 'ABERTO':
            self.prim_girar_braco(180 + ganho_extra)
        self.estado_braco = 'RETRAIDO'

    def abrir_braco(self):
        if self.estado_braco == 'FECHADO':
            self.prim_girar_braco(-90)
        elif self.estado_braco == 'RETRAIDO':
            self.prim_girar_braco(-(180 + ganho_extra))
        self.estado_braco = 'ABERTO'

    def fechar_braco(self):
        if self.estado_braco == 'ABERTO':
            self.prim_girar_braco(90)
        elif self.estado_braco == 'RETRAIDO':
            self.prim_girar_braco(-(90 + ganho_extra))
        self.estado_braco = 'FECHADO'

    def prim_girar_prancha(self, angulo, velocidade=800):
        """Gira a prancha no ângulo indicado (graus)."""
        fator_correcao = 3
        if fator_correcao < 0:
            fator_correcao = 3
        self.motor_prancha.run_angle(velocidade, angulo * fator_correcao, Stop.HOLD)
        wait(500)

    def prim_girar_braco(self, angulo, velocidade=150):
        """Gira o braço no ângulo indicado (graus)."""
        fator_correcao = 1.6
        if angulo < 0:
            fator_correcao = 1.25
        self.motor_braco.run_angle(fator_correcao * velocidade, angulo, Stop.HOLD)
        wait(500)

    def sec_girar_horizontal(self, sentido='+', disable_first_instruction=False):
        if not disable_first_instruction:
            self.abrir_braco()
        angulo = 90 if sentido == '+' else -90
        self.prim_girar_prancha(angulo)

    def sec_girar_vertical(self, sentido='+'):
        if sentido == '+':
            self.abrir_braco()
            self.fechar_braco()
            self.retrair_braco()
            self.fechar_braco()
        else:
            self.sec_girar_vertical()
            self.sec_girar_vertical()
            self.sec_girar_vertical()

    def sec_girar_peca(self, sentido='+'):
        self.fechar_braco()
        self.sec_girar_horizontal(sentido, disable_first_instruction=True)

    def printMessage(self, mensagem, tempo_ms=2000):
        """Mostra uma mensagem no display do EV3 e apaga após um tempo."""
        self.ev3.screen.clear()
        self.ev3.screen.draw_text(0, 50, mensagem)
        wait(tempo_ms)
        self.ev3.screen.clear()

    def ter_interpreter_sequence(self, movimentos):  
        """Interpreta uma sequência de movimentos no formato ['GH+', 'GV-', ...]"""
        list_movimentos_algoritm = []
        for item in movimentos:
            sinal = item[-1]
            movimento = item[:-1]
            list_movimentos_algoritm.append([movimento, sinal])

        print("Lista de moviemntos do interpretador")
        print(list_movimentos_algoritm)
        for comando in list_movimentos_algoritm:
            if comando[0] == "GH":
                self.sec_girar_horizontal(comando[1])
            elif comando[0] == "GV":
                self.sec_girar_vertical(comando[1])
            elif comando[0] == "GP":
                self.sec_girar_peca(comando[1])
            else:
                self.printMessage("Comando inválido: " + comando[0])

# Exemplo de uso
ev3 = EV3Brick()
robo = RoboGirador(ev3)

ev3.speaker.beep()

lista_movimentos = [
    'GV+', 'GP+', 'GH-', 'GV+', 'GH+', 'GH+', 'GP-', 'GH+', 'GV-', 'GH-', 'GV+', 'GH+', 'GP-', 'GH+', 'GP-'
]


robo.printMessage("Iniciando...", 2000)
print("Lista de movimento")
print(lista_movimentos)
robo.ter_interpreter_sequence(lista_movimentos)

lista_movimentos_invertida = [
    movimento[:-1] + ('-' if movimento[-1] == '+' else '+')
    for movimento in reversed(lista_movimentos)
]

print("Lista de movimento invertidas")
print(lista_movimentos_invertida)
robo.ter_interpreter_sequence(lista_movimentos_invertida)

robo.printMessage("Fim!", 2000)