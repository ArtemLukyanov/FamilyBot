import telebot
from telebot import types
import datetime

API_TOKEN = '7444859157:AAFo2yC6vxHZ1PG5HYd3JYnlJMALFRcvsXw'
bot = telebot.TeleBot(API_TOKEN)

# Храним состояния и данные пользователей
user_states = {}
user_data = {}

# Информация по услугам — заполните описания в этой структуре
service_info = {
    "dentistry": {
        "Терапевтическая стоматология": "Терапевтическая стоматология: \n\nДиагностика, лечение и профилактика заболеваний зубов и дёсен. Основное внимание уделяется лечению кариеса, лечению пульпита, лечению периодонтита и других воспалительных процессов. Проводятся процедуры по чистке зубов, реставрации зубов, пломбированию зубов.",
        "Хирургическая стоматология": "Хирургическая стоматология: \n\nОперативное и плановое вмешательство для лечения заболеваний и патологий зубочелюстной системы. Включает в себя удаление зубов, имплантацию, коррекцию врожденных и приобретенных дефектов, лечение травм и инфекций. Основная цель хирургической стоматологии - восстановление функциональности и эстетики ротовой полости, а также улучшение качества жизни пациента.",
        "Имплантация зубов": "Имплантация зубов:  \n\nСовременный метод восстановления утраченных зубов, который включает в себя установку искусственного корня (импланта) в челюстную кость. Имплант служит основой для последующего крепления коронки, мостовидного протеза или съёмного протеза. Этот метод позволяет восстановить функциональность и эстетику зубного ряда, обеспечивая долговечность и надежность результата. Имплантация зубов помогает улучшить качество жизни пациента, возвращая комфорт при жевании и уверенность в улыбке.",
        "Ортопедическая стоматология": "Ортопедическая стоматология:\n\nОсновная цель ортопедической стоматологии в Ялте - восстановление жевательной функции, улучшение эстетики улыбки и повышение качества жизни пациента. Включает в себя изготовление и установку коронок, виниров, мостовидных протезов, а также съёмных и несъёмных зубных протезов.",
        "Ортодонтическая стоматология": "Ортодонтическая стоматология:\n\nГлавной задачей ортодонтии является исправление неправильного прикуса и выравнивание зубов для улучшения функции жевания, речи и эстетики улыбки. Лечение может включать использование брекетов, элайнеров, капп и других ортодонтических аппаратов, которые помогают перемещать зубы в правильное положение.",
        "Детская стоматология": "Детская стоматология:\n\nУход за зубами детей от младенчества до подросткового возраста. Основной акцент детской стоматологии приходится на профилактику и лечение заболеваний полости рта у детей, а также обучение правильной гигиене полости рта. Врачи-стоматологи, работающие в этой области, имеют специальные навыки для работы с детьми и создания комфортной атмосферы во время визитов. Лечение может включать профилактические осмотры, пломбирование кариеса, герметизацию фиссур и ортодонтические консультации.",
        "Рентген зубов": "Рентген зубов:\n\nСнимки зубов на немецком томографе Sirona Orthophos XG 3D",
    },
    "cosmetology": {
        "Удаление новообразований": "",
        "Лазерная эпиляция": "",
        "Лазерное омоложение и отбеливание": "",
        "Космецевтические уходы": "",
        "Дерматологические пилинги": "",
        "Безоперационный лифтинг нитями": "",
        "Ботулинотерапия": "",
        "Мезотерапия": "",
        "Контурная пластика": "",
        "Биоревитализация": "",
    }
}

# Кнопка "Главное меню"
main_menu_button = types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")

# Функция для отправки главного меню
def send_main_menu(chat_id):
    user_states[chat_id] = None
    user_data[chat_id] = {}
    markup = types.InlineKeyboardMarkup()
    # При нажатии на эту кнопку будет открыт внешний сайт
    markup.add(types.InlineKeyboardButton(
        "📆  Онлайн запись на консультацию",
        url="https://testancet.tiiny.site/"
    ))
    markup.add(types.InlineKeyboardButton("🔥  Акции", callback_data="promo"))
    markup.add(types.InlineKeyboardButton("📲  Соцсети", callback_data="socials"))
    markup.add(types.InlineKeyboardButton("📋  Список услуг", callback_data="services"))
    markup.add(types.InlineKeyboardButton("☎️  Контакты", callback_data="contacts"))
    bot.send_message(
        chat_id,
        "❤️ Добро пожаловать в Family Clinic ! Мы — команда профессионалов с многолетним опытом...\n\nЧто вас интересует?",
        reply_markup=markup
    )

# === Хендлер /start ===
@bot.message_handler(commands=['start'])
def handle_start(message):
    send_main_menu(message.chat.id)

# === Обработка callbackQuery ===
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    chat_id = call.message.chat.id
    data = call.data

    # Главное меню
    if data == "main_menu":
        send_main_menu(chat_id)
        return

    # Акции
    if data == "promo":
        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Действующие акции: ...", reply_markup=markup)

    # Социальные сети
    elif data == "socials":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Telegram", url="https://t.me/family_clinic_pro"))
        markup.add(types.InlineKeyboardButton("ВКонтакте", url="https://vk.com/cosmetyalta?from=search"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Мы будем рады видеть Вас в социальных сетях!", reply_markup=markup)

    # Контакты
    elif data == "contacts":
        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        bot.send_message(
            chat_id,
            "Клиника работает ежедневно с 09:00 до 19:00\n"
            "Адрес: г. Ялта, ул. Боткинская, 13А\n"
            "Телефон: 📞 +7 (978) 756-50-20",
            reply_markup=markup
        )

    # Список услуг: выбор раздела
    elif data == "services":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🦷 Стоматология", callback_data="services|dentistry"))
        markup.add(types.InlineKeyboardButton("✨ Косметология и дерматология", callback_data="services|cosmetology"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите раздел услуг:", reply_markup=markup)

    # Список услуг: выбор конкретного направления
    elif data.startswith("services|"):
        _, section = data.split("|", 1)
        items = list(service_info.get(section, {}).keys())
        if not items:
            markup = types.InlineKeyboardMarkup()
            markup.add(main_menu_button)
            bot.send_message(chat_id, "Информация по этому разделу пока отсутствует.", reply_markup=markup)
            return

        markup = types.InlineKeyboardMarkup(row_width=1)
        for idx, name in enumerate(items):
            markup.add(types.InlineKeyboardButton(name, callback_data=f"service|{section}|{idx}"))
        markup.add(main_menu_button)
        bot.send_message(chat_id, "Выберите услугу:", reply_markup=markup)

    # Список услуг: показ информации по выбранной услуге
    elif data.startswith("service|"):
        _, section, idx_str = data.split("|", 2)
        try:
            idx = int(idx_str)
            items = list(service_info.get(section, {}).items())
            name, info = items[idx]
        except (ValueError, IndexError):
            markup = types.InlineKeyboardMarkup()
            markup.add(main_menu_button)
            bot.send_message(chat_id, "Ошибка выбора услуги. Попробуйте ещё раз.", reply_markup=markup)
            return

        markup = types.InlineKeyboardMarkup()
        markup.add(main_menu_button)
        if info:
            bot.send_message(chat_id, info, reply_markup=markup)
        else:
            bot.send_message(chat_id, f"Описание услуги «{name}» пока не добавлено. Скоро будет доступно.", reply_markup=markup)

    else:
        # На случай непредвиденных callback`ов возвращаем в главное меню
        send_main_menu(chat_id)

if __name__ == '__main__':
    bot.infinity_polling()
