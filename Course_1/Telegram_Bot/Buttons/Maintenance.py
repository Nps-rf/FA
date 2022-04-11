import asyncio
from datetime import timedelta, datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.exceptions import MessageToDeleteNotFound

from Course_1.Telegram_Bot.Buttons.Buttons import *
from Course_1.Telegram_Bot.Utils.Maintenance import bot, HDB, get_user_group, days_of_week, days, SelfState, \
	get_group_schedule, green_list
from Course_1.Telegram_Bot.Utils.date import week_definition
from Course_1.Telegram_Bot.Utils.debug import Debugger
from Course_1.Telegram_Bot.bot import process_start_command


debugger = Debugger()


async def callback_down(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] += 1
			date_count = data['date_count']
			button_state = data["state"]
			await bot.edit_message_text(
				chat_id=call.message.chat.id,
				message_id=call.message.message_id,
				text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
				parse_mode="markdown",
				reply_markup=Inline_Date_ADD if button_state else Inline_Date)

	except KeyError:
		pass


async def callback_up(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			data['date_count'] -= 1
			date_count = data['date_count']
			button_state = data["state"]
		await bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.message_id,
			text=f"*{'Выбираем день недели' if not button_state else 'На какой день задание?'}\n📅 {week_definition(date_count)[0]} - {week_definition(date_count)[1]} 📅*",
			parse_mode="markdown",
			reply_markup=Inline_Date_ADD if button_state else Inline_Date)
	except KeyError:
		pass


async def all_week_homework(call: types.CallbackQuery, state: FSMContext):
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		for day in range(6):
			current_day = (start_date + timedelta(days=day)).strftime('%d.%m.%Y')
			available_homework = HDB.is_available_homework_by_date(
				date=current_day,
				group=get_user_group(call.message),
				data=True)
			__text = ''

			for num, subject in enumerate(available_homework):
				__text += \
					f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
			if not __text:
				__text = '*Никто не заполнил домашнее задания на этот день* 😭'
			else:
				__text = '`' + __text + '`'
			message = f'*📅 {days_of_week[day + 1]} {current_day}*\n{__text}'
			await call.message.answer(
				text=message,
				parse_mode='markdown')
			if HDB.is_file_attached(group=get_user_group(call.message), date=current_day):
				attachments = HDB.get_attachments(group=get_user_group(call.message), date=current_day)
				for pos, document in enumerate(attachments):
					await bot.send_document(
						chat_id=call.message.chat.id,
						document=document[0],
						caption=None,
						parse_mode='markdown')
		try:
			await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
		except MessageToDeleteNotFound:
			debugger.error('Какое-то сообщение не удаляется(')
	except KeyError:
		await process_start_command(call.message)


