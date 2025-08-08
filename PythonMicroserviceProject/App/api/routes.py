from fastapi import APIRouter, Depends, Security
from App.controllers.math_controller import MathController
from App.auth.auth import verify_token

router = APIRouter(
    prefix="/api",
    tags=["default"],
    dependencies=[Depends(verify_token)]
)
@router.get("/pow")
def power(base: int, exponent: int):
    return MathController.handle_pow(base, exponent)

@router.get("/fib")
def fibonacci(n: int):
    return MathController.handle_fib(n)

@router.get("/fact")
def factorial(n: int):
    return MathController.handle_fact(n)
