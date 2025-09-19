import bpy
import numpy as np
import os
import sys
import random
path = r"BASE-PATH"

if path not in sys.path:
    sys.path.append(path)

def render_img(camera, out_dir, i):
    # Set the camera to the scene
    bpy.context.scene.camera = bpy.data.objects[camera]

    # Set the save path for the rendered image
    save_path = out_dir + "//" + str(i) + '.jpg'

    # Get the render settings
    r = bpy.context.scene.render
    
    # Set the resolution to a lower value (e.g., 1280x720)
    r.resolution_x = 512
    r.resolution_y = 512

    # Set the output file path
    r.filepath = save_path

    # Render the image and save it
    bpy.ops.render.render(write_still=True)



def add_bluerov(model_path,bluerov_location=(0,0,0)):
    bpy.ops.wm.collada_import(filepath=model_path)
    model_name = "BlueROV"

    obj=bpy.context.scene.objects["Untitled_282"]
    obj.name=model_name
    obj.location.x=0
    obj.location.y=0
    obj.location.z=0
    obj.rotation_euler.x=1.57 

    roll=1.57               
    pitch=0
    yaw=3.14159
    bottom_cam, cam_obj = set_camera(0,0,0,roll, pitch, yaw)
    cam_obj.parent = bpy.data.objects[model_name]

    roll=-0.436332
    pitch=3.14159
    yaw=0
    front_cam, cam_obj2 = set_camera(0,0,0,roll, pitch, yaw)
    cam_obj2.parent = bpy.data.objects[model_name]

    obj=bpy.context.scene.objects[model_name]
    obj.location.x=bluerov_location[0]
    obj.location.y=bluerov_location[1]
    obj.location.z=bluerov_location[2]

    obj=bpy.context.scene.objects["BlueROV"]
    obj.location=bluerov_location

    return front_cam, bottom_cam







def set_light(x=0, y=0, z=15, energy=70, angle=0.5):
    # Switch to Object mode if not already in it
    if bpy.context.object and bpy.context.object.mode != 'OBJECT':
        bpy.ops.object.mode_set(mode='OBJECT')

    # Select and delete existing light objects in the scene
    bpy.ops.object.select_by_type(type='LIGHT')
    bpy.ops.object.delete()

    # Add a Sun Light source
    bpy.ops.object.light_add(type='SUN', align='WORLD', location=(x, y, z))
    bpy.ops.object.use_shadow = False
    
    # Adjust the light energy (brightness)
    bpy.context.object.data.energy = energy

    # Set the angle for softer shadows (lower = sharper shadows, higher = softer)
    bpy.context.object.data.angle = angle

    # Deselect all objects after the operation
    bpy.ops.object.select_all(action='DESELECT')



def set_camera(x=0, y=0, z=2, roll=0, pitch=0, yaw=0, track=False):
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(x, y, z),rotation=(roll, pitch, yaw), scale=(1, 1, 1))
    if track:
        bpy.ops.object.constraint_add(type='TRACK_TO')
        bpy.context.object.constraints["Track To"].target = bpy.data.objects["BlueROV"]

    return bpy.context.object.name, bpy.context.object



def delete_objs():
    bpy.ops.object.select_by_type(type='MESH')
    bpy.ops.object.delete()
    bpy.ops.object.select_all(action='DESELECT')

def delete_landscape():
    # Check if the object exists in the scene
    if "Landscape" in bpy.context.scene.objects:
        # Select the object
        bpy.context.scene.objects["Landscape"].select_set(True)
        # Delete the selected object
        bpy.ops.object.delete()
    else:
        print("Landscape object not found in the scene.")
    
    # Deselect all objects to avoid confusion
    bpy.ops.object.select_all(action='DESELECT')


def delete_oysters():
    for obj in bpy.context.scene.objects:
        if obj.name.startswith("rhino") or obj.name.startswith("ImageToStl"):
            #print("stunk")
            obj.select_set(True)
            bpy.ops.object.delete()
    bpy.ops.object.select_all(action='DESELECT')

def apply_texture(PassiveObject, mat):
    if PassiveObject.data.materials:
        PassiveObject.data.materials[0] = mat
    else:
        PassiveObject.data.materials.append(mat)





