
import argparse
import subprocess
import re
import platform

import socket

def resolve_url_to_ip(url_or_ip):
    try:
        # Vérifie si c'est déjà une adresse IP
        socket.inet_aton(url_or_ip)
        return url_or_ip  # C'est une adresse IP valide
    except socket.error:
        try:
            # Résout l'URL en adresse IP
            return socket.gethostbyname(url_or_ip)
        except socket.gaierror:
            print(f"Erreur : Impossible de résoudre l'URL {url_or_ip}")
            return None

def traceroute(url_or_ip, progressive=False, output_file=None):
    """
    Effectue un traceroute vers une URL ou une adresse IP.

    Args:
        url_or_ip (str): URL ou adresse IP cible.
        progressive (bool): Affiche les résultats au fur et à mesure si True.
        output_file (str): Nom du fichier pour enregistrer les résultats (facultatif).
    """
    # Détection du système d'exploitation
    is_windows = platform.system().lower() == "windows"
    command = ["tracert", url_or_ip] if is_windows else ["traceroute", url_or_ip]
    result_lines = []

    try:
        if progressive:
            # Mode progressif : Affichage au fur et à mesure
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            file = open(output_file, "w") if output_file else None  # Ouvre le fichier si spécifié
            try:
                for line in process.stdout:
                    ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                    if ip_match:
                        ip = ip_match.group(1)
                        print(ip)  # Affichage progressif
                        result_lines.append(ip)
                        if file:  # Écriture progressive dans le fichier
                            file.write(ip + "\n")
            finally:
                if file:  # Ferme le fichier uniquement s'il est ouvert
                    file.close()

        else:
            # Mode par défaut : Affichage après exécution complète
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            for line in result.stdout.splitlines():
                ip_match = re.search(r"(\d+\.\d+\.\d+\.\d+)", line)
                if ip_match:
                    ip = ip_match.group(1)
                    result_lines.append(ip)

            # Affichage des résultats après exécution complète
            for ip in result_lines:
                print(ip)

            # Enregistrement dans un fichier si spécifié
            if output_file:
                with open(output_file, "w") as file:
                    file.write("\n".join(result_lines) + "\n")

    except FileNotFoundError:
        print(
            f"Erreur : La commande '{'tracert' if is_windows else 'traceroute'}' n'est pas disponible sur ce système.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de la commande : {e}")
    except Exception as e:
        print(f"Erreur inattendue : {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traceroute Script TP6")
    parser.add_argument("url_or_ip", help="URL ou adresse IP à tracer")
    parser.add_argument("-p", "--progressive", action="store_true", help="Affiche les IPs des sauts au fur et à mesure")
    parser.add_argument("-o", "--output-file", help="Nom du fichier pour enregistrer les résultats")
    args = parser.parse_args()

    resolved_ip = resolve_url_to_ip(args.url_or_ip)
    if not resolved_ip:
        exit(1)  # Quitte si l'URL n'est pas résolue
    traceroute(resolved_ip, args.progressive, args.output_file)