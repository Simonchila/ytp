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

    console.print("1. Default")
    console.print(f"   {DEFAULT_DIR}")

    console.print("2. Custom folder")

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



def download_playlist(url, output, start):

    output.mkdir(
        parents=True,
        exist_ok=True
    )


    cmd = [

        "yt-dlp",

        # Best video + best audio
        "-f",
        "bestvideo+bestaudio/best",

        # Always output mp4
        "--merge-output-format",
        "mp4",

        # Start position in playlist
        "--playlist-start",
        str(start),

        # Resume unfinished downloads
        "--continue",

        # Continue even if one video fails
        "--ignore-errors",

        # Don't download extra files
        "--no-write-info-json",
        "--no-write-thumbnail",

        # Don't overwrite existing videos
        "--no-overwrites",

        # Organize playlist
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
            "[bold cyan]"
            ">>>>>>>>>>>>>>>>>>>> 🎬 YTP - YouTube Playlist Downloader "
            "<<<<<<<<<<<<<<<<<<<<"
            "[/bold cyan]"
        )
    )


    url = Prompt.ask(
        "\nPlaylist URL"
    )


    folder = choose_folder()


    start = IntPrompt.ask(
        "\nStart downloading from video number",
        default=1
    )


    console.print(
        f"\n[green]Saving to:[/green] {folder}"
    )

    console.print(
        f"[green]Starting from video:[/green] {start}\n"
    )


    download_playlist(
        url,
        folder,
        start
    )


    console.print(
        Panel.fit(
            "[bold green]Finished![/bold green]"
        )
    )



if __name__ == "__main__":
    main()