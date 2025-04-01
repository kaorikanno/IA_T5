Aclaraciones:

Dejé las iteraciones hasta 40000, pues a partir de aquí ya no mejoraba mucho más mi rendimiento, al menos con la configuración inicial.

En la línea 48 creé la función self.tupla_a_entero, la cual convierte la tupla de los 5 valores que definen al estado en un número, de tal forma de que el q_table trabaje con un solo valor numérico para el estado y otro para el movimiento. La explicación de este código está implementada en el código mismo, pero básicamente el número fue asignado considerando el orden de estos valores y sus rangos, de tal forma de de ir asignando un valor único a cada tupla a partir de multiplicar estos rangos y sumarlos, de tal forma de hacerlo único para cada caso.

Luego, retorné este valor entero a la función self.get_state para que todo valor de estado tenga esta etiqueta única.

En get_action, en la línea 95 se aprecia que cambié el peso de las acciones posibles al explorar, dándole mucho más peso a la acción 0, de tal forma que al inicio no vaya siempre subiendo tanto y logre atravesar los tubos antes. En la línea 107 utilicé argmax, lo cual vimos en la ayudantía 11.

Para el q_table ocupé una de las funciones vistas en clases para definirla.

Modifiqué la línea 155 para que las actualizaciones salgan cada 1000 juegos en vez de cada 100, pues son muchas.

Finalmente en la línea 179 agregué un código que escribía el q_table de salida en el csv adjuntado, "q_table.csv". 

En la "respuestas_teóricas.pdf" añadí las respuestas teóricas, además copié ciertas iteraciones como el score y el record de arcos para comparar los discount rate y los learning rates, esto para 30000 iteraciones, pues después de este valor, ya no mejoraba mucho en la configuración por defecto el record.