import Sofa.Core
import Sofa.constants.Key as Key


class ThreeInstrumentsController(Sofa.Core.Controller):

    def __init__(self, ir_controller):
        super().__init__()
        self.name = "ThreeInstrumentsController"

        # collegamento all'IRController presente nella scena
        self.ir = ir_controller

        # valori correnti
        self.selected = 0
        self.speed_step = 1.0     # mm per comando
        self.rot_step = 5.0       # gradi per comando
        self.current_rot = [0.0, 0.0, 0.0]

        print("[Controller] Ready. Keys: 0-1-2 select tube, arrows = extend/retract, A/D rotate.")

    def onKeypressedEvent(self, e):

        key = e["key"]

        # 1) Switch del tubo da comandare
        if key in ['0', ord('0')]:
            self.selected = 0
        if key in ['1', ord('1')]:
            self.selected = 1
        elif key in ['2', ord('2')]:
            self.selected = 2
        
        self.ir.controlledInstrument.value = self.selected

        # 2) Movimento avanti/indietro
        if key == Key.uparrow:
            self.ir.speed.value =  self.speed_step
        elif key == Key.downarrow:
            self.ir.speed.value = -self.speed_step
        else:
            # se non premi flecce → niente avanzamento
            self.ir.speed.value = 0.0

        # 3) Rotazione del tubo attivo
        if key == Key.leftarrow:
            self.current_rot[0] += self.rot_step
        elif key == Key.rightarrow:
            self.current_rot[0] -= self.rot_step

        self.ir.rotationInstrument.value = [self.current_rot[0], self.current_rot[1], self.current_rot[2]]
