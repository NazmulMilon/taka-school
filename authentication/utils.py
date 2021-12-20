import uuid


def random_hex_code(length: int = 16) -> str:
    """
        To create a new random hex code of dynamic length.

        :parameter
            length (int): set how many character of hex code will generate.
             Default is 16 character.

        :return
            random hex code with dynamic length.
    """
    return uuid.uuid4().hex[:length]


# For Chart

days = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14',
    '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
    '27', '28', '29', '30', '31'
]

hours = ['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00',
         '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00',
         '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00',
         '21:00', '22:00', '23:00']

minutes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11',
           '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22',
           '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
           '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44',
           '45', '46', '47', '48', '49', '50', '51', '52', '53', '54', '55',
           '56', '57', '58', '59', '60']

colorPrimary = 'rgba(54,162,235,0.2)'
colorPrimaryBorder = 'rgb(54,162,235)'
colorDanger = 'rgba(255,99,132,0.2)'
colorDangerBorder = 'rgb(255,99,132)'


def get_day_dict():
    day_dict = {}

    for day in days:
        day_dict[day] = 0

    return day_dict


def get_hour_dict():
    hour_dict = {}

    for hour in hours:
        hour_dict[hour] = 0

    return hour_dict


def get_minute_dict():
    minute_dict = {}

    for minute in minutes:
        minute_dict[minute] = 0

    return minute_dict
