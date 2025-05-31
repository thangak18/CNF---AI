import time

# Lớp BacktrackingSolver để giải bài toán bằng phương pháp quay lui (backtracking)
class BacktrackingSolver:
    # Hàm khởi tạo: Chỉ nhận ma trận
    def __init__(self, grid):
        self.grid = grid  # Lưu ma trận
        self.solution = None  # Lưu ma trận kết quả (ban đầu là None)

    # Hàm giải bài toán bằng phương pháp quay lui
    def solve(self):
        start = time.time()  # Ghi lại thời gian bắt đầu
        
        # Tạo bản sao của ma trận để chỉnh sửa
        working_grid = [row.copy() for row in self.grid.grid]
        self.solution = self.backtrack(working_grid)
        
        end = time.time()  # Ghi lại thời gian kết thúc
        running_time = end - start  # Tính thời gian chạy
        solved = self.solution is not None
        return solved, running_time

    # Hàm quay lui: Gán giá trị cho từng ô và quay lui nếu cần
    def backtrack(self, grid, i=0, j=0):
        height = self.grid.rows
        width = self.grid.cols

        if i == height:
            if self.check_grid(grid):
                return grid
            return None

        next_i, next_j = (i, j + 1) if j + 1 < width else (i + 1, 0)

        if grid[i][j] is not None:
            return self.backtrack(grid, next_i, next_j)

        for value in ['T', 'G']:
            grid[i][j] = value
            if self.is_partial_grid_valid(grid, i, j):
                result = self.backtrack(grid, next_i, next_j)
                if result is not None:
                    return result
            grid[i][j] = None
        return None

    # Hàm kiểm tra tính hợp lệ của ma trận từng phần tại vị trí (i, j)
    def is_partial_grid_valid(self, grid, i, j):
        for r in range(self.grid.rows):
            for c in range(self.grid.cols):
                cell = self.grid.get_cell(r, c)
                if isinstance(cell, int):
                    neighbors = self.grid.get_neighbors(r, c)
                    if any(nr == i and nc == j for nr, nc, _ in neighbors):
                        count = sum(1 for nr, nc, val in neighbors if grid[nr][nc] == 'T' or val == 'T')
                        unknown = sum(1 for nr, nc, val in neighbors if grid[nr][nc] is None and val is None)
                        max_traps = count + unknown
                        min_traps = count
                        if cell < min_traps or cell > max_traps:
                            return False
        return True

    # Hàm kiểm tra tính hợp lệ của ma trận hoàn chỉnh
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
            print("No solution found with Backtracking.")
            return
        self.grid.print_grid(self.solution)