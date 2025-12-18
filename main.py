from neon_rain_generator_v3 import NeonRainGenerator

if __name__ == "__main__":
    gradient_colors = [
        [(238, 38, 95), (168, 28, 117), (61, 16, 63)], # rose -> violet foncé
        [(0, 255, 255), (0, 128, 255), (0, 0, 128)],   # cyan -> bleu
        [(255, 255, 0), (255, 128, 0), (255, 0, 0)],   # jaune -> orange -> rouge
        [(0, 255, 0), (0, 128, 64), (0, 32, 0)],       # vert -> vert foncé
        [(255, 0, 255), (128, 0, 128), (32, 0, 64)]    # magenta -> violet foncé
    ]
    generator = NeonRainGenerator(
        width=2560,
        height=1440,
        num_stars=200,
        trail_length=50,
        speed=15,
        angle=45,
        frames=300,
        background_color=(0, 0, 0),
        gradient_colors=gradient_colors
    )
    generator.generate_frames()
    generator.save_gif("neon_rain.gif", duration=10, open_after_creation=True)