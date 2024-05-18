import jpholiday
import datetime
import random
from models import ShiftDay, Staff
import copy

AKE = 0
YAKIN = 1
NIKKINN = 2
YASUMI = 3
YUUKYU = 4

def prepare_shift_days(start_date, end_date, normal_day_point=8.5, normal_night_point=2.4, holiday_day_point=1.8, holiday_night_point=2.4, normal_day_people_count=13, normal_night_people_count=3, holiday_day_people_count=2, holiday_night_people_count=3):
    # シフトデイの集合
    shift_days = []
    start_date = start_date
    end_date = end_date
    current_date = start_date
    shift_id = 0

    while True:
        # 休日祝日の場合
        if current_date.weekday() >= 5 or jpholiday.is_holiday(current_date):
            shift_day = ShiftDay(current_date, holiday_day_point, holiday_night_point, holiday_day_people_count, holiday_night_people_count, shift_id)
            shift_days.append(shift_day)
        # 平日の処理
        else:
            shift_day = ShiftDay(current_date, normal_day_point, normal_night_point, normal_day_people_count, normal_night_people_count, shift_id)
            shift_days.append(shift_day)

        if current_date == end_date:
            break

        current_date = current_date + datetime.timedelta(days=1)
        shift_id += 1

    return shift_days

def calculate_shift(shift_days, staffs, req_shift):
    original_staffs = staffs
    staffs = copy.deepcopy(original_staffs)

    # ans[datetime][staff]でシフトパターンが取り出せる二次元配列
    ans = [[-1 for _ in range(len(staffs))] for _ in range(len(shift_days))]

    # 最終的にシフト作成が成功したかどうか
    shift_days_success = True

    for shift_day in shift_days:
        # 日勤候補のスタッフ
        nikkinn_pool = []

        # 夜勤候補のスタッフ
        yakin_pool = []

        # 日勤確定のスタッフ
        nikkin = []

        # 夜勤確定のスタッフ
        yakin = []

        # 明け確定のスタッフ
        ake = []

        # 休み確定のスタッフ
        yasumi = []

        # 有給確定のスタッフ
        yuukyu = []

        nikkin_success = False
        yakin_success = False

        # 明けのシフトを確定させる
        for staff in staffs:
            # 昨日のシフトターンが夜勤の場合
            if staff.last_day_shift_pattern == YAKIN:
                ake.append(staff)

        # 夜勤プールをつくる
        for staff in staffs:
            # 最終日のパターン
            if shift_day.id + 1 == len(shift_days):
                # 昨日までで五連勤、トータルの出勤日数に達している、昨日が夜勤を除く)
                if staff.current_shift_streak >= 6 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count or staff.max_night_shift_count - staff.current_night_shift_count <= 0:
                    continue
            # 最終日じゃないパターン
            else:
                if staff.current_shift_streak >= 5 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count + 1 >= staff.max_shift_count or staff.max_night_shift_count - staff.current_night_shift_count <= 0:
                    continue
            # 夜勤がいけるシフト希望を判定する
            # 最終日の場合
            if shift_day.id + 1 == len(shift_days):
                if req_shift[shift_day.id][staff.id] & 2 ** YAKIN:
                    yakin_pool.append(staff)
            # 最終日じゃない場合
            else:
                if req_shift[shift_day.id][staff.id] & 2 ** YAKIN and req_shift[shift_day.id + 1][staff.id] & 2 ** AKE:
                    yakin_pool.append(staff)

        # 夜勤のシフトを確定させる
        for i in range(100):
            try:
                yakin = random.sample(yakin_pool, shift_day.night_people_count)
            except ValueError:
                break

            yakin_point = 0

            for yakin_staff in yakin:
                yakin_point += yakin_staff.point

            if yakin_point >= shift_day.night_point:
                yakin_success = True
                break

        # 日勤のプールを作成する　
        for staff in staffs:
            # 休まないといけないパターン(昨日までで6連勤 or 昨日が夜勤 or トータルの出勤日数に達している or 昨日が明け or 夜勤でシフトが確定している)
            if staff.current_shift_streak >= 6 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count or staff.last_day_shift_pattern == AKE or staff in yakin:
                continue
            else:
                # 日勤がいけるシフト希望かを判定する
                if req_shift[shift_day.id][staff.id] & 2 ** NIKKINN:
                    nikkinn_pool.append(staff)

        # 日勤を確定させる
        for i in range(100):
            try:
                nikkin = random.sample(nikkinn_pool, shift_day.day_people_count)
            except ValueError:
                break

            nikkin_point = 0

            for nikkin_staff in nikkin:
                nikkin_point += nikkin_staff.point

            if nikkin_point >= shift_day.day_point:
                nikkin_success = True
                break

        # 有休を確定させる
        for staff in staffs:
            # 夜勤、日勤、明けで確定していないかつシフト希望が有給のみ可になっている
            if staff not in yakin and staff not in nikkin and staff not in ake and req_shift[shift_day.id][staff.id] == 2 ** YUUKYU:
                yuukyu.append(staff)    

        # 休みを確定させる
        for staff in staffs:
            # 夜勤、日勤、明け、有給で確定していないかつシフト希望が休み可になっている
            if staff not in yakin and staff not in nikkin and staff not in ake and staff not in yuukyu:
                yasumi.append(staff)
        
        # 日勤か夜勤が確定できていなかったら、シフト作成失敗とする
        if not yakin_success or not nikkin_success:
            shift_days_success = False
            break

        # ansに情報を入れる
        for staff in nikkin:
            ans[shift_day.id][staff.id] = NIKKINN
        for staff in yakin:
            ans[shift_day.id][staff.id] = YAKIN
        for staff in ake:
            ans[shift_day.id][staff.id] = AKE
        for staff in yasumi:
            ans[shift_day.id][staff.id] = YASUMI
        for staff in yuukyu:
            ans[shift_day.id][staff.id] = YUUKYU

        # スタッフの情報更新
        for staff in staffs:
            # 明けのシフトになった場合
            if staff in ake:
                staff.last_day_shift_pattern = AKE
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
            # 日勤のシフトになった場合
            elif staff in nikkin:
                staff.last_day_shift_pattern = NIKKINN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_day_shift_count += 1
            # 夜勤のシフトになった場合
            elif staff in yakin:
                staff.last_day_shift_pattern = YAKIN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_night_shift_count += 1
            # 有給のシフトになった場合
            elif staff in yuukyu:
                staff.last_day_shift_pattern = YUUKYU
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_yuukyu_count += 1
            # 休みのシフトになった場合
            elif staff in yasumi:
                staff.last_day_shift_pattern = YASUMI
                staff.current_shift_streak = 0
                staff.current_off_day_count += 1
    if shift_days_success:
        return ans
    else:
        raise Exception

