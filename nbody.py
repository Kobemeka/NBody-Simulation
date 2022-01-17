from cProfile import label
import random
import numpy as np
import matplotlib.pyplot as plt
import colorsys as cs
from matplotlib.animation import FuncAnimation

G = 6.67408e-11

class Vector:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def getVector(self):
        return np.array([self.x,self.y])

    def magnitude(self):
        return np.sqrt(sum(np.power(self.getVector(),2)))

    def normalize(self):
        return Vector(*(self.getVector()/self.magnitude()))

    def __add__(self,other):
        return Vector(*(self.getVector() + other.getVector()))
    def __radd__(self,other):
        if other == 0:
            return self
        else:
            return self.__add__(other)

    def __sub__(self,other):
        return Vector(*(self.getVector() - other.getVector()))

    def __mul__(self,other):
        return Vector(*(self.getVector() * other))

    def __rmul__(self,other):
        return Vector(*(self.getVector() * other))
    
    def __truediv__(self,other):
        return Vector(*(self.getVector() / other))

    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"

class Body:
    def __init__(self,position:Vector,velocity:Vector,mass:float,name="Body") -> None:
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.name = name
    def actingAcceleration(self,objects,exclude):
        
        return sum([acceleration(o.position - self.position,o.mass) for i,o in enumerate(objects) if i != exclude])

    def changePosition(self,other_objects,time_step,exclude):
        self.velocity += self.actingAcceleration(other_objects,exclude)*time_step
        self.position += self.velocity*time_step
        return self.position

def createRandomNBody(n):
    return np.array([Body(Vector(1e7*random.randint(-5,5),1e7*random.randint(-5,5)),Vector(random.randint(-50,50),random.randint(-50,50)),1e24*random.randint(1,10),f"Body-{i}") for i in range(n)])

def distance(a,b):
    return a.position - b.position

def acceleration(distance,M):
    return G*M*distance.normalize()/np.power(distance.magnitude(),2)

def map_color(i,m):
    return cs.hsv_to_rgb(i/m,0.8,0.8)

def animate(bodies,time_step,total_time,boundaries:tuple):

    fig,ax = plt.subplots()
    positionsx = [[] for _ in range(len(bodies))]
    positionsy = [[] for _ in range(len(bodies))]
    animPlot = [plt.plot([],[],".-",label=f"{bodies[i].name}")[0] for i in range(len(bodies))]

    def init():
        ax.set_xlim(-boundaries[0],boundaries[0])
        ax.set_ylim(-boundaries[1],boundaries[1])
        return animPlot,

    def update(frame):
        for i in range(len(bodies)):
            positionsx[i].append(frame[i].x)
            positionsy[i].append(frame[i].y)
            animPlot[i].set_data(positionsx[i],positionsy[i])

        flt_px = np.array(positionsx).reshape(-1)
        flt_py = np.array(positionsy).reshape(-1)

        ax.set_xlim(min(flt_px),max(flt_px))
        ax.set_ylim(min(flt_py),max(flt_py))
        return animPlot,

    new_positions = [[b.changePosition(bodies,time_step,i) for i,b in enumerate(bodies)] for t in range(total_time)]

    ani = FuncAnimation(fig, update, frames=new_positions,init_func=init,interval=50)
    plt.legend()
    plt.show()