use tecnoandina;

CREATE TABLE IF NOT EXISTS alerts (
    `datetime` VARCHAR(50) CHARACTER SET utf8,
    `value` VARCHAR(10) CHARACTER SET utf8,
    `version` VARCHAR(10) CHARACTER SET utf8,
    `type` VARCHAR(10) CHARACTER SET utf8,
    `sended` VARCHAR(10 ) CHARACTER SET utf8,
    `created_at` VARCHAR(50) CHARACTER SET utf8,
    `updated_at` VARCHAR(50) CHARACTER SET utf8
);