def add_oyster(model_dir_path=None, texture_dir_path=None, n_clusters=5, min_oyster=5, max_oyster=None, x_range=5, y_range=5):
    cal_n_oysters = True
    if max_oyster is None:
        n_oyster = min_oyster
        cal_n_oysters = False


    # calculate cluster offset values
    cluster_offset_x = x_range * 0.05
    cluster_offset_y = y_range * 0.05

    # list of -1 and 1 to choose sign for cluster offset
    signs = [-1, 1, 1, -1, -1, 1, -1]

    # list of mesh names in model_dir_path
    if model_dir_path is None:
        print("Error: Model directory path is None")
        return

    mesh_names = os.listdir(model_dir_path)
    #print(f"Mesh names loaded: {mesh_names}")

    # list of textures in texture_dir_path
    texture_names = []
    if texture_dir_path:
        texture_names = os.listdir(texture_dir_path)
    else:
        print("No texture directory path provided.")

    pass_idx = 1

    for i in range(n_clusters):
        plane_size_x = 20.3
        plane_size_y = 20.3
        n_oyster = random.randint(min_oyster, max_oyster)
        #print(f"\nCluster {i+1}:")
        #print(f"  - Number of oysters: {n_oyster}")

        # randomly select mesh names for the cluster
        cluster_mesh_names = [random.choice(mesh_names) for i in range(n_oyster)]
        #print(f"  - Selected meshes: {cluster_mesh_names}")

        for n in range(0, n_oyster):
            # oyster model path
            oyster_file_path = "/fs/nexus-scratch/zeorymer/lastsim/underwater-perception-xiaomin/data/blender_data/oysters/model/rhino.stl"

            bpy.ops.import_mesh.stl(filepath=oyster_file_path)
            bpy.context.object.hide_render = False 
            bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='MEDIAN')
            bpy.context.object.cycles.cast_shadow = False

            
            target_areas = {0.000305, 0.00061, 0.002747, 0.000137, 0.002579, 0.001465, 0.000687, 0.00238, 0.001602,
                0.000214, 0.000824, 0.000992, 0.000961, 0.000488, 0.000183, 0.00032, 0.003372, 0.001984,
                0.002289, 0.001511, 0.003204, 0.002594, 0.001343, 0.001648, 0.001953, 0.001175, 0.001785,
                0.001007, 0.000229, 0.000534, 0.000839, 0.000366, 0.003113, 0.000671, 0.002777, 0.001389,
                0.000916, 0.001221, 0.001526, 0.001831, 0.000748, 0.002136, 0.002441, 0.000275, 0.00119,
                0.000412, 0.001495, 0.000244, 0.000549, 0.000854, 0.002991, 0.000381, 0.002518,
                0.0023001587, 0.001282, 0.002197, 0.000641}

            # Image size (256x256)
            image_size = 256
            max_area_in_pixels = image_size * image_size
            
            # Convert target areas to pixel values
            target_area_in_pixels = {area: (area / (image_size ** 2)) * max_area_in_pixels for area in target_areas}
            
            # Get the selected object and calculate its bounding box projected area
            if bpy.context.object:
                selected_object = bpy.context.object
                bbox = selected_object.bound_box
                width = abs(bbox[0][0] - bbox[4][0])
                depth = abs(bbox[0][1] - bbox[2][1])
                projected_area = width * depth
            
                # Select a random target area from the available target areas
                target_area = random.choice(list(target_areas))
                
                # Calculate the scale factor for the selected target area
                scale_factor = math.sqrt(target_area / projected_area)
            

            scale_factor = random.uniform(0.015,0.02)
            #print(f"  - Selected scale: {scale_factor}")

            # Set oyster scales
            bpy.context.object.scale[0] = scale_factor
            bpy.context.object.scale[1] = scale_factor
            bpy.context.object.scale[2] = scale_factor

            # Set oyster location in x and y randomly
            random_x = random.uniform(-plane_size_x/3, plane_size_x/3)
            random_y = random.uniform(-plane_size_y/3, plane_size_y/3)
            #print(f"  - Oyster location: x={random_x}, y={random_y}, z=0")

            bpy.context.object.location.x = random_x
            bpy.context.object.location.y = random_y
            bpy.context.object.location.z = 0

            rand_rot = random.uniform(-90, 90)
            #print(f"  - Rotation angle: {rand_rot}")

            bpy.ops.transform.rotate(value=(90 * np.pi / 180), orient_axis='X')
            bpy.ops.transform.rotate(value=(90 * np.pi / 180), orient_axis='Z')
            bpy.ops.transform.rotate(value=(-np.pi / 2), orient_axis='Y')
            bpy.ops.transform.rotate(value=(np.pi), orient_axis='Y')
            bpy.ops.transform.rotate(value=(rand_rot * np.pi / 180), orient_axis='Z')

            # Set pass index for the object
            bpy.context.object.pass_index = pass_idx
            pass_idx += 1

            # Applying rigid body dynamics
            bpy.ops.rigidbody.object_add(type='ACTIVE')
            #bpy.context.object.rigid_body.mass = 10
            bpy.context.object.rigid_body.collision_shape = 'MESH'

            current_object = bpy.context.view_layer.objects.active
                
                
            if current_object and current_object.type == 'MESH':
                 # Switch to Object Mode
                 bpy.ops.object.mode_set(mode='OBJECT')
              
                 # Add a Decimate modifier to the mesh
                 modifier = current_object.modifiers.new(name='Simplify', type='DECIMATE')
              
                 # Set the decimation ratio (0.0 to 1.0, where 1.0 is no simplification)
                 modifier.ratio = 0.2 # Reduce to 50% of the original face count
              
                 # Apply the modifier
                 bpy.ops.object.modifier_apply(modifier='Simplify')
            
            # Get the active object
            current_object = bpy.context.view_layer.objects.active
            
            # Create a new material and enable nodes
            mat = bpy.data.materials.new(name='Texture')
            mat.use_nodes = True
            
            # Access the Principled BSDF node
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            
            # Create and configure the texture node
            tex_image = mat.node_tree.nodes.new('ShaderNodeTexImage')
            if len(texture_names):
                tex_path = texture_dir_path + '\\' + random.choice(texture_names)
                tex_image.image = bpy.data.images.load(filepath=tex_path)
            
            # Link the texture to the Base Color of the BSDF
            mat.node_tree.links.new(bsdf.inputs['Base Color'], tex_image.outputs['Color'])
            
            # Apply the material to the object
            if current_object:
                if len(current_object.data.materials) == 0:
                    current_object.data.materials.append(mat)
                else:
                    current_object.data.materials[0] = mat
            
            # Ensure proper UV mapping
            bpy.ops.object.mode_set(mode='EDIT')  # Switch to Edit Mode
            bpy.ops.uv.smart_project(angle_limit=66, island_margin=0.02, area_weight=1.0)

            bpy.ops.object.mode_set(mode='OBJECT')

            # Deselect all objects
            bpy.ops.object.select_all(action='DESELECT')
        

