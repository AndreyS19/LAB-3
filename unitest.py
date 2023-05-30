import unittest
from app import app


class Test(unittest.TestCase):
    def setUp(self):# Метод класса, вызываемый перед запуском тестов в отдельном классе.
        app.config['TESTING'] = True# устанавливает флаг TESTING в значение True, чтобы приложение работало в режиме тестирования.
        self.app = app.test_client() # чтобы отправлять запросы к приложению.

    #получение url-адреса стартовой страницы
    def test_home(self):
        #Браузер говорит серверу, чтобы он просто получил информацию, хранимую на этой странице, и отослал её
        result = self.app.get('/')# проверяет, что код состояния равен 200 (успешный запрос).
        self.assertEqual(result.status_code, 200)

    #ввод данных по url-адресу /solve
    def test_solve(self):
        #Браузер говорит серверу, что он хочет сообщить этому URL некоторую новую информацию, и что сервер должен убедиться, что данные сохранены и сохранены в единожды. Обычно, аналогичным образом происходит передача из HTML форм на сервер данных.
        response = self.app.post('/solve',data=dict(a=2.5, b=1, c=1))
        self.assertEqual(response.status_code, 200)# проверяет, что код состояния равен 200 (успешный запрос).

    # дискриминант меньше нуля
    def test_discriminant_less_than_zero(self):
        result = self.app.post('/solve', data=dict(a=2.5, b=1, c=1))
        self.assertEqual(result.status_code, 0)
        self.assertIn(b'x1=(-0,2+0,6j)', result.data)# проверяет, что в содержимом ответа присутствует строка x1=(-0,2+0,6j)
        self.assertIn(b'x2=(-0,2-0,6j)', result.data)# проверяет, что в содержимом ответа присутствует строка x1=(-0,2-0,6j)

    # дискриминант равен нулю
    def test_discriminant_equal_to_zero(self):
        result = self.app.post('/solve', data=dict(a=1, b=-2, c=1))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x=1,0', result.data) # проверяет, что в содержимом ответа присутствует строка x=1,0

    # дискриминант больше нуля
    def test_discriminant_more_than_zero(self):
        result = self.app.post('/solve', data=dict(a=1, b=-5, c=6))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x1=3,0', result.data)
        self.assertIn(b'x2=2,0', result.data)

    # нечитаемые параметры
    def test_unreadeble_variables(self):
        result = self.app.post('/solve', data=dict(a='f', b=-5, c=6))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'This is not quadratic equation!', result.data)

    # нулевой коэф-ент первого параметра
    def test_zero_variable1(self):
        result = self.app.post('/solve', data=dict(a=0, b=-5, c=6))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'This is not quadratic equation!', result.data)

    # нулевой коэф-ент второго параметра
    def test_zero_variable2(self):
        result = self.app.post('/solve', data=dict(a=1, b=0, c=-4))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x1=2,0', result.data)
        self.assertIn(b'x2=-2,0', result.data)
    # нулевой коэф-ент третьего параметра
    def test_zero_variable3(self):
        result = self.app.post('/solve', data=dict(a=1, b=2, c=0))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x1=0,0', result.data)
        self.assertIn(b'x2=-2,0', result.data)
    # отрицательные значения параметра
    def test_negative_variable(self):
        result = self.app.post('/solve', data=dict(a=-4, b=1, c=3))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x1=-0,75', result.data)
        self.assertIn(b'x2=1,0', result.data)

    # дробные значения параметра
    def test_fraction_variable(self):
        result = self.app.post('/solve', data=dict(a=0.25, b=3, c=5))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'x1=-2', result.data)
        self.assertIn(b'x2=-10', result.data)
    if __name__ == '__main__':
        unittest.main()
