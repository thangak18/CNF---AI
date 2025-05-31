from itertools import combinations
from pysat.formula import CNF

# Lớp Constraints để tạo các ràng buộc logic dưới dạng CNF (Conjunctive Normal Form)
class Constraints:
    # Hàm khởi tạo: Nhận ma trận và khởi tạo các thuộc tính
    def __init__(self, grid):
        self.grid = grid  # Lưu ma trận
        self.rows = grid.rows  # Số hàng của ma trận
        self.cols = grid.cols  # Số cột của ma trận
        self.cnf = CNF()  # Khởi tạo đối tượng CNF để lưu các mệnh đề
        self.var_map = {}  # Bản đồ ánh xạ (row, col) -> số biến
        self.next_var = 1  # Số biến tiếp theo sẽ được gán

    # Hàm gán biến cho các ô chưa được điền sẵn
    # Các ô đã điền sẵn (T, G, hoặc số) sẽ không được gán biến
    def assign_variables(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.get_cell(r, c)
                if cell is None:  # Chỉ gán biến cho ô trống
                    self.var_map[(r, c)] = r * self.cols + c + 1
                else:
                    self.var_map[(r, c)] = None

    # Hàm thêm các ràng buộc cho các ô đã được điền sẵn (T: bẫy, G: ngọc)
    def add_pre_assigned(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.get_cell(r, c)
                var = self.var_map.get((r, c))
                if cell == 'T' and var is not None:
                    self.cnf.append([var])  # True nghĩa là Trap (T)
                elif cell == 'G' and var is not None:
                    self.cnf.append([-var])  # False nghĩa là Gem (G)

    # Hàm thêm các ràng buộc cho các ô chứa số
    def add_number_constraints(self):
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid.get_cell(r, c)
                if isinstance(cell, int):  # Nếu ô chứa số
                    neighbors = self.grid.get_neighbors(r, c)  # Lấy các ô lân cận
                    unknown_neighbors = [(nr, nc) for nr, nc, val in neighbors if val is None]  # Các ô lân cận trống
                    n = len(unknown_neighbors)  # Số ô lân cận trống
                    k = cell - sum(1 for nr, nc, val in neighbors if val == 'T')  # Số bẫy cần đặt

                    # Kiểm tra k có hợp lệ không
                    if k < 0:  # Quá nhiều bẫy, không có giải pháp
                        print(f"Ma trận không có giải pháp: Ô ({r}, {c}) yêu cầu {cell} bẫy nhưng đã có quá nhiều bẫy lân cận.")
                        return False
                    if k > n:  # Không đủ ô trống để đặt bẫy, không có giải pháp
                        print(f"Ma trận không có giải pháp: Ô ({r}, {c}) yêu cầu {k} bẫy nhưng chỉ có {n} ô lân cận trống.")
                        return False

                    # Trường hợp đặc biệt: k = 0 (tất cả ô lân cận trống phải là G)
                    if k == 0:
                        for nr, nc in unknown_neighbors:
                            var = self.var_map.get((nr, nc))
                            if var is not None:
                                self.cnf.append([-var])  # False nghĩa là ngọc (G)
                        continue
                    # Trường hợp đặc biệt: k = n (tất cả ô lân cận trống phải là T)
                    if k == n:
                        for nr, nc in unknown_neighbors:
                            var = self.var_map.get((nr, nc))
                            if var is not None:
                                self.cnf.append([var])  # True nghĩa là bẫy (T)
                        continue

                    # Ràng buộc U(k, n): Trong bất kỳ k+1 ô nào, ít nhất một ô không phải bẫy
                    for subset in combinations(unknown_neighbors, k + 1):
                        clause = [-self.var_map[(x, y)] for x, y in subset if self.var_map.get((x, y)) is not None]
                        if clause:  # Chỉ thêm nếu mệnh đề không rỗng
                            self.cnf.append(clause)

                    # Ràng buộc L(k, n): Trong bất kỳ n-k+1 ô nào, ít nhất một ô phải là bẫy
                    for subset in combinations(unknown_neighbors, n - k + 1):
                        clause = [self.var_map[(x, y)] for x, y in subset if self.var_map.get((x, y)) is not None]
                        if clause:  # Chỉ thêm nếu mệnh đề không rỗng
                            self.cnf.append(clause)
        return True

    # Hàm tạo và trả về danh sách các mệnh đề CNF cùng bản đồ biến
    def generate_cnf(self):
        self.assign_variables()  # Gán biến
        self.add_pre_assigned()  # Thêm ràng buộc cho các ô đã điền sẵn
        result = self.add_number_constraints()  # Thêm ràng buộc cho các ô số
        if result is False:
            print("No solution possible due to invalid constraints.")
            return [], self.var_map  # Trả về danh sách rỗng nếu không có giải pháp
        return self.cnf.clauses, self.var_map  # Trả về các mệnh đề CNF và bản đồ biến