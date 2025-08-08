from App.services.math_service import MathService

class MathController:

    @staticmethod
    def handle_pow(base, exponent):
        return MathService.process_operation("pow", [base, exponent])

    @staticmethod
    def handle_fib(n):
        return MathService.process_operation("fib", [n])

    @staticmethod
    def handle_fact(n):
        return MathService.process_operation("fact", [n])
