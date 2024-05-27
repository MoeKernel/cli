import subprocess
from datetime import datetime, timezone
import pytz
from os import system

def time_say():
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    utc_now = datetime.now(timezone.utc)
    brasilia_now = utc_now.astimezone(brasilia_tz)
    now = brasilia_now.strftime('%H:%M')
    print(f"⏱︎ {COLOR_RESET}Time: ", now)

    morning_start = "06:00"
    afternoon_start = "12:00"
    evening_start = "17:00"
    night_start = "20:00"

    if now >= night_start or now < morning_start:
        say = "Good Night!"
        return say
    elif afternoon_start <= now < evening_start:
        say = "Good Afternoon"
        return say
    elif morning_start <= now < afternoon_start:
        say = "Good Morning!"
        return say
    else:
        say = "Good Evening!"
        return say


def clear():
    """Clear of the OutPut."""
    system("clear")


def define_colors():
    global COLOR_RESET, COLOR_PURPLE, COLOR_YELLOW, COLOR_GREEN, COLOR_RED, COLOR_CYAN

    COLOR_RESET = "\033[0m"
    COLOR_PURPLE = "\033[95m"
    COLOR_YELLOW = "\033[93m"
    COLOR_GREEN = "\033[92m"
    COLOR_RED = "\033[91m"
    COLOR_CYAN = "\033[96m"


def menu():
    clear()
    define_colors()

    print(COLOR_PURPLE)
    print("  ☆彡(ノ^ ^)ノ     Waifu Git Helper         ヽ(^ ^ヽ)☆彡")
    print("  ★~(◠‿◕✿)        1. CherryPick & Push           ✿◕‿◠)~★")
    print("  ★~(◠‿◕✿)        2. Multiple CherryPick & Push  ✿◕‿◠)~★")
    print("  ★~(◠‿◕✿)        3. Create Patch                ✿◕‿◠)~★")
    print("  ★~(◠‿◕✿)        4. Apply Patch                 ✿◕‿◠)~★")
    print("  ★~(◠‿◕✿)        5. Install Packages            ✿◕‿◠)~★")
    print("  ★~(◠‿◕✿)        6. Exit                        ✿◕‿◠)~★")
    print(COLOR_RESET)

    choice = input(f"{COLOR_RESET}{time_say()} {COLOR_YELLOW}Akari-Sama{COLOR_RESET}.\n\n{COLOR_RESET}escolha o que deseja fazer-nyan {COLOR_CYAN}")

    if choice == '1':
        commit_hash_push()
    elif choice == '2':
        commit_hashes_push()
    elif choice == '3':
        create_patch_hash()
    elif choice == '4':
        apply_patch()
    elif choice == '5':
        install_packages()
    elif choice == '6':
        print(COLOR_GREEN + "Goodbye! Have a nice day! ｡◕‿◕｡" + COLOR_RESET)
        exit()
    else:
        print(COLOR_RED + "Invalid choice! Please choose again." + COLOR_RESET)
        menu()


def run_command(command):
    """Executa um comando no shell e retorna a saída."""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    return result


def commit_in_branch(commit_hash, branch):
    """Verifica se o commit está presente no histórico da branch."""
    result = run_command(f"git log {branch} --pretty=format:%H")
    return commit_hash in result.stdout.split()


def apply_commit_to_branch(commit_hash, branch):
    if commit_in_branch(commit_hash, branch):
        print(COLOR_YELLOW + f"Commit {commit_hash} já está presente na branch {branch}. Fazendo push..." + COLOR_RESET)
        push_result = run_command(f"git push origin {branch}")
        if push_result.returncode == 0:
            print(COLOR_GREEN + f"Branch {branch} enviada com sucesso." + COLOR_RESET)
        else:
            print(COLOR_RED + f"Erro ao enviar a branch {branch}." + COLOR_RESET)
        return

    checkout_result = run_command(f"git checkout {branch}")
    if checkout_result.returncode != 0:
        print(COLOR_RED + f"Erro ao mudar para a branch {branch}. Pulando para a próxima branch." + COLOR_RESET)
        return

    cherry_pick_result = run_command(f"git cherry-pick {commit_hash}")
    if cherry_pick_result.returncode == 0:
        print(COLOR_GREEN + f"Cherry-pick aplicado com sucesso na branch {branch}" + COLOR_RESET)
        push_result = run_command(f"git push origin {branch}")
        if push_result.returncode == 0:
            print(COLOR_GREEN + f"Branch {branch} enviada com sucesso." + COLOR_RESET)
        else:
            print(COLOR_RED + f"Erro ao enviar a branch {branch}." + COLOR_RESET)
    else:
        print(COLOR_RED + f"Erro ao aplicar cherry-pick na branch {branch}. Tentando resolver conflitos." + COLOR_RESET)
        run_command("git cherry-pick --abort")
        print(COLOR_RED + f"Cherry-pick abortado na branch {branch} devido a conflitos." + COLOR_RESET)


