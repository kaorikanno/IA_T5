import random
import numpy as np
from FlappyBirdAI import FlappyBird
import pandas as pd

# Hiperparámetros
LR = 0.3  # modificar
NUM_EPISODES = 30000  # lo cambié a 40000, pues a partir de aquí ya no mejora mucho más
DISCOUNT_RATE = 0  # modificar
MAX_EXPLORATION_RATE = 1
MIN_EXPLORATION_RATE = 0.0002
EXPLORATION_DECAY_RATE = 0.00015

VISUALIZATION = False  # modificar

class Agent:
    # Esta clase posee al agente y define sus comportamientos.

    def __init__(self):
        # Creamos la q_table y la inicializamos en 0.
        # IMPLEMENTAR
        self.q_table = np.zeros((159936, 7))

        # Inicializamos los juegos realizados por el agente en 0.
        self.n_games = 0

        # Inicializamos el exploration rate.
        self.EXPLORATION_RATE = MAX_EXPLORATION_RATE

        # Inicializamos los juegos realizados por el agente en 0.
        self.n_games = 0

    def get_state(self, game):
        # Este método consulta al juego por el estado del agente y lo retorna como una tupla.
        state = []

        # Computamos la distancia en el eje x entre el jugador y la tubería más cercana
        delta_x = game.current_wall.x - game.character.x
        delta_x = delta_x//22
        if delta_x < 0:
            delta_x = 0
        if delta_x > 50:
            delta_x = 50
        state.append(delta_x)

        sense = 0

        # Calculamos la distancia en el eje y con el agujero de la próxima tubería
        delta_y = game.character.y - game.current_wall.hole
        if delta_y < 0:
            # Sense nos indica si la tubería se encuentra encima o debajo del agente
            sense = 1
        delta_y = abs(delta_y//15)
        if delta_y > 27:
            delta_y = 27
        state.append(int(delta_y))
        state.append(sense)

        sense_next = 0

        # Calculamos la distancia al agujero de la tubería que vendrá después de la actual
        next_wall = game.walls[1] if game.current_wall == game.walls[0] else game.walls[0]
        delta_y_next = game.character.y - next_wall.hole
        if delta_y_next < 0:
            # Sense nos indica si el agujero se encontrará encima o debajo del agente
            sense_next = 1
        delta_y_next = abs(delta_y_next//15)
        if delta_y_next > 27:
            delta_y_next = 27
        state.append(int(delta_y_next))
        state.append(sense_next)

        tupla = tuple(state)
        valor = int(self.tupla_a_entero(tupla)) # volvemos un entero a la tupla
        return valor

    
    def tupla_a_entero(self, tupla):
        """
        Esta función convertirá nuestra tupla a un valor numérico para poder ordenar en el qtable
        """
        # como tupla[0] sabemos que toma valores de 0 a 50, no puede tomar valores mayores a esto
        # lo mismo con tupla[1], que no toma valores sobre 27, y así con todos
        # así que si queremos valores únicos para todos, sabemos que tupla[1] puede tomar valores sobre 51
        # de tal forma que tendremos valores únicos de este modo, como en combinatoria:
        valor = tupla[0] + tupla[1]*51 + tupla[2]*28*51 + tupla[3]*2*28*51 + tupla[4]*28*28*51*2
        return valor

    def get_action(self, state):
        # Este método recibe una estado del agente y retorna un entero con el indice de la acción correspondiente.
        # basado en: https://colab.research.google.com/drive/1Ur_pYvL_IngmAttMBSZlBRwMNnpzQuY_#scrollTo=KASNViqL4tZn

        accion = random.uniform(0, 1) # elegimos al azar si explorar o explotar
        #print("acción:", accion)
        # vamos a ver si explorar o explotar
        if accion <= self.EXPLORATION_RATE: # si vamos a explorar, no sabemos qué opción tomar
            #print("por esta acción vamos a explorar")
            # como no logra llegar mucho en x si es equitativo entre 0 y 1 hice el siguiente cambio:
            if random.random() < 0.95:
                return 0
            else:
                return 1
        else:
            if not np.any(self.q_table[state, :]): # si el estado no ha sido explorado, nos movemos al azar
                return random.choice([0, 1])
            else:
                return np.argmax(self.q_table[state, :])

def train():
    # Esta función es la encargada de entrenar al agente.

    # Las siguientes variables nos permitirán llevar registro del desempeño del agente.
    plot_scores = []
    plot_mean_scores = []
    mean_score = 0
    total_score = 0
    record = 0
    period_steps = 0
    period_score = 0

    # Instanciamos al agente o lo cargamos desde un pickle.
    agent = Agent()

    # Instanciamos el juego. El bool 'vis' define si queremos visualizar el juego o no.
    # Visualizarlo lo hace mucho más lento.
    game = FlappyBird(vis = VISUALIZATION)

    # Inicializamos los pasos del agente en 0.
    steps = 0

    while True:
        # Obtenemos el estado actual.
        state = agent.get_state(game)
        # Generamos la acción correspondiente al estado actual.
        move = agent.get_action(state)

        # Ejecutamos la acción.
        reward, done, score = game.play_step(move)

        # Obtenemos el nuevo estado.
        new_state = agent.get_state(game)

        # Actualizamos la q-table.
        agent.q_table[state, move] = agent.q_table[state, move] * (1 - LR) + LR * (reward + DISCOUNT_RATE * np.max(agent.q_table[new_state, :]))
        if done:
            # Actualizamos el exploration rate.
            agent.EXPLORATION_RATE = MIN_EXPLORATION_RATE + (MAX_EXPLORATION_RATE - MIN_EXPLORATION_RATE) * np.exp(-EXPLORATION_DECAY_RATE * agent.n_games)
            #Reiniciamos el juego.
            game.reset()

            # Actualizamos los juegos jugados por el agente.
            agent.n_games += 1

            # Imprimimos el desempeño del agente cada 100 juegos.
            if agent.n_games % 1000 == 0:
                # La siguiente línea guarda la QTable en un archivo (para poder ser accedida posteriormente)

                # Información relevante sobre los últimos 100 juegos
                print('Game', agent.n_games, 'Mean Score', period_score/100, 'Record:', record, "EXP_RATE:", agent.EXPLORATION_RATE, "STEPS:", period_steps/100)
                record = 0
                period_score = 0
                period_steps = 0

            # Actualizamos el record del agente.
            if score > record:
                record = score
            
            # Actualizamos nuestros indicadores.
            period_steps += steps
            period_score += score
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            steps = 0
            
            # En caso de alcanzar el máximo de juegos cerramos el loop. 
            if agent.n_games == NUM_EPISODES:
                # df = pd.DataFrame(agent.q_table)
                # file_path = "DCCanario/q_table_dr09.csv"
                # df.to_csv(file_path, index=False)
                # print(f"Data has been written to {file_path}")
                break

        else:
            steps += 1

if __name__ == '__main__':
    train()