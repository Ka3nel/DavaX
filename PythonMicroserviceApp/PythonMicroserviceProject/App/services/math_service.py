from math import pow, factorial
from App.db.database import SessionLocal, RequestRecord

class MathService:

    @staticmethod
    def process_operation(op, args):
        if op == "pow":
            result = pow(args[0], args[1])
        elif op == "fib":
            result = MathService._fib(args[0])
        elif op == "fact":
            result = factorial(args[0])
        else:
            raise ValueError("Invalid operation")

        db = SessionLocal()
        db_record = RequestRecord(operation=op, input=str(args), result=result)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        db.close()

        return {"operation": op, "input": args, "result": result}

    @staticmethod
    def _fib(n):
        a, b = 0, 1
        for _ in range(n):
            a, b = b, a + b
        return a
