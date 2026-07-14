#!/usr/bin/env python3

import subprocess
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt


console = Console()


DEFAULT_DIR = Path.home() / "Videos" / "ytp-downloads"
DOWNLOADS = Path.home() / "Downloads"


def choose_folder():

    console.print("\n[bold cyan]Download location[/bold cyan]")

    console.print(
        "1. Default"
    )

    console.print(
        f"   {DEFAULT_DIR}"
    )

    console.print(
        "2. Custom folder"
    )

    choice = IntPrompt.ask(
        "Choose",
        choices=["1", "2"],
        default=1
    )


    if choice == 1:
        return DEFAULT_DIR


    folder = Prompt.ask(
        "Folder name or path"
    )


    path = Path(folder).expanduser()


    if path.is_absolute():
        return path


    return DOWNLOADS / path



def download_playlist(url, output):

    output.mkdir(
        parents=True,
        exist_ok=True
    )


    cmd = [

        "yt-dlp",

        # Best video + best audio
        "-f",
        "bv*+ba/b",

        "--merge-output-format",
        "mp4",

        "--continue",

        "--ignore-errors",

        "--embed-thumbnail",

        "--embed-metadata",

        "--write-description",

        "--write-info-json",

        "--no-overwrites",

        "-o",

        str(
            output /
            "%(playlist_title)s/%(playlist_index)03d - %(title)s.%(ext)s"
        ),

        url
    ]


    console.print(
        "\n[yellow]Starting download...[/yellow]\n"
    )


    subprocess.run(cmd)



def main():

    console.print(
        Panel.fit(
            "[bold cyan] >>>>>>>>>>>>>>>>>>>> 🎬 YTP - YouTube Playlist Downloader[/bold cyan] <<<<<<<<<<<<<<<<<<<< "
        )
    )


    url = Prompt.ask(
        "\nPlaylist URL"
    )


    folder = choose_folder()


    console.print(
        f"\n[green]Saving to:[/green] {folder}\n"
    )


    download_playlist(
        url,
        folder
    )


    console.print(
        Panel.fit(
            "[bold green]Finished![/bold green]"
        )
    )



if __name__ == "__main__":
    main()
