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
    
    if (count + 2) < len(mesh.vertices) and (count - 1) < len(mesh.vertices) :
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
    
#***********************
#** calculate vectors **
#***********************  
def calc_vec(location ,ran, count):
    
    dx = location[0] / (math.sqrt(location[0]**2 + location[1]**2 + location[2]**2))
    dy = location[1] / (math.sqrt(location[0]**2 + location[1]**2 + location[2]**2))
    dz = location[2] / (math.sqrt(location[0]**2 + location[1]**2 + location[2]**2))


    location[0] += dx * ran[count]
    location[1] += dy * ran[count]
    location[2] += dz * ran[count]
    
    return location


#******************************
#** creating a "perlin" noise**
#******************************
def poor_mans_perlin(ran):
    ran_two = ran
    
    point = 128
    teilen = 2
    for itr in range(1,7) :
        ct = 0  
        for z in range(len(ran)):
            if ct < point:
                if it == 1:
                    wert = 0.0
                if it >1 :
                    wert = ran_two[z]
                ran_two[z] = wert
                ct += 1
            else :
               wert = ran[z] / teilen
               ran_two[z] = wert
               ct = 0
        point = point / 2
        teilen = teilen + 2
        
    return ran_two

#******************************************************
#** get vertices, vector and move vertices **
#******************************************************
def move_verts(zero, mesh, rand_max, it, obj):
    #++ subsurf ++
    sub_mod(obj,it)
    #++ randoms ++
    mesh = obj.data
    ran = []
    for x in range(len(mesh.vertices)):
        rx = random.uniform(0, rand_max / it)
        ran.append(rx)
    
    if it >= 2:
        ran_two = poor_mans_perlin(ran)
            
            
    #++ move vertices along a vector from center ++
    count = 0
    
    for vert in mesh.vertices:
        location = vert.co
        #d = math.sqrt((location[0] - zero[0]) ** 2 + (location[1] - zero[1]) ** 2 + (location[2] - zero[2]) ** 2)
        if it == 1 :
            
            loc = calc_vec(location ,ran, count)
            
            vert.co = loc
            
        elif it == 2 and check_others(count, mesh, ran) == True :
            
            

            loc = calc_vec(location ,ran_two, count)
            
            vert.co = loc
            
        else:

            loc = calc_vec(location ,ran_two, count)
            
            vert.co = loc

        count += 1
        
    
    


#++ global variables ++
zero = (0.0, 0.0, 0.0)       
sub_level = 2
rnd = 1.1
max_it = 4

#++ creating the object ++
row = sub_level * sub_level
bpy.ops.mesh.primitive_cube_add()
pl = bpy.context.active_object

for it in range(1,max_it):
    
    move_verts(zero, pl.data, rnd, it, pl)
    #++ decreasing the random max value to avoid weird artifacts ++
    rnd = rnd / 5.0
    
    
mesh = pl.data 
  
for face in mesh.polygons:
    face.use_smooth = True

#sub_mod(pl,max_it)

#++ end creation ++
