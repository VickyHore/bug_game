import math, sys, pygame
from bug import *
from pygame.locals import *
from time import sleep


COLOURS = ('red', 'green', 'purple', 'blue', 'pink', 'yellow')
BG_COLOUR = (0, 0, 0)


if len(sys.argv) > 1: # use default arguments
    if sys.argv[1] == 'default':
        n_bugs = 10
        bug_col = 'red'
        splat_col = 'blue'
        bug_speed = 1
    else:
        print "Incorrect command line arguments"
        sys.exit(0)

else: # get parameters from user
    n_bugs = int(raw_input("How many bugs do you want? (1-100)\n"))
    bug_col = raw_input("Specify a bug colour (red, green, purple, blue, pink, yellow)\n")
    splat_col = raw_input("Specify a splat colour (red, green, purple, blue, pink, yellow)\n")
    if bug_col not in COLOURS or splat_col not in COLOURS:
        print "Incorrect colour(s)"
        sys.exit(0)
    bug_speed = int(raw_input("Difficulty level (1-10)\n"))


# set up: window
pygame.init()
size = width, height = 1024, 768
window = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# create bugs
bugs = []
for n in range(n_bugs):
    bugs.append(Bug(size, bug_col, splat_col, bug_speed))


# play game
while True:
    clock.tick(30) # this make the loop below run every 1/30 of a second

    for event in pygame.event.get():
        if hasattr(event, 'key'): # ESC kills the game
            if event.key == K_ESCAPE:
                sys.exit(0)

        if event.type == pygame.MOUSEBUTTONUP: # mouse-click on bugs
            mouse = pygame.mouse.get_pos()

            for i, bug in enumerate(bugs):
                bug.update_status(mouse)

    window.fill(BG_COLOUR)

    for i, bug in enumerate(bugs): # update bug positions
        bug.move()
        image = pygame.transform.rotozoom(bug.image, 270 - bug.ang, 1)
        rect = image.get_rect()
        rect.center = bug.pos
        window.blit(image, rect)

    # behaviour at end of game
    num_bugs_alive = sum([bug.status=="alive" for bug in bugs])
    if num_bugs_alive == 0:
        font = pygame.font.Font(None, 100)
        label = font.render("You win!!", True, (238, 58, 140))
        window.blit(label, (width/2-150, height/2-100))
        pygame.display.flip()
        sleep(2)
        sys.exit(0)

    pygame.display.flip()

