import os
from grid import Grid
from constraints import Constraints
from pysat_solver import PySATSolver
from brute_force_solver import BruteForceSolver
from backtracking_solver import BacktrackingSolver

# Hàm đọc ma trận từ file và trả về dưới dạng list of lists
def read_matrix_from_file(filepath):
    matrix = []
    with open(filepath, 'r') as file:
        for line in file:
            row = line.strip().split(',')
            row = [None if cell.strip() == '_' else (int(cell.strip()) if cell.strip().isdigit() else cell.strip()) for cell in row]
            matrix.append(row)
    return matrix

# Hàm ghi tất cả kết quả vào một file duy nhất
def write_all_solutions_to_file(filepath, solutions):
    with open(filepath, 'w') as file:
        for method, solution in solutions.items():
            file.write(f"Solution with {method}:\n")
            if solution is None:
                file.write("No solution found.\n")
            else:
                for row in solution:
                    line = ", ".join(str(cell) if cell is not None else "_" for cell in row)
                    file.write(line + "\n")
            file.write("\n")

# Hàm giải ma trận và hiển thị kết quả cùng với ghi file
def solve_matrix(grid_data, output_file):
    try:
        # Bước 1: Tạo đối tượng Grid từ dữ liệu ma trận
        print("\nInitial map")
        grid = Grid(grid_data)
        grid.print_grid()

        # Bước 2 & 3: Tạo các ràng buộc CNF (dùng cho PySAT và DPLL)
        print("\nGenerating CNF constraints...")
        constraints = Constraints(grid)
        cnf, var_map = constraints.generate_cnf()

        print("\nKết quả chạy thuật toán")
        solutions = {}  # Lưu trữ kết quả của từng phương pháp

        # Bước 4: Giải bằng PySAT
        print("\nSolving with PySAT...")
        pysat_solver = PySATSolver(grid, cnf, var_map)
        print("\nResult map")
        solved_pysat, time_pysat = pysat_solver.solve()
        pysat_solver.print_solution()
        solutions["PySAT"] = pysat_solver.solution
        print(f"Running time: {time_pysat:.5f} seconds")

        # Bước 5: Giải bằng Brute Force
        # print("\nSolving with Brute Force...")
        # brute_force_solver = BruteForceSolver(grid)
        # print("\nResult map")
        # solved_brute, time_brute = brute_force_solver.solve()
        # brute_force_solver.print_solution()
        # solutions["Brute Force"] = brute_force_solver.solution
        # print(f"Running time: {time_brute:.5f} seconds")
        
        
        # Bước 6: Giải bằng Backtracking
        print("\nSolving with Backtracking...")
        backtracking_solver = BacktrackingSolver(grid)
        print("\nResult map")
        solved_backtrack, time_backtrack = backtracking_solver.solve()
        backtracking_solver.print_solution()
        solutions["Backtracking"] = backtracking_solver.solution
        print(f"Running time: {time_backtrack:.5f} seconds")
     
        

        # Ghi tất cả kết quả vào file
        write_all_solutions_to_file(output_file, solutions)
        print(f"\nAll solutions written to {output_file}")

    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

# Hàm hiển thị menu để người dùng chọn file input
def display_menu():
    print("Chọn file input để giải:")
    for i in range(1, 4):
        print(f"{i}. input_{i}.txt")
    print("0. Thoát")
    choice = input("Nhập lựa chọn của bạn (0-3): ")
    return choice

# Hàm chính của chương trình
def main():
    # Kiểm tra sự tồn tại của các file input_i.txt
    input_files = [f"input_{i}.txt" for i in range(1, 4)]
    missing_files = [f for f in input_files if not os.path.exists(f)]
    if missing_files:
        print("Các file sau không tồn tại:", ", ".join(missing_files))
        print("Vui lòng tạo các file input_i.txt (i từ 1 đến 3) trước khi chạy chương trình.")
        return

    matrices = []
    for i_file in input_files:
        try:
            matrix = read_matrix_from_file(i_file)
            matrices.append(matrix)
            print(f"Đã đọc ma trận từ {i_file}")
        except Exception as e:
            print(f"Lỗi khi đọc file {i_file}: {e}")
            return

    while True:
        choice = display_menu()
        
        if choice == '0':
            print("Thoát chương trình.")
            break
        
        try:
            choice = int(choice)
            if 1 <= choice <= 6:
                input_file = f"input_{choice}.txt"
                output_file = f"output_{choice}.txt"
                print(f"\nĐang giải ma trận từ file {input_file}...")
                solve_matrix(matrices[choice-1], output_file)
            else:
                print("Lựa chọn không hợp lệ. Vui lòng chọn từ 0 đến 6.")
        except ValueError:
            print("Lựa chọn không hợp lệ. Vui lòng nhập một số.")

if __name__ == "__main__":
    main()