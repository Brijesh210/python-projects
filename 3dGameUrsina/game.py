from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
blocks = {
    1: load_texture('assets/grass_block.png'),
    2: load_texture('assets/stone_block.png'),
    3: load_texture('assets/brick_block.png'),
    4: load_texture('assets/dirt_block.png')}

sky_texture = load_texture('assets/skybox.png')
arm_texture = load_texture('assets/arm_texture.png')
selectedBlock = 1


def update():
    global selectedBlock
    if held_keys['left mouse'] or held_keys['right mouse']:
        hand.active()
    else:
        hand.passive()
    if held_keys['1']: selectedBlock = 1
    if held_keys['2']: selectedBlock = 2
    if held_keys['3']: selectedBlock = 3
    if held_keys['4']: selectedBlock = 4


class Voxel(Button):
    def __init__(self, position=(0, 0, 0), block=blocks.get(0)):
        super().__init__(
            parent=scene,
            position=position,
            model='assets/block',
            origin_y=0.5,
            texture=block,
            color=color.color(0, 0, random.uniform(0.9, 1)),
            scale=0.5)

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                i = len(blocks) - 1 if selectedBlock >= len(blocks) else selectedBlock
                pos = sqrt(
                    pow(self.position.x - player.position.x, 2) +
                    pow(self.position.y - player.position.y, 2) +
                    pow(self.position.z - player.position.x, 2))
                if pos > 10:
                    return
                Voxel(position=self.position + mouse.normal, block=blocks.get(i))
            if key == 'right mouse down':
                destroy(self)


class Sky(Entity):
    def __init__(self):
        super().__init__(
            parent=scene,
            model='sphere',
            texture=sky_texture,
            scale=150,
            double_sided=True)


class Hand(Entity):
    def __init__(self):
        super().__init__(
            parent=camera.ui,
            model='assets/arm',
            texture=arm_texture,
            scale=0.2,
            rotation=Vec3(150, -10, 0),
            position=Vec2(0.4, -0.6))

    def active(self):
        self.position = Vec2(0.3, -0.5)

    def passive(self):
        self.position = Vec2(0.4, -0.6)


for z in range(20):
    for x in range(20):
        voxel = Voxel(position=(x, 0, z))

player = FirstPersonController()
sky = Sky()
hand = Hand()
window.exit_button.visible = True
app.run()