def commit_hash_push():
    while True:
        commit_hash = input(COLOR_RESET + "Commit hash: ").strip()
        if commit_hash:
            break
        else:
            print(COLOR_RED + "Commit hash cannot be empty. Please enter a valid commit hash." + COLOR_RESET)

    branches = [
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "without-ksu"
    ]

    for branch in branches:
        print(COLOR_CYAN + f"Aplicando cherry-pick na branch {branch}" + COLOR_RESET)
        apply_commit_to_branch(commit_hash, branch)

    run_command("git checkout fourteen")


def commit_hashes_push():
    while True:
        commit_hashes_input = input(COLOR_RESET + "Enter commit hashes separated by space (or 'done' to finish): ").strip()
        if commit_hashes_input.lower() == 'done':
            print(COLOR_RED + "No commit hashes entered. Returning to menu." + COLOR_RESET)
            menu()
            return
        elif commit_hashes_input:
            commit_hashes = commit_hashes_input.split()
            break
        else:
            print(COLOR_RED + "Commit hashes cannot be empty. Please enter valid commit hashes." + COLOR_RESET)

    branches = [
        "fourteen",
        "fourteen_dynamic_noksu",
        "fourteen_dynamic",
        "without-ksu"
    ]

    for branch in branches:
        print(COLOR_CYAN + f"Aplicando cherry-pick na branch {branch}" + COLOR_RESET)
        for commit_hash in commit_hashes:
            apply_commit_to_branch(commit_hash, branch)

    run_command("git checkout fourteen")


def create_patch_hash():
    hash = str(input(COLOR_RESET + "Commit hash: ")).strip()
    name_patch = str(input(COLOR_RESET + "Name of the patch? "))
    result = run_command(f"git diff {hash}^! > {name_patch}.patch")

    if result.returncode == 0:
        print(COLOR_GREEN + f"{name_patch}.patch criado com sucesso." + COLOR_RESET)
    else:
        print(COLOR_YELLOW + f"Ocorreu algum erro, tente novamente...")


def apply_patch():
    path = str(input(COLOR_RESET + "Path: "))
    patch = str(input("Patch: "))
    result = run_command(COLOR_RESET + f"patch {path} < {patch}.patch")

    if result.returncode == 0:
        print(COLOR_GREEN + f"Apply {patch} with successfully!" + COLOR_RESET)
    else:
        print(COLOR_RED + f"Error to apply {patch}" + COLOR_RESET)


def detect_os(os_name):
    os_name = run_command("cat /etc/os-release | grep -oP '(?<=^ID=).+'").stdout
    return os_name


def install_packages():
    """Install Packages Utils."""
    choice = str(input(COLOR_RESET + "Sir,\nU want the really install packages? " + COLOR_CYAN))
    yes = ["yes", "yeah", "yup", "yeah"]

    for y in yes:
        if y in choice:
            pkgs = ["bc", "neovim"] # add more packages
            for pkg in pkgs:

                if detect_os("archarm") or detect_os("arch"):
                    print(COLOR_YELLOW + "Installing the packages, wait...")
                    result = run_command(f"pacman -S {pkg} --noconfirm")
                    if result.returncode == 0:
                        print(COLOR_GREEN + f"Installed Package {pkg} (:")
                    else:
                        print(COLOR_RED + "ARCH! ERORR: I don't know, I just know that an error occurred... hehe")

                elif detect_os("ubuntu") or detect_os("Ubuntu"):
                    print(COLOR_YELLOW + "Installing the packages, wait...")
                    result = run_command(f"sudo apt install {pkg} -y")
                    if result.returncode == 0:
                        print(COLOR_GREEN + f"Installed Package {pkg} (:")
                    else:
                        print(COLOR_RED + "UBUNTU! ERROR: I don't know, I just know that an error occurred... hehe")

                else:
                    print(COLOR_RED + "Occurred an Error.")

        elif "" in choice:
            menu()


if __name__ == "__main__":
    menu()

