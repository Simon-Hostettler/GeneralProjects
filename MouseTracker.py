from pynput import mouse

with open("Mouseevents.txt", "a") as f:
    def on_move(x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))
        f.write("%d, %d" % (x, y) + ", ")

    def on_click(x, y, button, pressed):
        with open("Mouseevents.txt", "a") as f:
            if pressed:
                print('{0} at {1}'.format(
                    'Pressed',
                    (x, y)))
                f.write("%d, %d" % (x, y) + ", ")
            if not pressed:
                pass

    def on_scroll(x, y, dx, dy):
        pass

    with mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll) as listener:
        listener.join()