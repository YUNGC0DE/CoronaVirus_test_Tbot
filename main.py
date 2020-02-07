import configs
import telebot

bot = telebot.TeleBot(configs.Token)

users = [{'id': 'no', 'state': 'no', 'score' : 'no'}]


def change_state(state, id):
    for user in users:
        if user['id'] == id:
            user['state'] = state


def change_score(id):
    for user in users:
        if user['id'] == id:
            user['score'] += 100


def drop_score(id):
    for user in users:
        if user['id'] == id:
            user['score'] = 0


@bot.message_handler(commands=['start'])
def list(message):
    print(bot.get_chat(message.chat.id).last_name)
    user_dict = {
        'id': message.chat.id,
        'state': 0,
        'score': 0
    }
    is_new = 1
    bot.send_message(message.chat.id,
                     "<b>Коронавирус надвигается, пройди этот тест, чтобы узнать свои шансы выжить после наступления апокалипсиса</b>",
                     parse_mode='html')
    for user in users:
        if user['id'] == message.chat.id:
            is_new = 0
    if is_new == 1:
        users.append(user_dict)
        print('new')
    change_state(1, message.chat.id)
    bot.send_message(message.chat.id, "<b>Пройти тест?</b>", parse_mode='html')


@bot.message_handler(content_types=['text'])
def get_message(message):
    id = message.chat.id
    for user in users:
        if user['id'] == id:
            if user['state'] == 0:
                bot.send_message(message.chat.id, "Введи /start чтобы пройти тест снова")
            if user['state'] == 1:
                if message.text == 'Да' or message.text == 'да':
                    bot.send_message(message.chat.id, 'Отлично! Первый вопрос')
                    change_state(2, message.chat.id)
                    question_one(message.chat.id)
                    break
                elif message.text == 'Нет' or message.text == 'нет':
                    bot.send_message(message.chat.id, "Ты умрешь первым!")
                    change_state(0, message.chat.id)
                    break
                else:
                    bot.send_message(message.chat.id, "Необходимо ввести Да или Нет")
            if user['state'] == 2:
                if message.text == '1':
                    bot.send_message(message.chat.id, 'Отлично! Второй вопрос')
                    change_state(3, message.chat.id)
                    question_two(message.chat.id)
                    break
                elif message.text == '2':
                    change_score(message.chat.id)
                    bot.send_message(message.chat.id, 'Отлично! Второй вопрос')
                    change_state(3, message.chat.id)
                    question_two(message.chat.id)
                    break
                else:
                    bot.send_message(message.chat.id, "Необходимо ввести 1 или 2")
            if user['state'] == 3:
                if message.text == '1':
                    bot.send_message(message.chat.id, 'Отлично! Третий вопрос')
                    change_state(4, message.chat.id)
                    question_three(message.chat.id)
                    break
                elif message.text == '2':
                    change_score(message.chat.id)
                    bot.send_message(message.chat.id, 'Отлично! Третий вопрос')
                    change_state(4, message.chat.id)
                    question_three(message.chat.id)
                    break
                else:
                    bot.send_message(message.chat.id, "Необходимо ввести 1 или 2")
            if user['state'] == 4:
                if message.text == '1':
                    bot.send_message(message.chat.id, 'Отлично! Четвертый вопрос')
                    change_state(5, message.chat.id)
                    question_four(message.chat.id)
                    break
                elif message.text == '2':
                    change_score(message.chat.id)
                    bot.send_message(message.chat.id, 'Отлично! Четвертый вопрос')
                    change_state(5, message.chat.id)
                    question_four(message.chat.id)
                    break
                else:
                    bot.send_message(message.chat.id, "Необходимо ввести 1 или 2")
            if user['state'] == 5:
                if message.text == '1':
                    bot.send_message(message.chat.id, 'Отлично!')
                    score = (user['score'] + 100) * 2 / 10
                    bot.send_message(message.chat.id, f'Отлично, твои шансы выжить {score}%')
                    send_pic(score, message.chat.id)
                    drop_score(message.chat.id)
                    change_state(0, message.chat.id)
                    break
                elif message.text == '2':

                    change_score(message.chat.id)
                    bot.send_message(message.chat.id, 'Отлично!')
                    score = (user['score'] + 100) * 2 / 10
                    bot.send_message(message.chat.id, f'Отлично, твои шансы выжить {score}%')
                    send_pic(score, message.chat.id)
                    drop_score(message.chat.id)
                    change_state(0, message.chat.id)
                    break
                else:
                    bot.send_message(message.chat.id, "Необходимо ввести 1 или 2")


