from app.utils.db_api.quick_commands.quick_commands_timetable import add_couple

couple_text = '''
<b>Пара №{couple_number}</b>:
    <b>Предмет</b>:  {name_couple}
    <b>Начало - Конец</b>:   {time_start}  -  {time_end}
    <b>Перерыв</b>:  {time_break}  минут
'''

classes = {
    "Пара 1": 1,
    "Пара 2": 2,
    "Пара 3": 3,
    "Пара 4": 4,
    "Пара 5": 5,
    "Пара 6": 6,
}

reverse_classes = {
    1: "Пара 1",
    2: "Пара 2",
    3: "Пара 3",
    4: "Пара 4",
    5: "Пара 5",
    6: "Пара 6",
}

days = {
    "mon": "Понедельник",
    "tue": "Вторник",
    "wed": "Среда",
    "thu": "Четверг",
    "fri": "Пятница",
    "sat": "Суббота",
}

statuses_of_the_week = {
    "Четная": "even",
    "Нечетная": "odd",
    "Неизменяется": "not_change"
}

reverse_statuses = {
    "even": "Четная",
    "odd": "Нечетная",
    "not_change": "Неизменяется"
}


async def set_timetable():
    for day in days:
        await add_couple(couple_ui=f"{day}1", time_start="8:00", time_end="9:25", time_break="15")
        await add_couple(couple_ui=f"{day}2", time_start="9:40", time_end="11:05", time_break="30")
        await add_couple(couple_ui=f"{day}3", time_start="11:35", time_end="13:00", time_break="45")
        await add_couple(couple_ui=f"{day}4", time_start="13:45", time_end="15:10", time_break="30")
        await add_couple(couple_ui=f"{day}5", time_start="15:40", time_end="17:05", time_break="15")
        await add_couple(couple_ui=f"{day}6", time_start="17:20", time_end="18:45", time_break="Конец пар")
