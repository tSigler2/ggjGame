from menu import Menu

if __name__ == "__main__":
    # window dimensions and start
    menu = Menu((800, 600), enable_test_level=True)  # Width: 800px, Height: 600px
    menu.run()