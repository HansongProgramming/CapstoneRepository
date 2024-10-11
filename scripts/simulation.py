import bpy

def create_blood_splatter():
    # Create a particle system to simulate blood
    bpy.ops.object.particle_system_add()
    particle_system = bpy.context.object.particle_systems[-1]
    particle_system.settings.count = 1000  # Number of blood droplets
    particle_system.settings.lifetime = 50  # Lifespan of particles
    particle_system.settings.physics_type = 'NEWTON'
    particle_system.settings.gravity = -9.8  # Simulate gravity for droplets
    
    # Set particle behavior to simulate blood droplet splatter
    particle_system.settings.render_type = 'OBJECT'
    # Further customize for size, impact, etc.

# Trigger simulation
create_blood_splatter()
