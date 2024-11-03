import pygame
import random
import sys
import time
import logging

# Inizializzazione di pygame
pygame.init()

# Definire i colori
BIANCO = (255, 255, 255)
NERO = (0, 0, 0)
ROSSO = (255, 0, 0)

# Dimensioni della finestra di gioco
LARGHEZZA = 800
ALTEZZA = 600
BORDO_SUPERIORE = 50  # Spazio riservato per timer e punteggio

# Creare la finestra di gioco
finestra = pygame.display.set_mode((LARGHEZZA, ALTEZZA))
pygame.display.set_caption("Laundry Invaders")

# Caricare il nuovo logo del gioco e impostarlo come icona della finestra
logo_img = pygame.image.load("logo.png")
pygame.display.set_icon(logo_img)

# Caricare immagini
lavatrice_img = pygame.image.load("lavatrice.png")
lavatrice_img = pygame.transform.scale(lavatrice_img, (150, 150))
tessuto_img = pygame.image.load("tessuto.png")
tessuto_img = pygame.transform.scale(tessuto_img, (60, 60))
maglia_img = pygame.image.load("maglia.png")
maglia_img = pygame.transform.scale(maglia_img, (60, 60))
pantaloni_img = pygame.image.load("pantaloni.png")
pantaloni_img = pygame.transform.scale(pantaloni_img, (60, 60))
tovaglia_img = pygame.image.load("tovaglia.png")
tovaglia_img = pygame.transform.scale(tovaglia_img, (60, 60))
camicia_img = pygame.image.load("camicia.png")
camicia_img = pygame.transform.scale(camicia_img, (60, 60))

# Caricare l'immagine di sfondo
sfondo_img = pygame.image.load("sfondo.png")
sfondo_img = pygame.transform.scale(sfondo_img, (LARGHEZZA, ALTEZZA))

