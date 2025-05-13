-- Створення таблиці для panic logs
CREATE TABLE iphone_panic_dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    panic_code TEXT NOT NULL,
    hardware_component TEXT,
    description TEXT
);

-- Створення таблиці для hex-кодів датчиків iPhone 13/14
CREATE TABLE sensor_error_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model TEXT NOT NULL,
    hex_code TEXT NOT NULL,
    component TEXT,
    description TEXT
);

-- Дані для iphone_panic_dictionary
INSERT INTO iphone_panic_dictionary (panic_code, hardware_component, description) VALUES
('AOP PANIC - PressureController', 'Барометр', 'Эта ошибка возникает в основном на iPhone X и выше, находится барометр на системном шлейфе снизу возле левого микрофона.'),
('ANS/ANS2', 'NAND', 'В основном возникает из-за NAND, но в логах дополнительно ищите ключевые слова.'),
('SD: 0 Missing sensor(s): TG0B', 'АКБ/TIGRIS', 'Девайс не видит АКБ.'),
('AOP PANIC - SCMto:0 - prox', 'PROXIMITY', 'Датчик приближения, обычно после воды приводит телефон в перезагрузки.'),
('Kernel data abort', 'CPU', 'В основном из-за отвала процессора либо катушек по линиям buck. Так же в логе иногда встречаются конкретные линии и элементы со схем.'),
('Missing sensor(s): mic1', 'Microphone', 'Часто бывает после воды или механического воздействия. mic1 - нижний левый микрофон, mic2 - рядом со вспышкой/фонариком, mic3 - рядом с фронтальной камерой, mic4 - правый нижний микрофон.'),
('AppleSocHot: hot hot hot', 'CPU/КП', 'Встречал только на моделях iPhone 7. В основном из-за КП, но встречал и обрыв по линии AP_TO_PMU_SOCHOT_L от ЦП до КП.'),
('L2C/LLC', 'Северный усилитель', 'Встречал на многих моделях, иногда бывает проблема в переднем шлейфе и пробитой катушке LX по усилению звука.'),
('NO pulse on', 'Taptic Engine', 'Часто разъем в коррозии.'),
('nvme', 'NAND', 'Nand с PCIE шиной.'),
('Kernel instructglon fetch abort', 'CPU', 'Прекращение работы ядра ЦП.'),
('GFX GPU', 'CPU', 'Прекращение работы ЦП, встречал только на моделях iPhone 8, часто бывает из-за слоев в плате.'),
('Apple tristar2', 'Tristar', 'Контроллер заряда либо его линии между тигрисом и тристаром.'),
('Fatal coherency point error CP_com_NORM', 'CPU/катушки/КП', 'Неоднозначная ошибка.');

-- Дані для sensor_error_codes
INSERT INTO sensor_error_codes (model, hex_code, component, description) VALUES
('iPhone 13', '0x400', 'нижняя плата', 'Только для iPhone 13 Mini'),
('iPhone 13', '0x800', 'сборка порта зарядки', 'Зарядка на нижней плате'),
('iPhone 13', '0x1000', 'передний шлейф', 'Верхний шлейф'),
('iPhone 13', '0x4000', 'батарея', 'Часть батареи'),

-- Дані про коди датчиків iPhone 14
INSERT INTO sensor_error_codes (model, hex_code, component, description) VALUES
('iPhone 14', '0x10000', 'шлейф кнопки питания', 'Проблема с кнопкой питания'),
('iPhone 14', '0x20000', 'многослойная плата', 'Проблема с многослойной платой'),
('iPhone 14', '0x40000', 'шлейф зарядки', 'Неисправность зарядки'),
('iPhone 14', '0x80000', 'крышка/беспроводная зарядка', 'Индукционная зарядка или задняя крышка');
