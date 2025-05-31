# Lớp Grid để quản lý ma trận và cung cấp các phương thức hỗ trợ
class Grid:
    # Hàm khởi tạo: Nhận dữ liệu ma trận và tính số hàng, số cột
    def __init__(self, grid_data):
        self.grid = grid_data  # Lưu ma trận
        self.rows = len(grid_data)  # Số hàng của ma trận
        self.cols = len(grid_data[0]) if self.rows > 0 else 0  # Số cột của ma trận

    # Hàm lấy giá trị ô tại vị trí (row, col)
    # Trả về None nếu vị trí ngoài phạm vi
    def get_cell(self, row, col):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return self.grid[row][col]
        return None

    # Hàm lấy danh sách các ô lân cận (bao gồm cả đường chéo) của ô (row, col)
    # Trả về danh sách các bộ (r, c, giá trị) của các ô lân cận
    def get_neighbors(self, row, col):
        neighbors = []  # Danh sách các ô lân cận
        for dr in range(-1, 2):  # Duyệt các hàng lân cận (-1, 0, 1)
            for dc in range(-1, 2):  # Duyệt các cột lân cận (-1, 0, 1)
                if dr == 0 and dc == 0:  # Bỏ qua chính ô (row, col)
                    continue
                r, c = row + dr, col + dc  # Tọa độ ô lân cận
                if 0 <= r < self.rows and 0 <= c < self.cols:  # Kiểm tra ô lân cận có trong ma trận không
                    neighbors.append((r, c, self.grid[r][c]))  # Thêm tọa độ và giá trị ô lân cận
        return neighbors

    # Hàm in ma trận ra console
    # Nếu không truyền grid, sử dụng self.grid
    def print_grid(self, grid=None):
        if grid is None:
            grid = self.grid  # Sử dụng ma trận mặc định nếu không truyền grid
        for row in grid:
            # In từng hàng, thay None bằng "_" và phân tách bằng ", "
            print(", ".join(str(cell) if cell is not None else "_" for cell in row))