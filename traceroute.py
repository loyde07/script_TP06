import argparse
import subprocess

def get_route(adresse, progressive=False, output_file=None):
    try:
        with subprocess.Popen(['tracert', adresse], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,encoding='cp850') as process:
            output_lines = []
            if progressive:
                for line in process.stdout:
                    output_lines.append(line.strip())
                    print(line.strip())
            else:
                output, errors = process.communicate()
                print(output)
                output_lines = output.splitlines()

            if output_file:
                try:
                    with open(output_file, "w", encoding="utf-8") as file:
                        file.write("\n".join(output_lines))
                except FileNotFoundError:
                    print('File not created')

    except FileNotFoundError:
        print("Erreur : La commande 'tracert' est introuvable. Assurez-vous qu'elle est disponible sur votre système.")
    except Exception as e:
        print(f"Erreur : Une erreur est survenue lors de l'exécution de la commande tracert : {e}")


def main():
    parser = argparse.ArgumentParser(description="traceroute")
    parser.add_argument("adresse",  help="adresse")
    parser.add_argument(  "-p", "--progressive", nargs="?", const=True, help="utilisation -p ou --progressive")
    parser.add_argument("-o","--output-file", help="utilisation -o ou --output-file")

    args = parser.parse_args()
    get_route(adresse=args.adresse, progressive=args.progressive, output_file=args.output_file)

if __name__ == "__main__":
    main()