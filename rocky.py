import bpy
import random
import mathutils
import math

#*************************************
#** applying a sub-surface modifier **
#*************************************
def sub_mod(obj,i):
    pl_mod = pl.modifiers.new("tile"+str(i), "SUBSURF")
    #pl_mod.subdivision_type = "SIMPLE"
    pl_mod.levels = sub_level
    bpy.ops.object.modifier_apply(modifier="tile"+str(i))

#**********************************************************************
#** avoid large height differences between vertices(first iteration) **
#**********************************************************************
def check_first(count, mesh, ran):
    
    if (count + 2) < len(mesh.vertices) and abs(ran[count] - ran[count + 1]) < 0.1 :
        return True
    else:
        return False

#*****************************************************
#** avoid large height differences between vertices **
#*****************************************************
def check_others(count, mesh, ran):
    
    if (count + 2) < len(mesh.vertices) and ran[count] > 0.012 and ran[count + 1] > 0.012 and ran[count + 2] > 0.012:
        return True
    else:
        return False

#******************************************************
#** get vertices, calculate vector and move vertices **
#******************************************************
def move_verts(zero, mesh, rand_max, it, obj):
    #++ subsurf ++
    sub_mod(obj,it)
    #++ randoms ++
    ran = []
    for x in range(len(mesh.vertices)):
        rx = random.uniform(0, rand_max)
        ran.append(rx)

    #++ move vertices along a vector from center ++
    count = 0
    for vert in mesh.vertices: 
        if it == 1 and check_first(count, mesh, ran) == True:
            location = vert.co
            d = math.sqrt((location[0] - zero[0]) ** 2 + (location[1] - zero[1]) ** 2 + (location[2] - zero[2]) ** 2)
            #print(d)
            dx = zero[0] - location[0]
            dy = zero[1] - location[1]
            dz = zero[2] - location[2]
            
            h1 = math.atan2(dy, dx)
            h2 = math.atan2(dz, dy)
            
            location[0] += math.cos(h1) * ran[count]
            location[1] += math.sin(h1) * ran[count]
            location[2] += math.sin(h2) * ran[count]

            vert.co = location
            
        if it > 1 and check_others(count, mesh, ran) == True :
            location = vert.co
            d = math.sqrt((location[0] - zero[0]) ** 2 + (location[1] - zero[1]) ** 2 + (location[2] - zero[2]) ** 2)
            #print(d)
            dx = zero[0] - location[0]
            dy = zero[1] - location[1]
            dz = zero[2] - location[2]
            
            h1 = math.atan2(dy, dx)
            h2 = math.atan2(dz, dy)
            
            location[0] += math.cos(h1) * ran[count]
            location[1] += math.sin(h1) * ran[count]
            location[2] += math.sin(h2) * ran[count]

            vert.co = location

        count += 1



#++ global variables ++
zero = (0.0, 0.0, 0.0)       
sub_level = 2
rnd = 0.38
max_it = 3

#++ creating the object ++
row = sub_level * sub_level
bpy.ops.mesh.primitive_cube_add()
pl = bpy.context.active_object

for it in range(1,max_it):
    
    move_verts(zero, pl.data, rnd, it, pl)
    #++ decreasing the random max value to avoid weird artifacts ++
    rnd = rnd / 10.0

sub_mod(pl,max_it + 1)

#++ end creation ++
