import subprocess
import os


def create_shortcut():
    # Defina o caminho relativo para o cosmolite_app.py
    cosmolite_app_path = os.path.join("cosmolite_app.py")

    try:
        subprocess.Popen(["python", cosmolite_app_path])
    except subprocess.CalledProcessError as error:
        print(f"Erro ao abrir o arquivo cosmolite_app.py: {error}")
    except Exception as e:
        print(f"Erro desconhecido ao abrir o arquivo cosmolite_app.py: {e}")


def main():
    create_shortcut()


if __name__ == "__main__":
    main()
