import logging
from typing import Optional

class LoggerFactory:
    @staticmethod
    def create_logger(name: str, log_file: str, level: Optional[int] = logging.INFO) -> logging.Logger:
        """
        Создает логгер, который записывает сообщения в указанный файл.

        :param name: Имя логгера.
        :param log_file: Путь к файлу, в который будут записываться логи.
        :param level: Уровень логирования (по умолчанию logging.INFO).
        :return: Настроенный экземпляр логгера.
        """
        # Создаем новый логгер
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Создаем обработчик, который будет записывать сообщения в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)

        # Создаем формат сообщений
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Добавляем обработчик к логгеру, если он еще не добавлен
        if not logger.hasHandlers():
            logger.addHandler(file_handler)

        return logger
    
if __name__ == "__main__":
    # Создаем логгер, который будет писать в файл 'app.log'
    logger = LoggerFactory.create_logger("demo_logger", "logs/demo.log")

    # Используем логгер для записи сообщений разного уровня
    logger.info("Это информационное сообщение")
    logger.warning("Это предупреждающее сообщение")
    logger.error("Это сообщение об ошибке")
