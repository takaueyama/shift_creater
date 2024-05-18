import jpholiday
import datetime
import random
import numpy as np
from models import ShiftDay, Staff

AKE = 0
YAKIN = 1
NIKKINN = 2
YASUMI = 3

def prepare_shift_days(start_date, end_date, normal_day_point=6, normal_night_point=2.4, holiday_day_point=1.7, holiday_night_point=2.4, normal_day_people_count=13, normal_night_people_count=3, holiday_day_people_count=2, holiday_night_people_count=3):
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

def calculate_shift(shift_days, staffs):
    # shift = dict()
    ans = np.empty((len(shift_days), len(staffs)))
    
    for shift_day in shift_days:
        # 日勤のスタッフプール
        nikkinn_pool = []

        # 夜勤のポイントが1以上のスタッフプール
        yakin_upper_1 = []

        # 夜勤のポイントが1未満のスタッフプール
        yakin_under_1 = []

        # 日勤に割り当たった人
        nikkin = []

        # 夜勤に割り当たった人
        yakin = []

        # 明けに割り当たった人
        ake = []

        # 休みに割り当たった人
        yasumi = []

        # 明けのシフトを確定させる
        for staff in staffs:
            if staff.last_day_shift_pattern == YAKIN:
                ake.append(staff)

        # スタッフの条件によってスタッフのプールを作る
        for staff in staffs:
            # 休まないといけないパターン(昨日までで6連勤 or 昨日が夜勤 or トータルの出勤日数に達している)
            if staff.current_shift_streak >= 6 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count:
                continue
            # 昨日が明けではなかった場合
            if staff.last_day_shift_pattern != AKE:
                nikkinn_pool.append(staff)

        # 日勤のシフトを確定させる
        nikkin_success = False
        for i in range(10000):
            nikkin = random.sample(nikkinn_pool, shift_day.day_people_count)
            nikkin_point = 0

            for nikkin_staff in nikkin:
                nikkin_point += nikkin_staff.point

            if nikkin_point >= shift_day.day_point:
                nikkin_success = True
                break

        if not nikkin_success:
            for i in range(10000):
                nikkin = random.sample(nikkinn_pool, shift_day.day_people_count + 1)
                nikkin_point = 0

                for nikkin_staff in nikkin:
                    nikkin_point += nikkin_staff.point

                if nikkin_point >= shift_day.day_point:
                    nikkin_success = True
                    break

        if not nikkin_success:
            for i in range(10000):
                nikkin = random.sample(nikkinn_pool, shift_day.day_people_count + 2)
                nikkin_point = 0

                for nikkin_staff in nikkin:
                    nikkin_point += nikkin_staff.point

                if nikkin_point >= shift_day.day_point:
                    nikkin_success = True
                    break

        # 夜勤のシフトを確定させる
        for staff in staffs:
            # 昨日までで5連勤 or 昨日が夜勤 or トータルの出勤日数に達しているのを除外する
            if staff.current_shift_streak >= 5 or staff.last_day_shift_pattern == YAKIN or staff.current_shift_count >= staff.max_shift_count or (staff.current_shift_count + 1 >= staff.max_shift_count and shift_day.id + 1 != len(shift_days)) or staff in nikkin:
                continue
            # 一か月に取りうる夜勤の最大数に達していないスタッフをプールに入れる
            if staff.current_night_shift_count < staff.max_night_shift_count:
                if staff.point >= 1:
                    yakin_upper_1.append(staff)
                else:
                    yakin_under_1.append(staff)

        yakin_success = False

        # 日勤でシフト確定した人を夜勤に入れないようにする
        for key, yakin_upper_1_staff in enumerate(yakin_upper_1):
            if yakin_upper_1_staff in nikkin:
                del yakin_upper_1[key]
        
        for key, yakin_under_1_staff in enumerate(yakin_under_1):
            if yakin_under_1_staff in nikkin:
                del yakin_under_1[key]

        # デバッグ用
        # print('あっぱー１：', end='')
        # for staff in yakin_upper_1:
        #     print(staff.id, end='')
        # print('\n')
        # print('あんだー１：', end='')
        # for staff in yakin_under_1:
        #     print(staff.id, end='')
        # print('\n')

        # 夜勤を確定させる
        # 夜勤の決め方パターン１ここから
        for i in range(100):
            # for staff in yakin_upper_1:
            #     print('あっぱー' + str(staff.id) + '長さ' + str(len(yakin_upper_1)))
            # for staff in yakin_under_1:
            #     print('あんだー' + str(staff.id)+ '長さ' + str(len(yakin_under_1)))
            try:
                yakin = random.sample(yakin_upper_1, 1) + random.sample(yakin_under_1, shift_day.night_people_count-1)
            except:
                continue

            yakin_point = 0

            for yakin_staff in yakin:
                yakin_point += yakin_staff.point

            if yakin_point >= shift_day.night_point:
                yakin_success = True
                break
        
        if not yakin_success:
            for i in range(100):
                try:
                    yakin = random.sample(yakin_upper_1, 2) + random.sample(yakin_under_1, shift_day.night_people_count-2)
                except:
                    continue
                yakin_point = 0

                for yakin_staff in yakin:
                    yakin_point += yakin_staff.point

                if yakin_point >= shift_day.night_point:
                    yakin_success = True
                    break

        if not yakin_success:
            for i in range(100):
                try:
                    yakin = random.sample(yakin_upper_1, 3) + random.sample(yakin_under_1, shift_day.night_people_count-3)
                except:
                    continue
                yakin_point = 0

                for yakin_staff in yakin:
                    yakin_point += yakin_staff.point

                if yakin_point >= shift_day.night_point:
                    yakin_success = True
                    break
        # 夜勤の決め方パターン１ここまで
                
        # 休みのシフトを確定させる
        for staff in staffs:
            if staff in yakin or staff in nikkin or staff in ake:
                continue
            else:
                yasumi.append(staff)

        # 夜勤か日勤が確定できていなかったら例外を発生させる
        if not yakin_success or not nikkin_success:
            print(yakin_success, nikkin_success)
            raise Exception
        
        # シフト表に記録する
        # パターン1
        # shift[shift_day] = [nikkin, yakin, ake, yasumi]

        # パターン2
        for staff in nikkin:
            ans[shift_day.id][staff.id] = NIKKINN
        for staff in yakin:
            ans[shift_day.id][staff.id] = YAKIN
        for staff in ake:
            ans[shift_day.id][staff.id] = AKE
        for staff in yasumi:
            ans[shift_day.id][staff.id] = YASUMI

        # スタッフの情報更新
        for staff in staffs:
            # 明けに割り当たった場合
            if staff in ake:
                staff.last_day_shift_pattern = AKE
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
            # 日勤に割り当たった場合
            elif staff in nikkin:
                staff.last_day_shift_pattern = NIKKINN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_day_shift_count += 1
            # 夜勤に割り当たった場合
            elif staff in yakin:
                staff.last_day_shift_pattern = YAKIN
                staff.current_shift_streak += 1
                staff.current_shift_count += 1
                staff.current_night_shift_count += 1
            else:
                staff.last_day_shift_pattern = YASUMI
                staff.current_shift_streak = 0
                staff.current_off_day_count += 1
    # return shift
    return ans

def shift_pattern_counter(shift, staff):
    syukkin_days = 0
    nikkin_days = 0
    ake_days = 0
    yakin_days = 0
    yasumii_days = 0

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
    
    return (ake_days, yakin_days, nikkin_days, yasumii_days, syukkin_days)
