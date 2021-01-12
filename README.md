# ClickTracker GUI

### Uso
Correr el script `python3 main.py`
Apareceran cuadrados de forma random en la pantalla. Al darle click el puntaje aumenta en uno. Al terminar las iteraciones del programa, arroja por consola el puntaje si se hizo click dentro del cuadrado.

### Configuraciones en código
```
STEP =  4                 # Seleccionar 1 de las 4 etapas enviadas en el ppt

#default configuration
square_max_iter     = 3   # número de veces que aparecerá un cuadrado
max_timer_click     = 5   # tiempo en segundos para presionarlo
square_size         = 200 # tamaño en pixeles de cuadrado
click_error         = 0   # error permitido de click 
random_pos          = True # seleccionar una posición random de aparición de los cuadrados o aparecerá en el centro
random_color        = True # escoger un color random desde color_options o de lo contrario se selecciona el color en square_color
square_color        = [255,0,0] # color RGB cuando random_color es False
colors_options      = [[255,0,0],[255,255,0],[0,0,255]] # opciones de color para escoger de forma random cuando random_color es True
```
El error es similar a generar un cuadrado de mayor area imaginario. Quiere decir si el cuadrado normal es de 200x200 al tener un error de 100 permite que el click sea válido presionando en un cuadrado de 300x300.

### Prerequisitos 
Hay que tener los siguientes paquetes instalados.
- `pip3`
- `tkinter` para la interfaz gráfica, viene en python 3 ahora.
- `pip3 install pynput` 
- `pip3 intsall keyboard`