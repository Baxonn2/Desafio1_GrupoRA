class Action:
    cut = 0      #dimensión a cortar
    plank = 0    #tabla a la cual cortarle la dimensión 

    def __init__(self, plank, cut):
        self.cut = cut
        self.plank = plank

    def __str__(self):
        return f'cut: {self.cut} \t plank: {self.plank}'
