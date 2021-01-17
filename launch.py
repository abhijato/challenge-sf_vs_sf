import chess
from chess import engine
from chess import pgn
import smtplib, ssl

def PlayGame():
    eng = engine.SimpleEngine.popen_uci("engines/sf")
    while True:
        board = chess.Board()
        game = chess.pgn.Game()
        while not board.is_game_over():
            result = eng.play(board, engine.Limit(time=0.1))
            board.push(result.move)
        game.add_line(board.move_stack)
        exporter = pgn.StringExporter(headers=True, variations=True, comments=True)
        pgn_string = game.accept(exporter)
        print(pgn_string)

        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "lichessbotall@gmail.com"  # Enter your address
        receiver_email = "abhijato.chatterjee@gmail.com"  # Enter receiver address
        password = "lichess bot api"

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, pgn_string)

if __name__=="__main__":
    PlayGame()
