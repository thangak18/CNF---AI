import time
import itertools

# Lớp BruteForceSolver để giải bài toán bằng phương pháp vét cạn (brute force)
class BruteForceSolver:
    # Hàm khởi tạo: Chỉ nhận ma trận
    def __init__(self, grid):
        self.grid = grid  # Lưu ma trận
        self.solution = None  # Lưu ma trận kết quả (ban đầu là None)

    # Hàm giải bài toán bằng phương pháp vét cạn
    def solve(self):
        start = time.process_time()  # Ghi lại thời gian bắt đầu
        
        # Lấy danh sách các ô trống
        unknown_cells = [(r, c) for r in range(self.grid.rows) for c in range(self.grid.cols) if self.grid.get_cell(r, c) is None]
        # Thử tất cả tổ hợp T/G cho các ô trống
        for combination in itertools.product(['T', 'G'], repeat=len(unknown_cells)):
            new_grid = [row.copy() for row in self.grid.grid]
            for (r, c), value in zip(unknown_cells, combination):
                new_grid[r][c] = value
            if self.check_grid(new_grid):
                self.solution = new_grid
                break
        
        end = time.process_time()  # Ghi lại thời gian kết thúc
        running_time = end - start  # Tính thời gian chạy
        solved = self.solution is not None
        return solved, running_time

    # Hàm kiểm tra tính hợp lệ của ma trận
    def check_grid(self, grid):
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.get_cell(r, c)
                if isinstance(cell, int):
                    neighbors = self.grid.get_neighbors(r, c)
                    count = sum(1 for nr, nc, val in neighbors if grid[nr][nc] == 'T' or val == 'T')
                    if count != cell:
                        return False
        return True

    # Hàm in ma trận kết quả ra console
    def print_solution(self):
        if self.solution is None:
            print("No solution found with Brute Force.")
            return
        self.grid.print_grid(self.solution)