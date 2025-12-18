from PIL import Image
from PIL import ImageDraw
from shooting_star import ShootingStar
import random
import os

class NeonRainGenerator:
    def __init__(self, width=1920, height=1080, num_stars=100, trail_length=50, speed=15, angle=45, frames=240, background_color=(0, 0, 0), gradient_colors=None):
        """
        Initialise le générateur de pluie d'étoiles filantes.
        
        Args:
            width (int): Largeur de l'image.
            height (int): Hauteur de l'image.
            num_stars (int): Nombre d'étoiles filantes.
            trail_length (int): Longueur de la traînée des étoiles filantes.
            speed (int): Vitesse des étoiles filantes.
            angle (int): Angle de la traînée en degrés.
            frames (int): Nombre de frames à générer.
            background_color (tuple): Couleur de fond (R, G, B).
        """
        self.width = width
        self.height = height
        self.num_stars = num_stars
        self.trail_length = trail_length
        self.speed = speed
        self.angle = angle
        self.frames = frames
        self.background_color = background_color
        self.palette = [
            (255, 0, 255),   # Magenta
            (0, 255, 255),   # Cyan
            (0, 255, 0),     # Vert
            (255, 255, 0),   # Jaune
            (255, 165, 0),   # Orange
            (255, 0, 0)      # Rouge
        ]
        # Liste de dégradés (liste de listes de couleurs)
        self.gradient_colors = gradient_colors if gradient_colors is not None else [
            [(238, 38, 95), (168, 28, 117), (61, 16, 63)], # rose -> violet foncé
            [(0, 255, 255), (0, 128, 255), (0, 0, 128)],   # cyan -> bleu
            [(255, 255, 0), (255, 128, 0), (255, 0, 0)],   # jaune -> orange -> rouge
            [(0, 255, 0), (0, 128, 64), (0, 32, 0)],       # vert -> vert foncé
            [(255, 0, 255), (128, 0, 128), (32, 0, 64)]    # magenta -> violet foncé
        ]
        self.shooting_stars = self.create_shooting_stars()
        self.frames_list = []

    def max_distance_loop(self, star_speed):
        """
        Calcule la distance maximale qu'une étoile filante peut parcourir en une boucle complète.
        Utile pour positionner les étoiles filantes au départ.
        """
        import math
        angle_rad = math.radians(self.angle)
        dx = star_speed * math.cos(angle_rad)
        dy = star_speed * math.sin(angle_rad)
        trail_length_x = self.trail_length * math.cos(angle_rad)
        trail_length_y = self.trail_length * math.sin(angle_rad)
        distance_x = abs(dx * self.frames + trail_length_x)
        distance_y = abs(dy * self.frames + trail_length_y)
        return distance_x, distance_y

    def create_shooting_stars(self):
        """
        Crée une liste d'étoiles filantes avec des positions et des couleurs aléatoires,
        en garantissant une boucle parfaite (position initiale = position finale).
        """
        stars = []
        for _ in range(self.num_stars):
            # Choisir une position visible aléatoire sur l'image
            x_rand = random.randint(-round(self.width//1.5), self.width + 100)
            y_rand = random.randint(-round(self.height//1.5), self.height + 100)
            grad = random.choice(self.gradient_colors)
            star_speed = random.uniform(self.speed*0.75, self.speed * 1.25)
            max_dist = self.max_distance_loop(star_speed)
            star = ShootingStar(
                head_color=grad[0],
                head_position=(x_rand, y_rand),
                trail_length=self.trail_length,
                trail_angle=self.angle,
                speed=star_speed,
                head_size=6,
                trail_width=4,
                max_distance=max_dist,
                gradient=grad
            )
            stars.append(star)
        return stars
    
    def set_random_position(self, width, height, max_offset=200):
        """
        Définit une position aléatoire pour la tête de l'étoile filante en dehors de l'écran.

        Args:
            width (int): Largeur de l'écran.
            height (int): Hauteur de l'écran.
            max_offset (int): Décalage maximal par rapport à l'écran.
        """
        x = random.randint(-max_offset, width)
        y = random.randint(-max_offset, height)
        return (x, y)

    def generate_frames(self):
        """
        Génère les frames de la pluie d'étoiles filantes.
        """
        # Génère les frames de la pluie d'étoiles filantes.
        for i in range(self.frames):
            # Affiche la barre de progression
            progress = int((i + 1) / self.frames * 40)
            bar = '[' + '#' * progress + '-' * (40 - progress) + ']'
            print(f"\rGénération des frames {bar} {i+1}/{self.frames}", end='', flush=True)
            # Création de l'image avec alpha
            img = Image.new("RGBA", (self.width, self.height), self.background_color + (255,))
            # Dessine chaque étoile filante sur une image temporaire avec alpha
            for star in self.shooting_stars:
                temp = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
                temp_draw = ImageDraw.Draw(temp)
                dx, dy = star.move()
                head_x, head_y = star.head_position
                grad = star.gradient
                for j in range(star.trail_length):
                    t = j / star.trail_length
                    if t < 0.5:
                        local_t = t / 0.5
                        c0, c1 = grad[0], grad[1]
                        grad_color = tuple(
                            int(c0[k] * (1 - local_t) + c1[k] * local_t)
                            for k in range(3)
                        )
                    else:
                        local_t = (t - 0.5) / 0.5
                        c0, c1 = grad[1], grad[2]
                        grad_color = tuple(
                            int(c0[k] * (1 - local_t) + c1[k] * local_t)
                            for k in range(3)
                        )
                    # Ajout du fondu en transparence sur la fin de la traînée (dernier tiers)
                    fade_start = 0.7
                    alpha = 255
                    if t > fade_start:
                        fade_t = (t - fade_start) / (1 - fade_start)
                        alpha = int(255 * (1 - fade_t))
                    temp_draw.line(
                        [
                            (head_x - j * dx, head_y - j * dy),
                            (head_x - (j + 1) * dx, head_y - (j + 1) * dy)
                        ],
                        fill=grad_color + (alpha,),
                        width=star.trail_width
                    )
                # Dessiner la tête (toujours opaque)
                r = star.head_size / 2
                temp_draw.ellipse(
                    [
                        (head_x - r, head_y - r),
                        (head_x + r, head_y + r)
                    ],
                    fill=star.head_color + (255,)
                )
                # Fusionne la traînée sur l'image principale
                img = Image.alpha_composite(img, temp)
                # Calcul de la position de la fin de la traînée avec la méthode get_tail_position()
                tail_x, tail_y = star.get_tail_position()
                if tail_x > self.width or tail_y > self.height:
                    star.reset()
            # Convertit en RGB pour la sauvegarde GIF (perte alpha, mais effet fondu conservé)
            self.frames_list.append(img.convert("RGB"))
        return self.frames_list

    def save_gif(self, output_path="./neon_rain.gif", duration=10, open_after_creation=False):
        """
        Sauvegarde les frames générées en un GIF animé.
        
        Args:
            output_path (str): Chemin de sauvegarde du GIF.
            duration (int): Durée de la boucle en secondes.
        """
        if not self.frames_list:
            raise ValueError("Aucune frame générée. Veuillez appeler generate_frames() avant de sauvegarder le GIF.")
        # Si le fichier existe déjà, rajoute un suffixe numérique pour éviter d'écraser
        base, ext = os.path.splitext(output_path)
        counter = 1
        while os.path.exists(output_path):
            output_path = f"{base}_{counter}{ext}"
            counter += 1
        print("\nSauvegarde du GIF...")
        self.frames_list[0].save(output_path, save_all=True, append_images=self.frames_list[1:], duration=(duration * 1000)/self.frames, loop=0)
        abs_path = os.path.abspath(output_path)
        print(f"\n✅ GIF généré : {abs_path}")
        if open_after_creation:
            # Ouvre le GIF généré avec la visionneuse d'images par défaut (Windows)
            import subprocess
            subprocess.Popen(['start', abs_path], shell=True)