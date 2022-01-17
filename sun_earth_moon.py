import nbody

sun = nbody.Body(nbody.Vector(0,0),nbody.Vector(0,0),1.989e30)
earth = nbody.Body(nbody.Vector(147.17e9,0),nbody.Vector(0,30e3),5.972e24)
moon = nbody.Body(nbody.Vector(384400e3,0),nbody.Vector(0,3683e3/3600),7.34767309e22)

bodies = [
    sun,earth,moon
]

nbody.animate(bodies,60*60*24,365,(3e11,3e11))