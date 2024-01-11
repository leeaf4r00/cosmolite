from log_utils import LogController
from ui import LogWindow


def main():
    log_controller = LogController()
    # Passando log_controller como argumento
    log_window = LogWindow(log_controller)
    log_controller.set_log_window(log_window)
    log_controller.start_logging()


if __name__ == "__main__":
    main()
