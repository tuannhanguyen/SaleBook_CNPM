create database saledb_cnpm;

INSERT INTO `saledb_cnpm`.`category` (`id`, `name`) VALUES ('1', 'Văn học');
INSERT INTO `saledb_cnpm`.`category` (`id`, `name`) VALUES ('2', 'Kinh tế');
INSERT INTO `saledb_cnpm`.`category` (`id`, `name`) VALUES ('3', 'Khoa học');


INSERT INTO `saledb_cnpm`.`book` (`id`, `name`, `image`, `price`, `category_id`) VALUES ('1', 'Bố già', 'images/bo-gia.jpg', '16', '1');
INSERT INTO `saledb_cnpm`.`book` (`id`, `name`, `image`, `price`, `category_id`) VALUES ('2', 'Ông trùm cuối  cùng', 'images/ong-trum-cuoi-cung.jpg', '15', '1');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Luật bố già', 'images/luat-bo-gia.jpg', '14', '1');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Cách nền kinh tế vận hành', 'images/cach-nen-kinh-te-van-hanh.jpg', '19', '2');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Kinh tế tăng truongr và sụp đổ như thế nào', 'images/nen-kinh-te-tang-truong-va-sup-do-nhu-the-nao.jpg', '20', '2');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Bong bóng kinh tế', 'images/bong-bong-kinh-te.jpg', '21', '2');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Kinh tế học hài hước', 'images/kinh-te-hoc-hai-huoc.jpg', '20', '2');
INSERT INTO `saledb_cnpm`.`book` (`name`, `image`, `price`, `category_id`) VALUES ('Hai số phận', 'images/hai-so-phan.jpg', '13', '1');

UPDATE `saledb_cnpm`.`book` SET `description` = 'The Godfather - Bố Gìa (Cuốn Sách Bất Hủ Nhất Mọi Thời Đại )' WHERE (`id` = '1');
UPDATE `saledb_cnpm`.`book` SET `description` = 'Câu chuyện xen kẽ giữa ngành công nghiệp điện ảnh và các sòng bạc ở dải Las Vegas, cho thấy mafia liên kết với nhau như thế nào' WHERE (`id` = '2');
UPDATE `saledb_cnpm`.`book` SET `description` = 'Bài học kinh doanh từ những ông trùm Mafia' WHERE (`id` = '3');
UPDATE `saledb_cnpm`.`book` SET `description` = 'Cách Nền Kinh Tế Vận Hành - How The Economy Works' WHERE (`id` = '4');
UPDATE `saledb_cnpm`.`book` SET `name` = 'Kinh tế tăng trưởng và sụp đổ như thế nào', `description` = 'Những Công Ty Lớn Đã Thành Công Như Thế Nào? Bạn Cũng Có Thể Làm Được!' WHERE (`id` = '5');
UPDATE `saledb_cnpm`.`book` SET `name` = 'Elon Musk: Tesla & Spacex ', `image` = 'elon-musk.jpg', `description` = 'Elon Musk: Tesla, Spacex Và Sứ Mệnh Tìm Kiếm Một Tương Lai Ngoài Sức Tưởng Tượng ' WHERE (`id` = '6');
UPDATE `saledb_cnpm`.`book` SET `description` = 'Kinh Tế Học Hài Hước (Tái Bản 2018)' WHERE (`id` = '7');
UPDATE `saledb_cnpm`.`book` SET `description` = 'Hai số phận là một cuốn tiểu thuyết được sáng tác vào năm 1979 bởi nhà văn người Anh Jeffrey Archer' WHERE (`id` = '8');


INSERT INTO `saledb_cnpm`.`user` (`id`, `name`, `username`, `password`, `active`, `user_role`) VALUES ('1', 'tuan nhan', 'admin', 'admin', '1', 'ADMIN');
INSERT INTO `saledb_cnpm`.`user` (`id`, `name`, `username`, `password`, `active`, `user_role`) VALUES ('2', 'nhan', 'user', 'admin', '1', 'USER');

INSERT INTO `saledb_cnpm`.`user` (`id`, `name`, `active`, `username`, `password`) VALUES ('1', 'tuan nhan', '1', 'admin', 'admin');
INSERT INTO `saledb_cnpm`.`user` (`id`, `name`, `active`, `username`, `password`) VALUES ('2', 'nhan', '1', 'user', 'admin');