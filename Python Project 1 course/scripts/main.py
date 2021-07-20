
"""
    Основной скрипт.
    Автор: Шайкин К.А.
"""
import os
import gui as gui
os.chdir("d:/work/")


def main():
    """
    main
    Автор: Шайкин К.А.
    Запуск приложения
    """
    gui.create_app()
    gui.mainloop()


if __name__ == '__main__':
    main()
