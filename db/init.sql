use tecnoandina;


CREATE TABLE IF NOT EXISTS alerts (
    `id_alerta` INT
    `datetime` VARCHAR(50) CHARACTER SET utf8,
    `value` NUMERIC(6, 4),
    `version` INT
    `type` VARCHAR(10) CHARACTER SET utf8,
    `sended` BOOLEAN,
    `created_at` VARCHAR(50) CHARACTER SET utf8,
    `updated_at` VARCHAR(50) CHARACTER SET utf8
);