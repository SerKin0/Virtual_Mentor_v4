import logging

logger = logging.getLogger(__name__)


def start_logger():
    # self.logger = logging.getLogger(__name__)

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Установка уровня логирования
    logger.setLevel(logging.INFO)

    # Добавление обработчика для записи логов в файл
    file_handler = logging.FileHandler('app.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.info("Успешное подключение")