def apply_texture_to_plane(texture_dir_path):
    # Check if the plane object exists
    plane = bpy.data.objects.get('Plane')
    #print(plane.location.z)

    if not plane:
        print("Error: No object named 'Plane' found.")
        return
    
    # Create a new material with nodes enabled
    mat = bpy.data.materials.new(name='PlaneTexture')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    
    # Verify texture directory and get a random .jpg file
    if os.path.exists(texture_dir_path):
        textures = [f for f in os.listdir(texture_dir_path) if f.endswith('.jpg')]
        if textures:
            # Select a random texture file
            texture_path = os.path.join(texture_dir_path, random.choice(textures))
            #print("Applying texture:", texture_path)
            
            # Load and link texture to material
            texImage.image = bpy.data.images.load(filepath=texture_path)
            mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
            
            # Assign material to the plane object
            if len(plane.data.materials):
                plane.data.materials[0] = mat
            else:
                plane.data.materials.append(mat)
        else:
            print("No .jpg texture files found in the specified directory.")
    else:
        print("The specified texture directory does not exist.")




def start_pipeline(n_images,floor_noise,landscape_texture_dir,surface_size,oysters_model_dir,oysters_texture_dir,n_clusters,min_oyster,max_oyster,oyster_range_x,oyster_range_y,out_dir):
    
   
    
    TIME_TO_WAIT=150

    # if output dir not present, make one
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # if render output dir not present, make one
    render_out_dir = os.path.join(out_dir, "render_output")

    # set point source light
    set_light(0, 0, 10, 1)
    
    camera = bpy.context.scene.camera
    print(camera)
    
    
    
    # set camera
    camera="Camera"
    for i in range(n_images):
        delete_oysters()

        for scene in bpy.data.scenes:
            for node in scene.node_tree.nodes:
                if node.type == 'OUTPUT_FILE':
                    node.base_path = os.path.join(out_dir,str(i)+"_masks")

        add_oyster(oysters_model_dir,oysters_texture_dir, n_clusters, min_oyster, max_oyster,oyster_range_x,oyster_range_y) 
        texture_dir = "TEXTURE-DIR"
        apply_texture_to_plane(texture_dir) 

    
        # render image
        TIME_TO_WAIT=20
        for frame_count in range(TIME_TO_WAIT):
            bpy.context.scene.frame_set(frame_count)
    
        print("rendering frame:",i)
        render_img(camera,out_dir=out_dir,i=i)
  

if __name__=="__main__":
    
    # absolute path of the script
    script_path = os.path.dirname(os.path.abspath(__file__))

    # remove the last dir from path so that we are in base directory and can navigate further
    base_dir_path = script_path.split('code')[0]
    
    # output directory of saved images
    out_dir="OUTPUT-DIR-PATH"

    # landsrandom_x = random.uniform(-plane_size_x, plane_size_x)
   
    floor_noise = 100  # seabed smoothens out as the floor_noise is increased
    landscape_texture_dir = "LANDSCAPE-PATH"
    surface_size=5 # camera size
    
    

    # oysters paramteres
    oysters_model_dir = "MODELS-PATH"
    oysters_texture_dir ="MODEL-TEXTURE-PATH"
    n_clusters = 1
    min_oyster = 15
    max_oyster = 20

    # oyster dispersion range
    oyster_range_x=3
    oyster_range_y=3

    # number of random images
    n_images=1
    
    start_pipeline(n_images,floor_noise,landscape_texture_dir,surface_size,oysters_model_dir,oysters_texture_dir,n_clusters,min_oyster,max_oyster,oyster_range_x,oyster_range_y,out_dir)
    #delete_landscape()
    print("Pipeline executed.")
    
