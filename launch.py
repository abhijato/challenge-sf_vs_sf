import chess
from chess import engine
from chess import pgn
import smtplib, ssl
import threading

def PlayGame():
    eng = engine.SimpleEngine.popen_uci("engines/sf")
    while True:
        board = chess.Board()
        game = chess.pgn.Game()
        while not board.is_game_over():
            result = eng.play(board, engine.Limit(time=15))
            board.push(result.move)
        if not board.result()=='1/2-1/2':
            game.add_line(board.move_stack)
            game.headers["Event"]="Stockfish VS Stockfish(15s)"
            game.headers["Site"]="Heroku's server"
            game.headers["White"]="Stockfish 12"
            game.headers["Black"]="Stockfish 12"
            game.headers["Result"]=board.result()
            exporter = pgn.StringExporter(headers=True, variations=True, comments=True)
            pgn_string = game.accept(exporter)
            print(pgn_string)
            port = 465  # For SSL
            smtp_server = "smtp.gmail.com"
            sender_email = "lichessbotall@gmail.com"  # Enter your address
            receiver_email = "abhijato.chatterjee@gmail.com"  # Enter receiver address
            password = "lichess api token"

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(sender_email, receiver_email, pgn_string)


if __name__=="__main__":
    Game1=threading.Thread(target=PlayGame,args=())
    Game2=threading.Thread(target=PlayGame,args=())
    Game3=threading.Thread(target=PlayGame,args=())
    Game1.start()
    Game2.start()
    Game3.start()
