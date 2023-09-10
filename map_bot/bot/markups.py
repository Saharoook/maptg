from telebot import types

admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

add_point = types.KeyboardButton('add point')
change_point = types.KeyboardButton('change point')
my_points = types.KeyboardButton('my points')
invite_admin = types.KeyboardButton('invite admin')
invite_user = types.KeyboardButton('invite user')
support = types.KeyboardButton('support')

admin_markup.add(add_point, change_point, my_points, invite_admin, invite_user)

user_markup.add(support)