async def homework_reply(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	try:
		async with state.proxy() as data:
			date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		date_to_db = [
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%y'),
			(start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')]

		if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) or HDB.is_available_homework_by_date(
			date=date_to_db[1],
			group=get_user_group(query.message)):

			date_to_db = date_to_db[0] if HDB.is_available_homework_by_date(
				date=date_to_db[0],
				group=get_user_group(query.message)) else date_to_db[1]

			available_homework = HDB.is_available_homework_by_date(
				date=date_to_db,
				data=True,
				group=get_user_group(query.message))
			__text = str()
			for num, subject in enumerate(available_homework):
				__text += f'{str(num + 1)}) ' + subject[0] + ': ' + subject[1] + '\n'
			text = f'*📅 {days_of_week[days[day] + 1]} {date_to_db}*\n`{__text}`'
			await query.message.answer(
				text=text,
				parse_mode='markdown'
			)
			if HDB.is_file_attached(date=date_to_db, group=get_user_group(query.message)):
				attachments = HDB.get_attachments(group=get_user_group(query.message), date=date_to_db)
				for pos, document in enumerate(attachments):
					await bot.send_document(
						chat_id=query.message.chat.id,
						document=document[0],
						caption=None,
						parse_mode='markdown')
			try:
				await bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
			except MessageToDeleteNotFound:
				debugger.error('Какое-то сообщение не удаляется(')
		else:
			await query.message.answer(
				text='*Никто не заполнил домашнее задания на этот день* 😭', parse_mode='markdown'
			)

	except KeyError:
		await process_start_command(query.message)


async def edit_homework_date(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]

		start_date, end_date = week_definition(date_count, debug=True), week_definition(date_count)[1]
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
			date = data["date"]
		start_date = start_date.strftime('%d.%m.%Y')
		homework = HDB.is_available_homework_by_date(date=date, group=get_user_group(query.message), data=True)
		homework = list(map(lambda x: x[0], homework))
		await bot.edit_message_text(
			text='*Выберите предмет*' if homework else '*Тут ничего нет :(\nДавай выберем другой день лучше?*',
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			parse_mode='markdown',
			reply_markup=create_subjects_keyboard(homework) if homework else None
		)
		await asyncio.sleep(0.5)
		if not homework:
			await bot.send_message(
				chat_id=query.message.chat.id,
				text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
				reply_markup=Inline_Date_ADD,
				parse_mode="markdown"
			)


async def add_homework_date(query: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		current_state = data['state']
		date_count = data['date_count']
	if current_state:
		day = query.data.split("_")[2]
		start_date = week_definition(date_count, debug=True)
		await bot.edit_message_text(
			text='*Введите домашнее задание*',
			chat_id=query.message.chat.id,
			message_id=query.message.message_id,
			parse_mode='markdown'
		)
		async with state.proxy() as data:
			data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		await SelfState.Add_state.set()


async def edit_homework(message: types.Message, state: FSMContext):
	text = message.text
	async with state.proxy() as data:
		date = data['date']
		subject = data['subject']
	debugger.info(message.from_user.username, 'отредактировал', text)
	HDB.delete_homework(subject_name=subject, date=date, group=get_user_group(message))
	text = HDB.add_homework(
		subject_name=subject,
		username=message.from_user.username,
		text=text, date=date,
		group=get_user_group(message),
		edit=True)
	await message.answer(
		text=f'*{text}*', parse_mode='markdown')
	await state.finish()


async def edit_init(call: types.CallbackQuery, state: FSMContext):
	async with state.proxy() as data:
		data['state'] = True
		date_count = data['date_count']
	start_date, end_date = week_definition(date_count)
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
		reply_markup=Inline_Date_ADD,
		parse_mode="markdown"
	)
	await SelfState.Edit_state.set()


async def add_homework_state(call: types.CallbackQuery):
	start_date = datetime.now()
	await SelfState.Add_state.set()
	await bot.edit_message_text(
		chat_id=call.message.chat.id,
		message_id=call.message.message_id,
		text=f"*Выберите предмет*",
		parse_mode="markdown",
		reply_markup=create_subjects_keyboard(get_group_schedule(get_user_group(call.message), start=start_date))
	)


async def add_homework(message: types.Message, state: FSMContext):  # Проблематично перенести
	try:
		async with state.proxy() as data:
			date = data['date']
			subject = data['subject']
			data['state'] = False
	except KeyError:
		await message.answer(text='Ну ладно 🥺', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	if HDB.is_exists(subject_name=subject, date=date, group=get_user_group(message)):
		await message.reply(text='*Мы уже записывали задание на этот день и на этот предмет :)*', parse_mode='markdown')
		await state.finish()
		return Ellipsis

	text = message.text
	debugger.info(message.from_user.username, 'добавил', text if text is not None else message.caption)
	user_group = get_user_group(message)
	exercise = text
	if message.document is not None and message.document.file_id is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.document.file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	elif message.photo and message.photo[0] is not None:
		await SelfState.Parse_state.set()
		HDB.attach_file(date=date, filename=message.photo[0].file_id, group=user_group)
		exercise = message.caption if message.caption is not None else exercise
	else:
		await state.finish()
	if exercise is not None:
		await message.answer(
			text='*{}*'.format(
				HDB.add_homework(
					subject_name=subject,
					date=date,
					text=exercise,
					username=message.from_user.username,
					group=user_group)), parse_mode='markdown')
	try:
		await bot.delete_message(message.chat.id, message_id=message.message_id - 1)
	except MessageToDeleteNotFound:
		debugger.error('Какое-то сообщение не удаляется(')


async def parse_attachments(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		date = data['date']
	HDB.attach_file(date=date, filename=message.document.file_id, group=get_user_group(message))


async def process_add_command(message: types.Message, state: FSMContext):
	await state.finish()
	async with state.proxy() as data:
		data['date_count'] = 0
	debugger.info(message.from_user.username, 'управляет заданиями')
	if message.from_user.username in green_list():
		await message.answer(
			text='*Что будем делать?*',
			parse_mode='markdown',
			reply_markup=Inline_Manage
		)

	else:
		await message.answer(
			text='*Вы не можете управлять заданиями, для получения возможности → @Nps_rf или @monotank*',
			parse_mode='markdown')


async def group_state_command(message: types.Message, state: FSMContext):
	await state.finish()
	await message.answer("Нажми на кнопку, чтобы получить домашнее задание.", reply_markup=answer_start)
	chat_id = message.chat.id
	user_group = message.text.upper()
	HDB.add_user(chat_id=chat_id, user_group=user_group, username=message.from_user.username)


async def delete_homework_date(query: types.CallbackQuery, state: FSMContext):
	day = query.data.split("_")[2]
	async with state.proxy() as data:
		date_count = data['date_count']
		start_date = week_definition(date_count, debug=True)
		data['date'] = (start_date + timedelta(days=days[day])).strftime('%d.%m.%Y')
		date = data["date"]
	start_date, end_date = week_definition(date_count, debug=True), week_definition(date_count)[1]
	start_date = start_date.strftime('%d.%m.%Y')
	homework = HDB.is_available_homework_by_date(date=date, group=get_user_group(query.message), data=True)
	homework = list(map(lambda x: x[0], homework))
	await bot.edit_message_text(
		text='*Выберите предмет*' if homework else '*Тут ничего нет :(\nДавай выберем другой день лучше?*',
		chat_id=query.message.chat.id,
		message_id=query.message.message_id,
		parse_mode='markdown',
		reply_markup=create_subjects_keyboard(homework) if homework else None
	)
	await asyncio.sleep(0.5)
	if not homework:
		await bot.send_message(
			chat_id=query.message.chat.id,
			text=f"*На какой день задание?\n📅 {start_date} - {end_date} 📅*",
			reply_markup=Inline_Date_ADD,
			parse_mode="markdown"
		)