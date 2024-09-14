import arcade

class Explosion(arcade.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Cargar las imágenes de la explosión (1.png a 12.png)
        self.textures = []
        for i in range(1, 13):  # Cargar las 12 imágenes
            texture = arcade.load_texture(f"explosion/{i}.png")
            self.textures.append(texture)
        
        self.current_texture = 0
        self.center_x = x
        self.center_y = y
        self.texture = self.textures[0]  # Iniciar con la primera textura
    
    def update(self):
        # Avanzar en la animación de la explosión
        self.current_texture += 1
        if self.current_texture < len(self.textures):
            self.texture = self.textures[self.current_texture]
        else:
            # Remover la explosión una vez que la animación termina
            self.remove_from_sprite_lists()
