from flask import Flask, render_template, request
import string
import datetime
from itertools import product

app = Flask(__name__)


class Base36DateTime:
    def __init__(self):
        self.base36Lsit: str = string.digits + string.ascii_uppercase

    def y_formula(self, x: int, y: int, z: int) -> int:
        return x * 1296 + (y * 36) + z * 1

    def md_formula(self, x: int, y: int) -> int:
        return x * 36 + y * 1

    def year_to_base36(self, Y: int) -> str:
        for xyz in product(range(0, 36), range(0, 36), range(0, 36)):
            if self.y_formula(*xyz) == Y:
                return f"{self.base36Lsit[xyz[0]]}{self.base36Lsit[xyz[1]]}{self.base36Lsit[xyz[2]]}"

    def solar_day_to_base36(self, solar_day: int) -> str:
        for xy in product(range(0, 36), range(0, 36)):
            if self.md_formula(*xy) == solar_day:
                return f"{self.base36Lsit[xy[0]]}{self.base36Lsit[xy[1]]}"

    def encoding_dateTime(self, YMD: str) -> str:
        _YMD = datetime.datetime.strptime(YMD, "%Y-%m-%d")
        _Y = int(_YMD.year)
        _solar_day = int(_YMD.strftime("%j"))
        return self.solar_day_to_base36(_solar_day) + self.year_to_base36(_Y)

    def decoding_base36(self, base36code: str) -> str:
        dedata = [self.base36Lsit.index(n) for n in list(base36code)]
        _solar_day = self.md_formula(dedata[0], dedata[1])
        _Y = self.y_formula(dedata[2], dedata[3], dedata[4])

        return datetime.datetime.strptime(f"{_Y} {_solar_day}", "%Y %j").strftime("%Y-%m-%d")


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/base36transform', methods=["POST"])
def test_fetch():
    transform = Base36DateTime()
    content = request.json
    datetime_input = content.get('datetime_input', "")
    base36_code_input = content.get('base36_code_input', "")
    if datetime_input or base36_code_input:
        if datetime_input:
            value2 = transform.encoding_dateTime(datetime_input)
            return {'datetime_input': datetime_input,
                    'base36_code_input': value2}
        elif base36_code_input:
            value2 = transform.decoding_base36(base36_code_input)
            return {'datetime_input': value2,
                    'base36_code_input': base36_code_input}

    else:
        datetime_now = datetime.datetime.now().strftime("%Y-%m-%d")
        value1 = transform.encoding_dateTime(datetime_now)
        value2 = transform.decoding_base36(value1)
        return {'datetime_input': value2,
                'base36_code_input': value1}


if __name__ == '__main__':
    app.run(port=5004, debug=True)
