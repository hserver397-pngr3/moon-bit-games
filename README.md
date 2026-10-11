# Moonbit Games

Retro pixel arcade in your browser. Play **Flappy Pixel**, **Pixel Snake** and **Pixel Chess**, with sound effects, on a pixel-art indie game website.

## Games

| Game | Controls |
| --- | --- |
| Flappy Pixel | Space, click or tap to flap |
| Pixel Snake | Arrow keys / WASD, or swipe on a phone |
| Pixel Chess | Click a piece, then click a square. Play the computer or a friend |

Chess does not support castling or en passant yet. Pawns promote to queens automatically.

## How to run

You need [Python 3](https://www.python.org/downloads/) installed. No other packages are required.

1. Download or clone this repository.

   ```
   git clone https://github.com/YOUR-USERNAME/moonbit-games.git
   cd moonbit-games
   ```

2. Start the server.

   ```
   python server.py
   ```

   On some systems the command is `python3 server.py`.

3. Your browser opens at **http://localhost:8000**. If it does not, open that link yourself.

4. Press `Ctrl + C` in the terminal to stop the server.

If port 8000 is busy, the server tries 8001 to 8009 and prints the correct link in the terminal.

## Notes

- `server.py` has the whole website built in, so you only need that one file.
- `index.html` is the same website as a plain page. You can open it directly or host it with GitHub Pages.
- The pixel fonts load from Google Fonts, so you need internet for them. Without it, a plain monospace font is used.
- Sound uses the browser's built-in audio. Use the **Sound** button in the game window to turn it off.

## Tech

HTML, CSS and JavaScript (canvas and Web Audio), served by Python's built-in `http.server`.

==================================================================================================

# moon-bit-games
Here's one you can paste into the description box:  **Retro pixel indie game website with playable Flappy Bird, Snake and Chess, built with HTML, JavaScript and a Python server.**  A shorter version if you want it:  **Retro pixel arcade: Flappy, Snake and Chess in your browser.**
