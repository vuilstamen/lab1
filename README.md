Прикреплённый .py файл представляет собой модель распространения эпидемии Гринберга-Гастингса. Модель способна имитировать распространение эпидемии на плоском поле с произвольными задаваемыми размерами. 
На поле обязательно присутствуют больные и здоровые клетки. В конце пользователь получает картину распространения эпидемии, а также количество и типы клеток.
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Инструкция по запуску:
В начале выполнения кода появляется простейший интерфейс, в котором вводятся начальные данные (вид данных указан там же).
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Структура данных: входные данные представляют собой последовательность чисел, ограниченных размеры области, количество больных клеток, смертность и скорость смены кадров в анимации.
Выходные данные представляют собой совокупность пошаговых отражений хода эпидемии, её gif-анимации и набора данных в консоли (разбивка по типам клеток).
--------------------------------------------------------------------------------------------------------------------------------------------------------------
Модель позволяет многократно проводить эксперименты с различными начальными данными в целях проверки работоспособности модели и установления интересующих фактов 
(влияние различных факторов на ход эпидемии и сравнение экспериментов между собой).
--------------------------------------------------------------------------------------------------------------------------------------------------------------
В отчёте каждый случай представлен соответствующим графиком состояния клеток. Здесь представлены gif-анимации, соответствующие каждому случаю.
Составные номера (например, "рисунок_8_1") означают, что анимация относится к 1-му подграфику случая 8.
--------------------------------------------------------------------------------------------------------------------------------------------------------------
<table>
  <!-- Строка 1 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic1.gif" width="200"><br><sub>epidemic_pic1</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic2.gif" width="200"><br><sub>epidemic_pic2</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic3.gif" width="200"><br><sub>epidemic_pic3</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic4.gif" width="200"><br><sub>epidemic_pic4</sub></td>
  </tr>
  <!-- Строка 2 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic5.gif" width="200"><br><sub>epidemic_pic5</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic6.gif" width="200"><br><sub>epidemic_pic6</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic7.gif" width="200"><br><sub>epidemic_pic7</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic8_1.gif" width="200"><br><sub>epidemic_pic8_1</sub></td>
  </tr>
  <!-- Строка 3 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic8_2.gif" width="200"><br><sub>epidemic_pic8_2</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic9.gif" width="200"><br><sub>epidemic_pic9</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic10.gif" width="200"><br><sub>epidemic_pic10</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic11.gif" width="200"><br><sub>epidemic_pic11</sub></td>
  </tr>
  <!-- Строка 4 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic12.gif" width="200"><br><sub>epidemic_pic12</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic13.gif" width="200"><br><sub>epidemic_pic13</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic14_1.gif" width="200"><br><sub>epidemic_pic14_1</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic14_2.gif" width="200"><br><sub>epidemic_pic14_2</sub></td>
  </tr>
  <!-- Строка 5 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic15.gif" width="200"><br><sub>epidemic_pic15</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic16.gif" width="200"><br><sub>epidemic_pic16</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic17.gif" width="200"><br><sub>epidemic_pic17</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic18.gif" width="200"><br><sub>epidemic_pic18</sub></td>
  </tr>
  <!-- Строка 6 -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic19.gif" width="200"><br><sub>epidemic_pic19</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic20.gif" width="200"><br><sub>epidemic_pic20</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic21.gif" width="200"><br><sub>epidemic_pic21</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic22.gif" width="200"><br><sub>epidemic_pic22</sub></td>
  </tr>
  <!-- Строка 7 (оставшиеся 2 гифки) -->
  <tr>
    <td width="25%" align="center"><img src="gif/epidemic_pic23.gif" width="200"><br><sub>epidemic_pic23</sub></td>
    <td width="25%" align="center"><img src="gif/epidemic_pic24.gif" width="200"><br><sub>epidemic_pic24</sub></td>
    <td width="25%"></td> <!-- Пустая ячейка для ровности -->
    <td width="25%"></td> <!-- Пустая ячейка для ровности -->
  </tr>
</table>
