

import pywavefront
from shutil import copyfile
from pyffi.formats.nif import NifFormat
from PIL import Image, ImageEnhance
import os
from pathlib import Path
import shutil

###############################
# CHANGE TEXTURE BRIGHTNESS
###############################

def change_brightness(filename,brillo):
    #read the image
    #print(filename)
    data_folder = Path(filename)
    #print(data_folder)
    im = Image.open(data_folder)
    #print(filename)
    
    
    #image brightness enhancer
    enhancer = ImageEnhance.Brightness(im)
    
    factor = brillo/10 #darkens the image
    im_output = enhancer.enhance(factor)
    im_output.save('output_texture.jpg')

###############################
# OPEN AND EXTRACT OBJ INFO
###############################
    
def generate_meshes(f_obj,fem,f_tex):
    
    #######################################################
    ## Remove second line of facegen generated obj because it has a weird char
    #######################################################
    basefile_obj, file_extension = os.path.splitext(f_obj)
    
    #basefile_obj = "input"
    basefile_obj_ = basefile_obj + ".obj"
    basefile_copy = basefile_obj + "_copy.obj"
    basefile_mtl = basefile_obj+".mtl"
    basefile_mtl_copy = basefile_obj+"_copy.mtl"
    with open(basefile_obj_, "r") as infile:
        lines = infile.readlines()
    
    with open(basefile_copy, "w") as outfile:
        for pos, line in enumerate(lines):
            if pos != 1:
                outfile.write(line)
    
    copyfile(basefile_mtl,basefile_mtl_copy)
    
    #######################################################
    ## Load and extract info from obj
    #######################################################
    
    scene = pywavefront.Wavefront(basefile_copy)
    
    vertex_obj = scene.vertices
    num_vertex_obj = len(vertex_obj)
    print("#############################")
    print("num_vertex_obj")
    print(num_vertex_obj)
    print("#############################")
    
    #num_vertx_obj_eyes = 0
    #num_vertx_obj_browns = 0
    
    ###############################
    # OPEN AND EXTRACT NIF INFO
    ###############################
    
    #basefile = 'malehead.nif'
    female = fem
    if female:
        basefile = 'femalehead.nif'
    else :
        basefile = 'malehead.nif'
        
    stream = open(basefile, 'rb')
    data = NifFormat.Data()
    data.read(stream)
    stream.close()
    
    
    if female:
        num_vertx_obj_head = 3832
        num_vertx_obj_eyes = 176
        num_vertx_obj_browns = 318
    else:
        num_vertx_obj_head = 3598
        num_vertx_obj_eyes = 186
        num_vertx_obj_browns = 318
    
    
    for root in data.roots: 
        for block in root.tree(): 
            if isinstance(block, NifFormat.NiNode): 
                print(block.name.decode("ascii"))
                if block.name.decode("ascii")=='MaleHeadKouLeifoh':
                    bloqueForma = block
                    print('entra if 1')
                if block.name.decode("ascii")=='Scene Root':
                    bloqueForma = block
                    print('entra if 1')
                
    for elementos in bloqueForma.tree():
        if female:
            if isinstance(elementos, NifFormat.NiTriShape):
                print(elementos.name.decode("ascii"))
                if elementos.name.decode("ascii")=='FemaleHead':
                    bloqueForma_sub = elementos
                    print('entra if 2')
                if elementos.name.decode("ascii")=='HairFemaleRedguard03':
                    bloqueHair_sub = elementos
                    print('entra if 2.5')
                if elementos.name.decode("ascii")=='FemaleEyesHumanHazelBrown':
                    bloqueEyes_sub = elementos
                    print('entra if 2.6')
                if elementos.name.decode("ascii")=='FemaleBrowsHuman07':
                    bloqueBrowns_sub = elementos
                    print('entra if 2.7')
                if elementos.name.decode("ascii")=='FemaleMouthHumanoidDefault':
                    bloqueMouth_sub = elementos
                    print('entra if 2.9')
        else:
            if isinstance(elementos, NifFormat.NiTriShape):
                print(elementos.name.decode("ascii"))
                if elementos.name.decode("ascii")=='MaleHeadIMF':
                    bloqueForma_sub = elementos
                    print('entra if 2')
                if elementos.name.decode("ascii")=='HairMaleImperial1':
                    bloqueHair_sub = elementos
                    print('entra if 2.5')
                if elementos.name.decode("ascii")=='MaleEyesHumanHazelBrown':
                    bloqueEyes_sub = elementos
                    print('entra if 2.6')
                if elementos.name.decode("ascii")=='00KLH_BrowsMaleHumanoid07':
                    bloqueBrowns_sub = elementos
                    print('entra if 2.7')
                if elementos.name.decode("ascii")=='MaleMouthHumanoidDefault':
                    bloqueMouth_sub = elementos
                    print('entra if 2.9')
    
    
    for elementos2 in bloqueForma_sub.tree():
        if isinstance(elementos2, NifFormat.NiTriShapeData):
            print('entra if 3')
            infoShape = elementos2
    
    verticesForma = infoShape.vertices
    
    triangles_nif = infoShape.triangles
    num_triangles_nif = infoShape.num_triangles
    
    
    ###############################
    # MAKE A COPY OF HEAD INFO
    ###############################
    
    stream_c = open(basefile, 'rb')
    data_c = NifFormat.Data()
    data_c.read(stream_c)
    stream_c.close()
    
    for root_c in data_c.roots: 
        for block_c in root_c.tree(): 
            if isinstance(block_c, NifFormat.NiNode): 
                #print(block.name.decode("ascii"))
                if block_c.name.decode("ascii")=='MaleHeadKouLeifoh':
                    bloqueForma_c = block_c
                    print('entra if 1')
                if block_c.name.decode("ascii")=='Scene Root':
                    bloqueForma_c = block_c
                    print('entra if 1')
    
    for elementos_c in bloqueForma_c.tree():
        if isinstance(elementos_c, NifFormat.NiTriShape):
            print(elementos_c.name.decode("ascii"))
            if(female):
                if elementos_c.name.decode("ascii")=='FemaleHead':
                    bloqueForma_sub_c = elementos_c
                    print('entra if 2')
            else:
                if elementos_c.name.decode("ascii")=='MaleHeadIMF':
                    bloqueForma_sub_c = elementos_c
                    print('entra if 2')
    
    for elementos2_c in bloqueForma_sub_c.tree():
        if isinstance(elementos2_c, NifFormat.NiTriShapeData):
            print('entra if 3')
            infoShape_c = elementos2_c
    
    verticesForma_copia = infoShape_c.vertices
    verticesForma_copia2 = infoShape_c.vertices
    
    
    ###############################
    # GET VERTEX NUMBER
    ###############################
    
    num_vertices = 0
    for vertx in verticesForma:
        #print(vertx)
        num_vertices = num_vertices+1
    
    ######################################
    # CHECK OBJ ORIENTATION ##############
    ######################################
    
    #Check obj orientation
    x_max = 0
    x_min = 0
    y_max = 0
    y_min = 0
    z_max = 0
    z_min = 0
    
    for r in range(num_vertex_obj):
        x_d = vertex_obj[r][0] 
        y_d = vertex_obj[r][1] 
        z_d = vertex_obj[r][2]
        
        if x_d > x_max:
            x_max = x_d
        elif x_d < x_min:
            x_min = x_d
        if y_d > y_max:
            y_max = y_d
        elif y_d < y_min:
            y_min = y_d
        if z_d > z_max:
            z_max = z_d
        elif z_d < z_min:
            z_min = z_d
            
    if (z_max-z_min)>(x_max-x_min) and (z_max-z_min)>(y_max-y_min):
        print('correct')
    elif (x_max-x_min)>(z_max-z_min):
        print('incorrect rotation')
    elif (y_max-y_min)>(z_max-z_min):
        print('incorrect rotation')
    
    
    ######################################
    # NOSE TO NOSE OBJ MOVEMENT ##########
    ######################################
        
    max_y = 0
    for n in range(num_vertx_obj_head):
        if vertex_obj[n+num_vertx_obj_eyes][1] > max_y:
            v_ind_nose_obj = n+num_vertx_obj_eyes
            max_y = vertex_obj[n+num_vertx_obj_eyes][1] 
    
    
    max_yn = 0
    for nn in range(num_vertices):
        if verticesForma[nn].y > max_yn:
            v_ind_nose_nif = nn
            max_yn = verticesForma[nn].y
    
    vertex_obj_ = [[0 for x in range(3)] for y in range(num_vertx_obj_head)]
    vertex_obj_eyes = [[0 for x in range(3)] for y in range(num_vertx_obj_eyes)]
    vertex_obj_browns = [[0 for x in range(3)] for y in range(num_vertx_obj_browns)]
    
    delta_nose_x = verticesForma[v_ind_nose_nif].x-vertex_obj[v_ind_nose_obj][0]
    delta_nose_y = verticesForma[v_ind_nose_nif].y-vertex_obj[v_ind_nose_obj][1]
    delta_nose_z = verticesForma[v_ind_nose_nif].z-vertex_obj[v_ind_nose_obj][2]
    
    for lm in range(num_vertx_obj_head):
        vertex_obj_[lm][0] = vertex_obj[lm+num_vertx_obj_eyes][0] + delta_nose_x
        vertex_obj_[lm][1] = vertex_obj[lm+num_vertx_obj_eyes][1] + delta_nose_y 
        vertex_obj_[lm][2] = vertex_obj[lm+num_vertx_obj_eyes][2] + delta_nose_z
        
    ######################################
    # EYES MOVEMENT ##########
    ######################################
    
    if female:
        #d_h_x_ =  -0.000008
        #d_h_y_ =  -1.595064
        #d_h_z_ =  120.741463
        d_h_x_ =  -0.000256
        d_h_y_ =  -1.547514
        d_h_z_ =  120.343597
    else:
        #d_h_x_ =  -0.000256
        #d_h_y_ =  -1.547517
        #d_h_z_ =  120.343590
        d_h_x_ =  -0.000256
        d_h_y_ =  -1.547517
        d_h_z_ =  120.343590
    
    #################################################
    # project nif vertices to obj #############
    #################################################
    
    
    for i in range( num_vertx_obj_head ):
        #print(verticesForma_ref[i])
        verticesForma[i ].x = vertex_obj_[ i ][0]
        verticesForma[i ].y = vertex_obj_[ i ][1]
        verticesForma[i ].z = vertex_obj_[ i ][2]
    
    if female:
        path_h = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Female/output_head.nif'
    else:
        #path_h = 'FaceToSkyrimGenerated/Data/Meshes/Male/output_head.nif'
        path_h = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Male/output_head.nif' 
    stream2 = open(path_h, 'wb')
    data.write(stream2)
    stream2.close()
    
    
    
    
    ###############################
    # OPEN AND EXTRACT EYES INFO
    ###############################
    #######################################################
    ## Remove second line of facegen generated obj because it has a weird char
    #######################################################
    """
    basefile_obj = "input_eyes"
    basefile_obj_ = basefile_obj + ".obj"
    basefile_copy = basefile_obj + "_copy.obj"
    basefile_mtl = basefile_obj+".mtl"
    basefile_mtl_copy = basefile_obj+"_copy.mtl"
    with open(basefile_obj_, "r") as infile:
        lines = infile.readlines()
    
    with open(basefile_copy, "w") as outfile:
        for pos, line in enumerate(lines):
            if pos != 1:
                outfile.write(line)
    
    
    #######################################################
    ## Load and extract info from obj
    #######################################################
    
    scene = pywavefront.Wavefront(basefile_copy)
    
    vertex_obj = scene.vertices
    num_vertex_obj = len(vertex_obj)
    print("#############################")
    print("num_vertex_obj")
    print(num_vertex_obj)
    print("#############################")
    
    """
    ###############################
    # OPEN AND EXTRACT NIF INFO
    ###############################
    
    if female:
        basefile = 'eyesfemale.nif'
    else :  
        basefile = 'eyesmale.nif'
        
    
    stream = open(basefile, 'rb')
    dataE = NifFormat.Data()
    dataE.read(stream)
    stream.close()
    
    
    
    for root in dataE.roots: 
        for block in root.tree(): 
            if isinstance(block, NifFormat.NiNode): 
                print(block.name.decode("ascii"))
                if block.name.decode("ascii")=='EyesMale.nif':
                    bloqueForma = block
                    print('entra if 1')
                if block.name.decode("ascii")=='EyesFemale.nif':
                    bloqueForma = block
                    print('entra if 1')
                
    for elementos in bloqueForma.tree():
        if female:
            if isinstance(elementos, NifFormat.NiTriShape):
                if elementos.name.decode("ascii")=='EyesFemaleV2':
                    bloqueEyes_sub = elementos
                    print('entra if 2.6')
        else:
            if isinstance(elementos, NifFormat.NiTriShape):
                print(elementos.name.decode("ascii"))
                if elementos.name.decode("ascii")=='EyesMale':
                    bloqueEyes_sub = elementos
                    print('entra if 2.6')
    
    
    for elementosE in bloqueEyes_sub.tree():
        if isinstance(elementosE, NifFormat.NiTriShapeData):
            print('entra if 3.6')
            infoEyes = elementosE
    
    verticesEyes = infoEyes.vertices
    
    num_vertices_eyes = 0
    for vertx in verticesEyes:
        num_vertices_eyes = num_vertices_eyes+1
    
    vertex_obj_eyes = [[0 for x in range(3)] for y in range(num_vertx_obj_eyes)]
    
    
    delta_eyes_fix = 9.4-7.8
    
    for ey in range(num_vertx_obj_eyes):
    
        vertex_obj_eyes[ey][0] = vertex_obj[ey][0] + delta_nose_x - d_h_x_ #+ d_eyes_x
        vertex_obj_eyes[ey][1] = vertex_obj[ey][1] + delta_nose_y - d_h_y_ #+ d_eyes_y
        vertex_obj_eyes[ey][2] = vertex_obj[ey][2] + delta_nose_z - d_h_z_ #+ d_eyes_z #- delta_eyes_z
    
    
    #fix_y_factor = 0.35
    fix_y_factor = 0.1
    fix_z_factor = 0.1
    for e in range(len(vertex_obj_eyes)):
        #print(verticesForma_ref[i])
        verticesEyes[e].x = vertex_obj_eyes[ e ][0]
        verticesEyes[e].y = vertex_obj_eyes[ e ][1] #+ fix_y_factor
        verticesEyes[e].z = vertex_obj_eyes[ e ][2] #+ fix_z_factor
        
    
    if female:
        path_e = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Female/output_eyes.nif'
    else:
        path_e = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Male/output_eyes.nif'
    
    stream2 = open(path_e, 'wb')
    dataE.write(stream2)
    stream2.close()
    
    
    ###############################
    # GENERATE MOVED MOUTH
    ###############################
    ###############################
    # OPEN AND EXTRACT MOUTH INFO
    ###############################
    
    if female:
        basefileM = 'mouthhumanf.nif'
    else :  
        basefileM = 'mouthhuman.nif'
        
    
    stream = open(basefileM, 'rb')
    dataM = NifFormat.Data()
    dataM.read(stream)
    stream.close()
    
    
    
    for root in dataM.roots: 
        for block in root.tree(): 
            if isinstance(block, NifFormat.NiNode): 
                print(block.name.decode("ascii"))
                if block.name.decode("ascii")=='MouthHuman.nif':
                    bloqueForma = block
                    print('entra if 1')
                if block.name.decode("ascii")=='MouthHumanF.nif':
                    bloqueForma = block
                    print('entra if 1')
                
    for elementos in bloqueForma.tree():
        if female:
            if isinstance(elementos, NifFormat.NiTriShape):
                if elementos.name.decode("ascii")=='MouthHumanF':
                    bloqueMouth_sub = elementos
                    print('entra if 2.6')
        else:
            if isinstance(elementos, NifFormat.NiTriShape):
                print(elementos.name.decode("ascii"))
                if elementos.name.decode("ascii")=='MouthHuman':
                    bloqueMouth_sub = elementos
                    print('entra if 2.6')
    
    
    for elementosE in bloqueMouth_sub.tree():
        if isinstance(elementosE, NifFormat.NiTriShapeData):
            print('entra if 3.6')
            infoMouth = elementosE
    
    verticesMouth = infoMouth.vertices
    
    num_vertices_mouth = 0
    for vertx in verticesMouth:
        num_vertices_mouth = num_vertices_mouth+1
    
    num_vertx_obj_mouth = 141
    
    vertex_obj_mouth  = [[0 for x in range(3)] for y in range(num_vertx_obj_mouth)]
    
    
    for ey in range(num_vertx_obj_mouth):
    
        vertex_obj_mouth[ey][0] = verticesMouth[ey].x + delta_nose_x #- d_h_x_ #+ d_eyes_x
        vertex_obj_mouth[ey][1] = verticesMouth[ey].y + delta_nose_y #- d_h_y_ #+ d_eyes_y
        vertex_obj_mouth[ey][2] = verticesMouth[ey].z + delta_nose_z #- d_h_z_ #+ d_eyes_z #- delta_eyes_z
    
    
    #fix_y_factor = 0.35
    fix_y_factor = 0.1
    fix_z_factor = 0.1
    
    for e in range(len(vertex_obj_mouth)):
        #print(verticesForma_ref[i])
        verticesMouth[e].x = vertex_obj_mouth[ e ][0]
        verticesMouth[e].y = vertex_obj_mouth[ e ][1] #+ fix_y_factor
        verticesMouth[e].z = vertex_obj_mouth[ e ][2] #+ fix_z_factor
        
    
    if female:
        path_m = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Female/output_mouth.nif'
    else:
        path_m = 'FaceToSkyrimGenerated/Data/Meshes/RazaFacegen/Male/output_mouth.nif'
    
    stream2 = open(path_m, 'wb')
    dataM.write(stream2)
    stream2.close()
    
    
    tex_folder = Path(f_tex)
    if female:
        plus = 'FaceToSkyrimGenerated/Data/Textures/RazaFacegen/Female/output_texture.dds'
    else:
        plus = 'FaceToSkyrimGenerated/Data/Textures/RazaFacegen/Male/output_texture.dds'
    
    
    copyfile(tex_folder,plus)
    
    
    ###############################
    # CREATE ZIP FILE WITH FOLDER (RACE MOD)
    ###############################
    shutil.make_archive('FaceToSkyrimGenerated', 'zip', 'FaceToSkyrimGenerated')
    
    
    




