# Classe per rappresentare la Lavatrice
class Lavatrice(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = lavatrice_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = ALTEZZA // 2

    def update(self):
        # Controllo tramite touch o mouse
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:  # Se viene premuto il tasto sinistro del mouse o toccato lo schermo
            mouse_y = pygame.mouse.get_pos()[1]
            self.rect.y = max(BORDO_SUPERIORE + 20, min(mouse_y - self.rect.height // 2, ALTEZZA - self.rect.height - 20))

# Classe per rappresentare i Tessuti
class Tessuto(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice([tessuto_img, maglia_img, pantaloni_img, tovaglia_img, camicia_img])
        self.rect = self.image.get_rect()
        self.rect.x = LARGHEZZA - 40
        self.rect.y = random.randint(BORDO_SUPERIORE, ALTEZZA - 70)

    def update(self):
        self.rect.x -= 6 + int((time.time() - inizio_tempo) // 10)
        if tempo_trascorso > 40:
            self.rect.x -= 3
        if self.rect.x < 0:
            self.kill()  # Rimuove il tessuto una volta che lascia lo schermo

# Gruppi di sprite
lavatrice = Lavatrice()
tutti_gli_sprite = pygame.sprite.Group()
tutti_gli_sprite.add(lavatrice)

tessuti = pygame.sprite.Group()

# Creare 30 tessuti
numero_tessuti = 30

# Clock per controllare il frame rate
clock = pygame.time.Clock()

# Punteggio e timer
punteggio = 0
inizio_tempo = time.time()
durata_gioco = 90  # 90 secondi per la partita

# Font per il testo autore
font_autore = pygame.font.Font(None, 24)

# Funzione per mostrare la pagina di introduzione
def mostra_intro():
    intro_attiva = True
    while intro_attiva:
        finestra.blit(sfondo_img, (0, 0))
        # Testo del titolo
        font_titolo = pygame.font.Font("PressStart2P.ttf", 40)
        titolo = font_titolo.render("Laundry Invaders", True, BIANCO)
        finestra.blit(titolo, (LARGHEZZA // 2 - titolo.get_width() // 2, 80))
        # Testo del pulsante Play
        font_play = pygame.font.Font("PressStart2P.ttf", 50)
        play = font_play.render("Play", True, ROSSO)
        play_rect = play.get_rect(center=(LARGHEZZA // 2, 400))
        finestra.blit(play, play_rect)
        
        pygame.display.flip()

        # Gestione degli eventi
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    intro_attiva = False

# Mostrare la pagina di introduzione
mostra_intro()

# Ciclo principale del gioco
ultimo_tessuto_tempo = time.time()  # Variabile per tenere traccia dell'ultimo tessuto aggiunto
intervallo_tessuto = 2  # Intervallo in secondi tra l'apparizione di ogni tessuto

while True:
    # Gestione degli eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Controllare il tempo trascorso
    tempo_trascorso = time.time() - inizio_tempo
    if tempo_trascorso >= durata_gioco:
        # Fine del gioco
        finestra.fill(BIANCO)
        # Mostrare il titolo 'END GAME'
        font_end_game = pygame.font.Font("PressStart2P.ttf", 50)
        testo_end_game = font_end_game.render("END GAME", True, ROSSO)
        finestra.blit(testo_end_game, (LARGHEZZA // 2 - testo_end_game.get_width() // 2, 50))
        # Mostrare il messaggio 'If your score is above 130 points you may receive a reward'
        font_reward = pygame.font.Font("PressStart2P.ttf", 15)
        testo_reward_1 = font_reward.render("If your score is above 130 points", True, NERO)
        testo_reward_2 = font_reward.render("you may receive a reward", True, NERO)
        finestra.blit(testo_reward_1, (LARGHEZZA // 2 - testo_reward_1.get_width() // 2, 140))
        finestra.blit(testo_reward_2, (LARGHEZZA // 2 - testo_reward_2.get_width() // 2, 160))
        font_fine = pygame.font.Font(None, 50)
        testo_fine = font_fine.render(f"Congratulations you scored: {punteggio}", True, NERO)
        finestra.blit(testo_fine, (LARGHEZZA // 2 - testo_fine.get_width() // 2, ALTEZZA // 2 - 25))
        # Mostrare il messaggio "Created by Alessandro Ferrari" in basso
        testo_autore = font_autore.render("Created by Alessandro Ferrari", True, NERO)
        finestra.blit(testo_autore, (LARGHEZZA // 2 - testo_autore.get_width() // 2, ALTEZZA - 30))
        pygame.display.flip()
        font_replay = pygame.font.Font("PressStart2P.ttf", 25)
        testo_replay = font_replay.render("Want to play again?", True, (0, 0, 255))
        replay_rect = testo_replay.get_rect(center=(LARGHEZZA // 2, ALTEZZA - 200))
        finestra.blit(testo_replay, replay_rect)
        
        
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and replay_rect.collidepoint(event.pos):
                        inizio_tempo = time.time()
                        punteggio = 0
                        tessuti.empty()
                        tutti_gli_sprite.empty()
                        lavatrice = Lavatrice()
                        tutti_gli_sprite.add(lavatrice)
                        mostra_intro()
                        break
                

    # Aggiungere un nuovo tessuto se è trascorso abbastanza tempo e se ci sono meno di 3 tessuti contemporaneamente (dopo 40 secondi)
    max_tessuti = 3 if tempo_trascorso > 40 else numero_tessuti
    if len(tessuti) < max_tessuti and (time.time() - ultimo_tessuto_tempo) > intervallo_tessuto:
        tessuto_corrente = Tessuto()
        tessuti.add(tessuto_corrente)
        tutti_gli_sprite.add(tessuto_corrente)
        ultimo_tessuto_tempo = time.time()

    # Se il tempo è maggiore di 70 secondi, aggiungi tutti gli oggetti contemporaneamente e mantieni almeno 3 tessuti in gioco
    if tempo_trascorso > 70 and len(tessuti) < 3:
        for _ in range(3 - len(tessuti)):
            tessuto_corrente = Tessuto()
            tessuti.add(tessuto_corrente)
            tutti_gli_sprite.add(tessuto_corrente)

    # Aggiornamento degli sprite
    tutti_gli_sprite.update()

    # Controllo collisioni
    colpiti = pygame.sprite.spritecollide(lavatrice, tessuti, True)
    for colpito in colpiti:
        punteggio += 1
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(filename="laundry_invaders.log", level=logging.INFO, format="%(asctime)s - %(message)s")
        logging.info("Hai preso un tessuto!")

    finestra.blit(sfondo_img, (0, 0))
    tutti_gli_sprite.draw(finestra)

    # Disegnare il punteggio
    font_punteggio = pygame.font.Font(None, 36)
    testo_punteggio = font_punteggio.render(f"Punteggio: {punteggio}", True, BIANCO)
    finestra.blit(testo_punteggio, (LARGHEZZA - 200, 10))

    # Disegnare il timer
    tempo_rimanente = max(0, int(durata_gioco - tempo_trascorso))
    testo_timer = font_punteggio.render(f"Tempo: {tempo_rimanente}s", True, BIANCO)
    finestra.blit(testo_timer, (10, 10))

    # Aggiornare il display
    pygame.display.flip()

    # Limitare il frame rate
    clock.tick(60)

