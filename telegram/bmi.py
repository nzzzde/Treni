from models.bmi import BMIModel


async def procces_bmi_command(message):
    try:
        args = message.text.split()[1:]
        if len(args) != 2:
            await message.reply("Введіть вагу(кг) і ріст(см). Наприклад /bmi 70 172")
            return

        weight = float(args[0])
        height = float(args[1])

        bmi_model = BMIModel(weight, height)
        bmi_value = bmi_model.calculate_bmi()

        # add saving into db

        await message.reply(f"Ваш ІМТ:{bmi_value}")

    except ValueError as e:
        await message.reply(str(e))
