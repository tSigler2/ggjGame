# To run the game, use this command:
# python -m GameLib.main
from GameLib.menu import Menu

if __name__ == "__main__":
    # window dimensions and start
    menu = Menu((800, 600), enable_test_level=False)  # Width: 800px, Height: 600px
    menu.run()
