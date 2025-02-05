from argparse import ArgumentParser, Namespace
from src.interfaces.baseui import BaseUI


class ConsoleUI(BaseUI):
    """Console UI"""
    def __init__(self) -> None:
        super().__init__()

        self.parser: ArgumentParser = ArgumentParser(
            description='Spellsolver',
            epilog="Word Finder for Discord Spellcast")

        self.parser.add_argument('game', type=str, default=None, nargs='?', help="gameboard string")
        self.parser.add_argument('--swap', type=int, required=False, help="enable swap mode", default=0)
        
        self.parser.add_argument('--x2', type=str, required=False, help="word multiplier", default="")
        self.parser.add_argument('--dl', type=str, required=False, help="double letter", default="")
        self.parser.add_argument('--tl', type=str, required=False, help="triple letter", default="")
        
        self.opt = self.parser.parse_args()
    
    def set_multipliers(self, mult_string: str, DL_string: str, TL_string: str) -> None:
        """Set values for multipliers"""
        if mult_string != "":
            mult_cord = (int(mult_string[0]), int(mult_string[1]))
            self.gameboard.set_mult_word(mult_cord)
        
        if DL_string != "":
            DL_cord = (int(DL_string[0]), int(DL_string[1]))
            self.gameboard.set_mult_letter(DL_cord, 2)
        
        if TL_string != "":
            TL_cord = (int(TL_string[0]), int(TL_string[1]))
            self.gameboard.set_mult_letter(TL_cord, 3)

    def mainargs(self, opt: Namespace) -> None:
        """Main loop of the Console UI using arguments"""
        self.load(opt.game)
        self.set_multipliers(opt.x2, opt.dl, opt.tl)
        results = self.solve(opt.swap)

        results.sorted(console=True)
    
    def maininput(self) -> None:
        """Main loop of the Console UI using inputs"""
        gameboard_string = input("Insert a gameboard: ")
        self.load(gameboard_string)

        mult_string = input("Insert 2x cord: ")
        DL_string = input("Insert DL cord: ")
        TL_string = input("Insert TL cord: ")
        self.set_multipliers(mult_string, DL_string, TL_string)

        swap = input("Use swap?: ")
        results = self.solve(swap)
        results.sorted(console=True)

    def mainloop(self) -> bool:
        """Main loop of the Console UI"""
        if self.opt.game:
            self.mainargs(self.opt)
            return False

        try:
            self.maininput()
        except Exception as e:
            print("Exception:", e)
        
        return True


if __name__ == "__main__":
    app = ConsoleUI()

    loop = True
    while(loop):
        loop = app.mainloop()