# 作った時の気持ちが分からん関数、あとで直す
def shift_pattern_counter(shift, staff):
    syukkin_days = 0
    nikkin_days = 0
    ake_days = 0
    yakin_days = 0
    yasumii_days = 0
    yuukyu_days = 0

    for shift_day in shift:
        if shift_day[staff.id] == YAKIN:
            syukkin_days += 1
            yakin_days += 1
        if shift_day[staff.id] == AKE:
            syukkin_days += 1
            ake_days += 1
        if shift_day[staff.id] == NIKKINN:
            syukkin_days += 1
            nikkin_days += 1
        if shift_day[staff.id] == YASUMI:
            yasumii_days += 1
        if shift_day[staff.id] == YUUKYU:
            yuukyu_days += 1
    
    return (ake_days, yakin_days, nikkin_days, yasumii_days, yuukyu_days, syukkin_days)

# シフトとスタッフを引数にとって、そのシフトで7連勤以上がないかを判定する関数
def is_shift_valid(shift, staffs):
    # 働きタイプ
    hataraki_type = (NIKKINN, YAKIN, AKE)

    # 休みタイプ
    yasumi_type = (YASUMI, YUUKYU)

    for j in range(len(shift[0])):
        staff = staffs[j]
        shift_streak = staff.current_shift_streak

        for i in range(len(shift)):
            # 連勤が増える勤務(日勤、夜勤、明け)
            if shift[i][j] in hataraki_type:
                shift_streak += 1

                if shift_streak >= 7:
                    print(staff.id)
                    return False
                
            # 連勤がリセットされる勤務(休み、有給)
            elif shift[i][j] in yasumi_type:
                shift_streak = 0
    return True

# シフトとスタッフを引数にとって、トータル勤務日数の帳尻をあわせたシフトを返す関数
def caluculate_complete_shift(shift, staff):
    pass
        