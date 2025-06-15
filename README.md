# config.py 使用说明

本文件用于配置数据库连接参数，供图书管理系统的各模块使用。
拉取完先在此处配置本地数据库。

## 初始化SQL代码

```sql
-- 创建数据库
CREATE DATABASE IF NOT EXISTS library CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE library;

-- 创建图书表
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(100) NOT NULL,
    publisher VARCHAR(100),
    publish_date DATE,
    price DECIMAL(8,2),
    total_copies INT DEFAULT 0,
    available_copies INT DEFAULT 0,
    INDEX idx_title (title),
    INDEX idx_author (author)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin','user') DEFAULT 'user',
    phone VARCHAR(20),
    email VARCHAR(100),
    max_borrow INT DEFAULT 5,
    INDEX idx_username (username)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建借阅记录表
CREATE TABLE IF NOT EXISTS borrowrecords (
    borrow_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    book_id INT NOT NULL,
    borrow_date DATE NOT NULL,
    due_date DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id),
    INDEX idx_user (user_id),
    INDEX idx_book (book_id),
    INDEX idx_due_date (due_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 创建测试图书数据
INSERT INTO books (title, author, publisher, publish_date, price, total_copies, available_copies)
VALUES 
('Python编程从入门到实践', 'Eric Matthes', '人民邮电出版社', '2020-01-01', 89.00, 10, 10),
('深入理解计算机系统', 'Randal E.Bryant', '机械工业出版社', '2019-05-15', 139.00, 5, 5),
('算法导论', 'Thomas H.Cormen', '机械工业出版社', '2018-11-20', 128.00, 8, 8),
('代码整洁之道', 'Robert C. Martin', '人民邮电出版社', '2020-03-01', 69.00, 7, 7),
('重构：改善既有代码的设计', 'Martin Fowler', '人民邮电出版社', '2019-07-01', 99.00, 6, 6),
('计算机程序的构造和解释', 'Harold Abelson', '机械工业出版社', '2019-04-01', 79.00, 4, 4),
('C++ Primer Plus', 'Stephen Prata', '人民邮电出版社', '2020-02-15', 119.00, 5, 5),
('Java核心技术 卷I', 'Cay S. Horstmann', '机械工业出版社', '2019-08-01', 149.00, 8, 8),
('Effective Java', 'Joshua Bloch', '机械工业出版社', '2019-09-01', 89.00, 5, 5),
('Head First设计模式', 'Eric Freeman', '中国电力出版社', '2020-05-01', 98.00, 6, 6),
('数据库系统概念', 'Abraham Silberschatz', '机械工业出版社', '2019-06-01', 129.00, 4, 4),
('MySQL必知必会', 'Ben Forta', '人民邮电出版社', '2020-04-01', 49.00, 10, 10),
('高性能MySQL', 'Baron Schwartz', '电子工业出版社', '2019-10-01', 139.00, 3, 3),
('计算机网络：自顶向下方法', 'James F. Kurose', '机械工业出版社', '2019-11-01', 89.00, 5, 5),
('操作系统概念', 'Abraham Silberschatz', '高等教育出版社', '2020-01-15', 109.00, 4, 4),
('现代操作系统', 'Andrew S. Tanenbaum', '机械工业出版社', '2019-12-01', 119.00, 3, 3),
('编译原理', 'Alfred V. Aho', '机械工业出版社', '2019-07-15', 99.00, 2, 2),
('人工智能：现代方法', 'Stuart Russell', '人民邮电出版社', '2020-03-15', 159.00, 5, 5),
('机器学习', '周志华', '清华大学出版社', '2019-05-01', 88.00, 7, 7),
('数学之美', '吴军', '人民邮电出版社', '2020-02-01', 69.00, 9, 9),
('黑客与画家', 'Paul Graham', '人民邮电出版社', '2019-09-15', 59.00, 6, 6);