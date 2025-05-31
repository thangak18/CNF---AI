import time
from pysat.solvers import Glucose3

class PySATSolver:
    def __init__(self, grid, cnf, var_map):
        self.grid = grid
        self.cnf = cnf
        self.var_map = var_map
        self.solution = None

    def solve(self):
        start = time.time()

        solver = Glucose3()

        # Thêm tất cả các mệnh đề CNF vào solver
        for clause in self.cnf:
            solver.add_clause(clause)

        # Nếu CNF rỗng, trả về False (không có giải pháp cụ thể)
        if not self.cnf:
            print("CNF is empty, no specific solution can be determined.")
            end = time.perf_counter()
            return False, end - start

        # Giải bài toán
        solved = solver.solve()
        if solved:
            model = solver.get_model()
            self.solution = [row.copy() for row in self.grid.grid]
            for r in range(self.grid.rows):
                for c in range(self.grid.cols):
                    if self.solution[r][c] is None:
                        var = self.var_map.get((r, c))  # Lấy biến từ var_map
                        if var is None:
                            continue
                        # Kiểm tra giá trị của biến trong model
                        if var in model and model[var - 1] > 0:  # Biến là True
                            self.solution[r][c] = 'T'
                        else:  # Biến là False
                            self.solution[r][c] = 'G'

        end = time.time()
        running_time = end - start
        return solved, running_time

    def print_solution(self):
        if self.solution is None:
            print("No solution found with PySAT.")
            return
        self.grid.print_grid(self.solution)