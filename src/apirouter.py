from fastapi.responses import Response
from pydantic import BaseModel
from src.baseapi import BaseRouter
from src.baseui import BaseUI


class SolverData(BaseModel):
    """Data model for spellsolver_solve endpoint"""
    gameboard: str
    mult: tuple | None = None
    DL: tuple | None = None
    TL: tuple | None = None
    swap: bool | None = None

class SolverRouter(BaseRouter):
    """Represents a spellsolver fastapi router"""
    def __init__(self, app: BaseUI, **kwargs: dict):
        super().__init__(**kwargs)
        self.app: BaseUI = app

        @self.router.post("/solve")
        async def spellsolver_solve(data: SolverData) -> Response:
            """Endpoint that solve spellsolver game"""
            response = self.solve(data)

            if not response["successful"]:
                return self.error(response)
            return response
    
    def solve(self, data: SolverData) -> dict[str, object]:
        """Solve a spellsolver game"""
        try:
            self.app.load(data.gameboard)

            if data.mult:
                self.app.gameboard.set_mult_word(data.mult)
            if data.DL:
                self.app.gameboard.set_mult_letter(data.DL, 2)
            if data.TL:
                self.app.gameboard.set_mult_letter(data.TL, 3)
            
            results = self.app.solve(data.swap)
            response = {
                "elapsed": results.time,
                "words": results.sorted(api=True)
            }
            return {
                "successful": True, "message": "Spellsolver executed correctly", "data": response }
    
        except Exception as e:
            return { "successful": False, "message": "Spellsolver cannot be executed", "data": e }
