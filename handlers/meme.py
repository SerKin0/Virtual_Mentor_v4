from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.filters import StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database.methods.db.sqlite_methods import Database
from database.methods.json.json_methods import language_message
from keyboards import create_reply_keyboard


router = Router()


class FSMMemes(StatesGroup):
    photo_or_video = State()
    text = State()
    name = ""


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_meme_menu", chat)[0]))
async def UploadMeme(message: Message, state: FSMContext):
    await message.answer(language_message("load_photo_or_video_meme", message),
                         reply_markup=create_reply_keyboard(["Skip", "/Cancel"], 1))
    await state.set_state(FSMMemes.photo_or_video)


@router.message(FSMMemes.photo_or_video, F.content_type == ContentType.PHOTO)
@router.message(FSMMemes.photo_or_video, F.content_type == ContentType.TEXT)
async def loadPhotoOrVideoMeme(message: Message, state: FSMContext):
    if message.content_type == "photo":
        await state.update_data(photo_or_video=message.photo[0].file_id)
    elif message.content_type == "video":
        await state.update_data(photo_or_video=message.video.thumb.file_id)
    else:
        print("Да, все норм!")
        await state.update_data(photo_or_video=None)
    await message.answer(language_message("write_description_meme", message))
    await state.set_state(FSMMemes.text)


@router.message(FSMMemes.text, F.content_type == ContentType.TEXT)
async def loadDescriptionMeme(message: Message, state: FSMContext):
    db = Database()
    await state.update_data(text=message.text if message.text != "Skip" else None)
    info_user = db.get_info_user_database(message)
    if info_user:
        await state.update_data(name=f"t.me/{info_user[2]} {info_user[0]} {info_user[1]}")
    else:
        await state.update_data(name=f"t.me/{message.from_user.username} {message.from_user.full_name}")
    data = await state.get_data()
    flag = False if (data["text"] in (None, "")) and (data["photo_or_video"] in (None, "")) else True
    if not flag:
        await message.answer(language_message("download_error", message),
                             reply_markup=create_reply_keyboard(language_message("buttons_meme_menu")))
    else:
        await message.answer(language_message("finish_load_meme", message),
                             reply_markup=create_reply_keyboard(language_message("buttons_meme_menu")))
        await db.add_meme_database(data["photo_or_video"], data["text"], data["name"])
    await state.clear()


@router.message(F.chat.func(lambda chat: chat.text == language_message("buttons_meme_menu", chat)[1]))
async def send_random_meme(message: Message):
    db = Database()
    temp = await db.get_meme_database()
    print(temp)
    if temp[0] == "photo":
        print(temp[1])
        await message.bot.send_photo(message.from_user.id, temp[1], caption=temp[2])
    elif temp[0] == "text":
        await message.bot.send_message(message.from_user.id, temp[2])


@router.message(Command("Cancel"))
async def close(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.answer("Ну окей", reply_markup=create_reply_keyboard(language_message("buttons_meme_menu", message)))
    await state.clear()
