from flask import Flask, jsonify, request
from main import Game
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

p1_name = 'Alex'
p2_name = 'Max'
game = Game(p1_name, p2_name)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(8), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User: {self.username}>'


@app.route('/', methods=['GET'])
def who_starts():
    """ @TODO: doc """

    return jsonify({
        'message': 'who starts',
        'player': game.starts(game.player1_hand, game.player2_hand, game.trump_card),
        'trump': game.trump_card,
        'status': 200,
    })


@app.route('/hand/<string:name>/', methods=['GET'])
def p_cards(name):
    """ @TODO: doc """

    if name == game.player1_name:
        return jsonify({
            'name': game.player1_name,
            'p1_hand': game.player1_hand,
            'card_amount': len(game.player1_hand),
        })
    elif name == game.player2_name:
        return jsonify({
            'name': game.player2_name,
            'p1_hand': game.player2_hand,
            'card_amount': len(game.player2_hand),
        })

    return jsonify(
        {
            'message': f'invalid name {name}',
            'status': 400,
        }
    )


table = []  # @TODO: write in json or some db


@app.route('/card/play/<string:player>/<string:card>/', methods=['GET'])
def put_card(player: str, card: str):
    """
    :param player: player name (Alex or Max)
    :param card: card (e.g: 9♥)
    """

    # @TODO: if player1 hasn't greater card than player2 (FUNC pick())
    # @TODO: if player1 start playing he/she can put another card if it is possible
    # @TODO: e.g:(table_cards - [9♥, J♥]; hand - [10♦, 9♣, J♦, 10♣, J♥] player can put cards with rank 9, J)

    if card in table:
        return jsonify({
            'message': 'card already on table',
            'passed_card': card,
            'table': table,
        })

    if not table:
        if player.title() == game.player1_name:
            if card in game.player1_hand:
                table.append(card)
                game.player1_hand.remove(card)  # @TODO: write in json or some db
                return jsonify({
                    'message': 'p1',
                    'card': card,
                })

        elif player.title() == game.player2_name:
            if card in game.player2_hand:
                table.append(card)
                game.player2_hand.remove(card)
                return jsonify({
                    'message': 'p2',
                    'card': card,
                })

    if table:
        if player.title() == game.player1_name:
            if card in game.player1_hand:
                if game.is_stronger(card, table):
                    table.append(card)
                    game.player1_hand.remove(card)  # @TODO: write in json or some db
                    return jsonify({
                        'message': 'p1',
                        'card': card,
                    })
                return jsonify({
                    'message': 'Alex\'s card is not greater than table[-1] card, try another card',
                    'status': 100,
                })

        elif player.title() == game.player2_name:
            if card in game.player2_hand:
                if game.is_stronger(card, table):
                    game.player2_hand.remove(card)
                    table.append(card)
                    return jsonify({
                        'message': 'p2',
                        'card': card,
                    })
                return jsonify({
                    'message': 'Max\'s card is not greater than table[-1] card, try another card',
                    'status': 100,
                })

    return jsonify({
        'message': 'card not in hand (p1/p2)',
        'status': 400,
    })


@app.route('/table/read/', methods=['GET'])
def table_cards():
    """ @TODO: doc """

    return jsonify({
        'message': 'table cards',
        'card': table,
    })


@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user_data: dict = request.form.to_dict()
        username: str = user_data.get('username')
        email: str = user_data.get('email')
        password: str = user_data.get('password')
        confirm_password: str = user_data.get('confirm_password')
        db.create_all()

        if password == confirm_password:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()

            return jsonify(
                {
                    'message': f'{user} successfully registered',
                    'status': 201,
                }
            )
        return jsonify(
            {
                'message': 'password doesnt match',
                'status': 400,
            }
        )

    return jsonify(
        {
            'message': 'register page',
            'status': 200,
        }
    )


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user_data: dict = request.form.to_dict()
        email: str = user_data.get('email')
        password: str = user_data.get('password')

        user = User.query.filter_by(email=email).first()
        print(user.password, user.email)
        # @TODO: Generate token

        if email == user.email and password == user.password:
            return jsonify(
                {
                    'message': 'successfully logged in',
                    'status': 200,
                }
            )
        return jsonify(
            {
                'message': 'password or email does not match',
                'status': 400
            }
        )

    return jsonify(
        {
            'message': 'login page',
            'status': 200,
        }
    )


@app.route('/all_users')
def all_users():
    return jsonify(
        {
            'users': f'{User.query.all()}'
        }
    )


if __name__ == '__main__':
    app.run(debug=True)
