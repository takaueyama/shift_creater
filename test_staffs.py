import random
from models import Staff

last_name_pool = ["佐藤", "山田", "朝倉", "斎藤", "渡辺", "堀口", "堀江", "浜辺", "湊", "宝鐘", "樋口", "白石", "小坂", "与田", "設楽"]
first_name_pool = ['太郎', '未来', '海', '裕', '祐介', '旬', '智也', 'ジョン', 'ジョニー', 'ニック', 'タイラー', '信之', '太子', '信長']

test_staffs = []
test_staff_id = 0

# テスト用のシフトを作成
# 夜勤が普通回数で、ポイントが1.0、5人
for i in range(5):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.2, False, 3, 20, 6, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 昨日が夜勤
for i in range(2):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.9, False, 1, 20, 6, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 夜勤が普通回数で、ポイントが0.7、5人
for i in range(5):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 3, 20, 6, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 昨日が夜勤
for i in range(1):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 1, 20, 6, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 夜勤が少な目で、ポイントが1.0、6人
for i in range(6):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, True, 3, 20, 3, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 夜勤なしで、ポイントが1.0、3人
for i in range(3):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 1.0, False, 3, 20, 0, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1

# 夜勤なしで、ポイントが0.7、2人
for i in range(2):
    staff = Staff(random.choice(last_name_pool), random.choice(first_name_pool), 0.7, False, 3, 20, 0, 0, test_staff_id)
    test_staffs.append(staff)
    test_staff_id += 1