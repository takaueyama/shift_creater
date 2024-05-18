class Staff:
    def __init__(self, last_name, first_name, point, is_proper, last_day_shift_pattern,  max_shift_count, max_night_shift_count, current_shift_streak, id, current_off_day_count = 0, current_yuukyu_count = 0 ,current_night_shift_count = 0, current_day_shift_count = 0, current_shift_count = 0):
        # 個人識別
        self.id = id
        self.last_name = last_name
        self.first_name = first_name

        # 基本は不変のもの
        self.point = point
        self.is_proper = is_proper

        # シフトを作る度に設定するもの
        self.max_night_shift_count = max_night_shift_count
        self.max_shift_count = max_shift_count

        # 状態
        # 前日の勤務形態(日勤、夜勤、明け、休み)
        self.last_day_shift_pattern = last_day_shift_pattern
        # 今の連続勤務日数
        self.current_shift_streak = current_shift_streak
        # 今シフトのトータル休み日数
        self.current_off_day_count = current_off_day_count
        # 今シフトのトータル有給日数
        self.current_yuukyu_count = current_yuukyu_count
        # 今シフトのトータルの夜勤日数
        self.current_night_shift_count = current_night_shift_count
        # 今シフトのトータルの日勤日数
        self.current_day_shift_count = current_day_shift_count
        # 今シフトのトータル出勤日数
        self.current_shift_count = current_shift_count

    def __str__(self):
        return self.last_name + self.first_name

class ShiftDay:
    def __init__(self, day, day_point, night_point, day_people_count, night_people_count, id):
        # 日付
        self.day = day
        # 日勤に必要なポイント
        self.day_point = day_point
        # 夜勤に必要なポイント
        self.night_point = night_point
        # 日勤に必要な人数
        self.day_people_count = day_people_count
        # 夜勤に必要な人数
        self.night_people_count = night_people_count
        # 識別番号
        self.id = id

    def __str__(self):
        return str(self.day)