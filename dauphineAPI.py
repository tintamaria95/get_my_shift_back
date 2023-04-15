import http.client
from urllib.parse import urlencode
from env import AuthID


def get_phpsessid(mail: str, password: str) -> str:
    conn = http.client.HTTPSConnection("sports.monportail.psl.eu")
    payload = urlencode({
        'login': mail,
        'password': password,
        'job': 'auth-user',
        'com': 'login'
    })
    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    conn.request("POST", "/pegasus/index.php", payload, headers)
    res = conn.getresponse()
    cookie = res.headers.get('set-cookie')\
        .split(';')[0]\
        .split('=')[1]
    return cookie


def get_shifts(phpsessid: str) -> list:
    conn = http.client.HTTPSConnection("sports.monportail.psl.eu")
    payload = ''
    headers = {
      'Cookie': f'PHPSESSID={phpsessid}'
    }
    url_shifts = (
        "/pegasus/index.php?com=courses_choices&job=get-cours&"
        "start=1600102594&end=1947171394")
    conn.request("GET", url_shifts, payload, headers)
    res = conn.getresponse()
    data = res.read()
    # print(data.decode("utf-8"))
    return eval(data.decode("utf-8"))


def get_user_formation(mail: str, password: str):
    token = get_phpsessid(mail, password)
    try:
        shifts = get_shifts(token)
        return shifts[0]['FORMATION_PERSONNALISEE']
    except ValueError:
        raise ('Invalid login')


def is_valid_login(mail: str, password: str) -> bool:
    try:
        get_user_formation(mail, password)
        return True
    except ValueError:
        return False


def register_or_unregister_to_shift(
        *,
        phpsessid: str,
        user_formation: str,
        course_program: str,
        session_course: str
) -> None:
    conn = http.client.HTTPSConnection("sports.monportail.psl.eu")
    headers = {
      'Cookie': f'PHPSESSID={phpsessid}',
      'Content-Type': 'application/x-www-form-urlencoded'
    }
    payload = urlencode({
        'COURS_PROGRAMME': course_program,
        'SESSION_COURSE': session_course,
        'FORMATION_PERSONNALISEE': user_formation
    })
    conn.request(
        "POST",
        "/pegasus/index.php?com=courses_choices&"
        "job=enregistrer-courses_choices", payload, headers)
    res = conn.getresponse()
    data = res.read()
    return data


mail, password = AuthID['mail'], AuthID['password']
user_formation = get_user_formation(mail, password)
print(user_formation)
phpsessid = get_phpsessid(mail, password)
print(phpsessid)
course_programme = (
    "MY1LCLIMBU220001    SPORT     .   2023-15     Samedi  08:0009:00")
sess_course = "2022MY1LCLIMBU          22010001"
data = register_or_unregister_to_shift(
    phpsessid=phpsessid,
    user_formation=user_formation,
    course_program=course_programme,
    session_course=sess_course
)
print(data)