def question_one(message_chat_id):
    bot.send_message(message_chat_id, "Ты видшь его, что сделаешь?")
    bot.send_photo(message_chat_id, "https://sun9-24.userapi.com/c638020/v638020282/2436f/sfRYJP3Pkgw.jpg")
    bot.send_message(message_chat_id, "<b>Введите цифру</b> \n<b>1</b> - Погладить \n <b>2</b> - Застрелить", parse_mode="html")


def question_two(message_chat_id):
    bot.send_message(message_chat_id, "Ты идешь по лесу и видшь этот дом")
    bot.send_photo(message_chat_id, "https://avatars.mds.yandex.net/get-pdb/1925510/b1c1c1c3-596f-46f9-a3ae-b1f4167e630b/s1200")
    bot.send_message(message_chat_id, "<b>Введите цифру</b> \n <b>1</b> - Обойти стороной, вдруг там прячутся зараженные \n <b>2</b> - Зайти и обыскать дом, вдруг там есть припасы", parse_mode="html")


def question_three(message_chat_id):
    bot.send_message(message_chat_id, "Ты встретил девушку, она говорит, что не заражена, но у нее проявляются симптомы коронавируса. Твои действия?")
    bot.send_message(message_chat_id, "<b>Введите цифру</b> \n <b>1</b> - Поверить ей, ведь у нее нет причин тебе врать \n <b>2</b> - Застрелить!", parse_mode="html")


def question_four(message_chat_id):
    bot.send_message(message_chat_id, "Ты идешь по дороге, видишь, что в далеке за кем то бегут зараженные, он кричит о помощи. Поможешь ему?")
    bot.send_message(message_chat_id, "<b>Введите цифру</b> \n <b>1</b> - Да, вместе веселее \n <b>2</b> - Нет!", parse_mode="html")


def send_pic(score, id):
    if score == 20:
        bot.send_message(id, "ты - труп и откинешься первым")
        bot.send_photo(id, "https://i.imgur.com/unuUPBE.jpg")
    if score == 40:
        bot.send_message(id, "ты - сок добрый, Ты слишком добрый,ты не выживешь.")
        bot.send_photo(id, "https://tashkentcena.com/files/products/c32767b8a8a2bc5c2860a8e39dfd9a74.jpeg")
    if score == 60:
        bot.send_message(id, "ты - обычный мужик, у тебя есть шанс выжить, но только если повезет")
        bot.send_photo(id, "https://avatars.mds.yandex.net/get-pdb/2321032/a3ac43f1-c551-49e3-b2e9-d91bea15d080/s1200")
    if score == 80:
        bot.send_message(id, "ты - Гелаевский спецназовец, ты хорошо подготвлен и у тебя есть все шансы выжить")
        bot.send_photo(id, "https://galeri.uludagsozluk.com/35/hamzat-gelayev_136389.jpg")
    if score == 100:
        bot.send_message(id, "ты - гуля,бессердечная мразь, тебе вообще пох, ведь твоя жизнь никак не изменилась с наступлением апокалипсиса")
        bot.send_photo(id, "https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/9ee19f45523437.583401ef4e727.jpg")


if __name__ == '__main__':
    bot.polling(none_stop=True)