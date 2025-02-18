from pygame import font, draw

from utils.constants import SCREEN_SETTINGS, COLORS


def drawLife(screen, player, enemy):
    fuente = font.Font(None, 30)
    fuenteVida = font.Font(None, 20)

    player_hp_percent = player.life / player.max_life
    enemy_hp_percent = enemy.life / enemy.max_life

    player_box_x, player_box_y = SCREEN_SETTINGS.WIDTH - 220, SCREEN_SETTINGS.HEIGHT - 245
    enemy_box_x, enemy_box_y = 20, 20

    draw.rect(screen, COLORS.WHITE, (enemy_box_x, enemy_box_y, 200, 80))
    draw.rect(screen, COLORS.BLACK, (enemy_box_x, enemy_box_y, 200, 80), 3)

    enemy_text = fuente.render(f"{enemy.name}", True, COLORS.BLACK)
    screen.blit(enemy_text, (enemy_box_x + 10, enemy_box_y + 10))

    draw.rect(screen, COLORS.RED, (enemy_box_x + 10, enemy_box_y + 40, 180, 10))
    draw.rect(screen, COLORS.GREEN, (enemy_box_x + 10, enemy_box_y + 40, int(180 * enemy_hp_percent), 10))

    enemy_life = fuenteVida.render(f"{enemy.life}/{enemy.max_life}", True, COLORS.BLACK)
    screen.blit(enemy_life, (enemy_box_x + 10, enemy_box_y + 60))

    draw.rect(screen, COLORS.WHITE, (player_box_x, player_box_y, 200, 80))
    draw.rect(screen, COLORS.BLACK, (player_box_x, player_box_y, 200, 80), 3)

    player_text = fuente.render(f"{player.name}", True, COLORS.BLACK)
    screen.blit(player_text, (player_box_x + 10, player_box_y + 10))

    draw.rect(screen, COLORS.RED, (player_box_x + 10, player_box_y + 40, 180, 10))
    draw.rect(screen, COLORS.GREEN, (player_box_x + 10, player_box_y + 40, int(180 * player_hp_percent), 10))

    player_life = fuenteVida.render(f"{player.life}/{player.max_life}", True, COLORS.BLACK)
    screen.blit(player_life, (player_box_x + 10, player_box_y + 60))
