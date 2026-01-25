INSERT INTO library_author (first_name, last_name, date_of_birth, date_of_death) VALUES
('Jane', 'Austen', '1775-12-16', '1817-07-18'),
('George', 'Orwell', '1903-06-25', '1950-01-21'),
('Agatha', 'Christie', '1890-09-15', '1976-01-12'),
('Haruki', 'Murakami', '1949-01-12', NULL), 
('Virginia', 'Woolf', '1882-01-25', '1941-03-28'),
('Ernest', 'Hemingway', '1899-07-21', '1961-07-02'),
('Mark', 'Twain', '1835-11-30', '1910-09-11'),
('Leo', 'Tolstoy', '1828-09-09', '1910-11-20'),
('Fyodor', 'Dostoevsky', '1821-11-11', '1881-11-02'),
('Gabriel', 'García Márquez', '1927-03-06', '2014-04-17'),
('William', 'Shakespeare', '1564-04-26', '1616-04-23'),
('Franz', 'Kafka', '1883-07-03', '1924-06-03'),
('Emily', 'Brontë', '1818-07-30', '1848-12-19'),
('박', '경리', '1926-10-25', '2008-05-25'),
('황', '석영', '1943-01-04', NULL),
('신', '경숙', '1963-01-12', NULL),
('윤', '동주', '1917-12-30', '1945-02-16'),
('이', '상', '1910-09-20', '1937-04-17'),
('한', '강', '1970-11-27', NULL),
('김', '영하', '1968-01-01', NULL),
('공', '지영', '1963-01-31', NULL),
('오', '정희', '1947-11-09', NULL),
('박', '완서', '1931-10-10', '2011-01-22'),
('염', '상섭', '1897-08-18', '1963-03-14'),
('채', '만식', '1902-07-25', '1950-06-11'),
('Robert', 'C. Martin', '1952-12-05', NULL);

-- 위에 있는 작가의 책(isbn, title, author, summary) 생성을 위한 sql 
INSERT INTO library_book (isbn, title, author_id, summary) VALUES
-- Robert C. Martin
('978-0132350884', 'Clean Code: A Handbook of Agile Software Craftsmanship', 26, 'Even bad code can function. But if code is not clean, it can bring a development organization to its knees.'),
('978-0134494166', 'Clean Architecture: A Craftsman''s Guide to Software Structure and Design', 26, 'A guide to software architecture that helps you create systems that are easy to understand, maintain, and deploy.'),
('978-0137081073', 'The Clean Coder: A Code of Conduct for Professional Programmers', 26, 'This book is packed with practical advice—about everything from estimating and coding to refactoring and testing.'),
-- Jane Austen
('978-0141439518', 'Pride and Prejudice', 1, 'A classic novel about the emotional development of the protagonist, Elizabeth Bennet.'),
('978-0141439662', 'Sense and Sensibility', 1, 'The story of two sisters, Elinor and Marianne Dashwood, who have contrary temperaments.'),
('978-0141439587', 'Emma', 1, 'A novel about youthful hubris and the perils of misconstrued romance.'),
-- George Orwell
('978-0451524935', '1984', 2, 'A dystopian novel set in Airstrip One, a province of the superstate Oceania in a world of perpetual war, omnipresent government surveillance, and public manipulation.'),
('978-0451526342', 'Animal Farm', 2, 'An allegorical novella reflecting events leading up to the Russian Revolution of 1917 and then on into the Stalinist era of the Soviet Union.'),
('978-0141182652', 'Down and Out in Paris and London', 2, 'A memoir in two parts on the theme of poverty in the two cities.'),
-- Agatha Christie
('978-0062073488', 'And Then There Were None', 3, 'Ten strangers are lured to an isolated island and are killed off one by one.'),
('978-0062073495', 'Murder on the Orient Express', 3, 'Detective Hercule Poirot must solve a murder on a snowbound train.'),
('978-0007527526', 'The Murder of Roger Ackroyd', 3, 'A classic Hercule Poirot mystery involving a wealthy man found stabbed in his study.'),
-- Haruki Murakami
('978-0307278932', '1Q84', 4, 'A story of how a young woman named Aomame and a writer named Tengo are drawn into a strange, parallel world.'),
('978-0375704024', 'Norwegian Wood', 4, 'A nostalgic story of loss and burgeoning sexuality.'),
('978-1400079278', 'Kafka on the Shore', 4, 'A metaphysical novel that follows two distinct but interrelated plots.'),
-- Virginia Woolf
('978-0156030410', 'To the Lighthouse', 5, 'A novel that centers on the Ramsay family and their visits to the Isle of Skye in Scotland between 1910 and 1920.'),
('978-0156628709', 'Mrs Dalloway', 5, 'The novel details a day in the life of Clarissa Dalloway, a fictional high-society woman in post-First World War England.'),
('978-0156030410', 'A Room of One''s Own', 5, 'An extended essay, based on a series of lectures, that explores the role of women in literature.'),
-- Ernest Hemingway
('978-0684801223', 'The Old Man and the Sea', 6, 'The story of Santiago, an aging Cuban fisherman who struggles with a giant marlin far out in the Gulf Stream.'),
('978-0684801469', 'For Whom the Bell Tolls', 6, 'It tells the story of Robert Jordan, a young American volunteer attached to a Republican guerrilla unit during the Spanish Civil War.'),
('978-0684801452', 'A Farewell to Arms', 6, 'A first-person account of an American, serving as a lieutenant in the ambulance corps of the Italian Army during World War I.'),
-- Mark Twain
('978-0486280615', 'Adventures of Huckleberry Finn', 7, 'A novel about a young boy, Huckleberry "Huck" Finn, and his adventures as he travels down the Mississippi River with a runaway slave, Jim.'),
('978-0486400778', 'The Adventures of Tom Sawyer', 7, 'A novel about a young boy growing up along the Mississippi River.'),
('978-0553212459', 'The Prince and the Pauper', 7, 'A novel for young people which tells the story of two young boys who are identical in appearance.'),
-- Leo Tolstoy
('978-0140449244', 'War and Peace', 8, 'A novel that chronicles the history of the French invasion of Russia and the impact of the Napoleonic era on Tsarist society through the stories of five Russian aristocratic families.'),
('978-0143035008', 'Anna Karenina', 8, 'A novel of a married aristocrat and her affair with the affluent Count Vronsky.'),
('978-0872203988', 'The Death of Ivan Ilyich', 8, 'A novella about a high-court judge in 19th-century Russia and his sufferings and death.'),
-- Fyodor Dostoevsky
('978-0486415871', 'Crime and Punishment', 9, 'A novel about the mental anguish and moral dilemmas of Rodion Raskolnikov, an impoverished ex-student in Saint Petersburg who formulates a plan to kill an unscrupulous pawnbroker for her money.'),
('978-0374528379', 'The Brothers Karamazov', 9, 'A passionate philosophical novel set in 19th-century Russia, that enters deeply into the ethical debates of God, free will, and morality.'),
('978-0486270524', 'Notes from Underground', 9, 'An 1864 novella that is considered by many to be one of the first existentialist novels.'),
-- Gabriel García Márquez
('978-0060883287', 'One Hundred Years of Solitude', 10, 'The multi-generational story of the Buendía family, whose patriarch, José Arcadio Buendía, founds the town of Macondo.'),
('978-1400034680', 'Love in the Time of Cholera', 10, 'The story of two lovers, Florentino Ariza and Fermina Daza, whose love endures for over fifty years.'),
('978-0141032466', 'Chronicle of a Death Foretold', 10, 'A novella that tells, in the form of a pseudo-journalistic reconstruction, the story of the murder of Santiago Nasar by the two Vicario brothers.'),
-- William Shakespeare
('978-0743477123', 'Hamlet', 11, 'A tragedy that tells the story of Prince Hamlet of Denmark, who seeks revenge on his uncle Claudius for murdering his father.'),
('978-0743477116', 'Romeo and Juliet', 11, 'An archetypal story of young, star-crossed lovers.'),
('978-0743477109', 'Macbeth', 11, 'A tragedy about a Scottish general who, spurred by a prophecy and his ambitious wife, murders the king to seize the throne.'),
-- Franz Kafka
('978-1503292333', 'The Metamorphosis', 12, 'The story of a traveling salesman, Gregor Samsa, who wakes up one morning to find himself inexplicably transformed into a huge insect.'),
('978-0805210429', 'The Trial', 12, 'Tells the story of Josef K., a man arrested and prosecuted by a remote, inaccessible authority, with the nature of his crime revealed neither to him nor to the reader.'),
('978-0805210573', 'The Castle', 12, 'A novel about a land surveyor named K. who struggles to gain access to the mysterious authorities of a castle who govern the village.'),
-- Emily Brontë
('978-0141439556', 'Wuthering Heights', 13, 'A novel about the passionate and destructive love between Catherine Earnshaw and Heathcliff.'),
-- 박경리 (Park Kyong-ni)
('978-8965450017', '토지 (Toji)', 14, 'A saga that follows the turbulent history of Korea from the late 19th century to the early 20th century through the lives of the Choi family.'),
-- 황석영 (Hwang Sok-yong)
('978-1583228109', 'The Guest', 15, 'A novel that deals with the tragic events of a massacre that occurred in a Korean village during the Korean War.'),
('978-8936433598', '바리데기 (Princess Bari)', 15, 'A modern retelling of a traditional Korean myth, following a North Korean girl named Bari on her journey to London.'),
('978-8936433796', '오래된 정원 (The Old Garden)', 15, 'A story of a political prisoner who is released after seventeen years to find a world that has changed and a love that has endured.'),
-- 신경숙 (Shin Kyung-sook)
('978-0307743717', 'Please Look After Mom', 16, 'A novel about a family''s search for their mother who goes missing in a Seoul subway station.'),
('978-8936433697', '어디선가 나를 찾는 전화벨이 울리고 (I''ll Be Right There)', 16, 'A story of youth, love, and loss set against the backdrop of South Korea''s political turmoil in the 1980s.'),
('978-8954602324', '리진 (Li Jin)', 16, 'A historical novel about a 19th-century Korean court dancer who falls in love with a French diplomat.'),
-- 윤동주 (Yun Dong-ju)
('978-8937460165', '하늘과 바람과 별과 시 (Sky, Wind, and Stars)', 17, 'A collection of poems by one of Korea''s most beloved poets, known for his lyrical and resistance poetry against Japanese colonialism.'),
-- 이상 (Yi Sang)
('978-0979971486', '날개 (The Wings)', 18, 'A short story that explores themes of alienation, consciousness, and the fragmented self in modern society.'),
('978-8983922336', '오감도 (Crow''s Eye View)', 18, 'A series of experimental poems that challenged the conventions of the time and is a cornerstone of Korean modernist literature.'),
-- 한강 (Han Kang)
('978-1107150221', 'The Vegetarian', 19, 'A novel about a woman who decides to stop eating meat and the devastating consequences of this decision on her personal and family life.'),
('978-1108405020', '소년이 온다 (Human Acts)', 19, 'A novel centered on the 1980 Gwangju Uprising in South Korea.'),
('978-8954682654', '희랍어 시간 (Greek Lessons)', 19, 'A story about a woman who has lost her ability to speak and her Greek language instructor who is losing his sight.'),
-- 김영하 (Kim Young-ha)
('978-0156031844', 'I Have the Right to Destroy Myself', 20, 'A novel about a man who "assists" people with suicide and the stories of his clients.'),
('978-8954622032', '살인자의 기억법 (Memoir of a Murderer)', 20, 'The story of a former serial killer with Alzheimer''s who tries to protect his daughter from her boyfriend, whom he suspects is also a killer.'),
('978-8982739348', '빛의 제국 (Your Republic Is Calling You)', 20, 'A novel about a North Korean spy who has been living in South Korea for 20 years and is suddenly recalled to the North.'),
-- 공지영 (Gong Ji-young)
('978-1566568602', 'Our Happy Time', 21, 'A novel about the relationship between a suicidal young woman from a privileged background and a death-row inmate.'),
('978-8984312823', '도가니 (The Crucible)', 21, 'A novel based on a true story of abuse at a school for the hearing-impaired, which led to widespread public outrage and legal reforms.'),
('978-8992449007', '즐거운 나의 집 (My Happy Home)', 21, 'A novel that explores family relationships and personal growth through the eyes of a teenage girl.'),
-- 오정희 (Oh Jung-hee)
('978-0786495207', 'The Bird', 22, 'A collection of short stories that delve into the lives of characters, often women, who are marginalized and struggling with the aftermath of trauma and loss.'),
-- 박완서 (Park Wan-suh)
('978-1597190011', 'Who Ate Up All the Shinga?', 23, 'An autobiographical novel that depicts the author''s childhood and experiences during the Japanese colonial period and the Korean War.'),
('978-8932016279', '그 산이 정말 거기 있었을까 (Was the Mountain Really There?)', 23, 'A sequel to "Who Ate Up All the Shinga?", this novel covers the author''s life during and after the Korean War.'),
('978-8932011953', '그 많던 싱아는 누가 다 먹었을까', 23, 'An autobiographical novel that depicts the author''s childhood and experiences during the Japanese colonial period and the Korean War.'),
-- 염상섭 (Yom Sang-seop)
('978-1572410344', 'Three Generations', 24, 'A novel that portrays the conflicts between three generations of a Korean family, reflecting the social changes of the 1930s.'),
-- 채만식 (Chae Man-sik)
('978-0824831006', 'Peace Under Heaven', 25, 'A satirical novel that critiques the Korean society under Japanese rule through the story of a tyrannical landlord.');

-- 장르 데이터 삽입
INSERT INTO library_genre (name) VALUES
('Novel'), 
('Romance'), 
('Classic'), 
('Politic'), 
('Science'), 
('Essay'), 
('Mystery'), 
('Thriller'), 
('Fantasy'), 
('War'), 
('Non-fiction'), 
('fiction'), 
('Computer Programming'), 
('Software'), 
('Linux'), 
('Memoir'), 
('Detective'), 
('Modernist'), 
('Feminism'),
('Adventure'), 
('Satire'), 
('Children'), 
('Philosophy'), 
('Tragedy'), 
('Play'),
('Saga'), 
('Modern Myth'), 
('Contemporary'), 
('Poetry'), 
('Autobiographic'), 
('Historic');

-- 책과 장르 연결 데이터 삽입 (library_book_genre)
INSERT INTO library_book_genre (book_id, genre_id) VALUES
-- Clean Code
(1, 1), (1, 2),
-- Clean Architecture
(2, 1), (2, 3) ON CONFLICT (book_id, genre_id) DO NOTHING;

INSERT INTO library_book_genre (book_id, genre_id) VALUES
-- The Clean Coder
(3, 1),
-- Pride and Prejudice
(4, 4), (4, 5),
-- Sense and Sensibility
(5, 4), (5, 5),
-- Emma
(6, 4), (6, 5),
-- 1984
(7, 6), (7, 7), (7, 8),
-- Animal Farm
(8, 9), (8, 10),
-- Down and Out in Paris and London
(9, 11),
-- And Then There Were None
(10, 12), (10, 13),
-- Murder on the Orient Express
(11, 12), (11, 14),
-- The Murder of Roger Ackroyd
(12, 12), (12, 14),
-- 1Q84
(13, 15), (13, 16),
-- Norwegian Wood
(14, 17), (14, 4), (14, 18),
-- Kafka on the Shore
(15, 16), (15, 15), (15, 30),
-- To the Lighthouse
(16, 19),
-- Mrs Dalloway
(17, 19), (17, 20),
-- A Room of One's Own
(18, 21), (18, 22), (18, 23),
-- The Old Man and the Sea
(19, 18), (19, 25),
-- For Whom the Bell Tolls
(20, 24), (20, 21),
-- A Farewell to Arms
(21, 24), (21, 4), (21, 18),
-- Adventures of Huckleberry Finn
(22, 26), (22, 27),
-- The Adventures of Tom Sawyer
(23, 26),
-- The Prince and the Pauper
(24, 5), (24, 28),
-- War and Peace
(25, 3), (25, 29),
-- Anna Karenina
(26, 29), (26, 4),
-- The Metamorphosis
(37, 8), (37, 25),
-- The Vegetarian
(51, 23),
-- Human Acts
(52, 5),
-- The Death of Ivan Ilyich
(27, 25), (27, 30),
-- Crime and Punishment
(28, 30), (28, 20),
-- The Brothers Karamazov
(29, 30), (29, 3),
-- Notes from Underground
(30, 30), (30, 2),
-- One Hundred Years of Solitude
(31, 16), (31, 22),
-- Love in the Time of Cholera
(32, 4), (32, 16),
-- Chronicle of a Death Foretold
(33, 12), (33, 25),
-- Hamlet
(34, 11), (34, 12),
-- Romeo and Juliet
(35, 24), (35, 4),
-- Macbeth
(36, 26),
-- The Trial
(38, 4), (38, 30),
-- The Castle
(39, 5), (39, 19),
-- Wuthering Heights
(40, 6), (40, 4),
-- 토지 (Toji)
(41, 7), (41, 8) ON CONFLICT (book_id, genre_id) DO NOTHING;


INSERT INTO library_book_genre (book_id, genre_id) VALUES
-- The Guest
(42, 13),
-- 바리데기 (Princess Bari)
(43, 15), (43, 9),
-- 오래된 정원 (The Old Garden)
(44, 18), (44, 4),
-- Please Look After Mom
(45, 3),
-- 어디선가 나를 찾는 전화벨이 울리고 (I'll Be Right There)
(46, 15), (46, 17),
-- 리진 (Li Jin)
(47, 15), (47, 4),
-- 하늘과 바람과 별과 시 (Sky, Wind, and Stars)
(48, 9),
-- 날개 (The Wings)
(49, 19), (49, 16),
-- 오감도 (Crow's Eye View)
(50, 4), (50, 19),
-- 희랍어 시간 (Greek Lessons)
(53, 31) ON CONFLICT (book_id, genre_id) DO NOTHING;

INSERT INTO library_book_genre (book_id, genre_id) VALUES
-- I Have the Right to Destroy Myself
(54, 24), (54, 30),
-- 살인자의 기억법 (Memoir of a Murderer)
(55, 13), (55, 20),
-- 빛의 제국 (Your Republic Is Calling You)
(56, 13), (56, 26),
-- Our Happy Time
(57, 26),
-- 도가니 (The Crucible)
(58, 20), (58, 21),
-- 즐거운 나의 집 (My Happy Home)
(59, 29),
-- The Bird
(60, 20),
-- Who Ate Up All the Shinga?
(61, 15), (61, 11),
-- 그 산이 정말 거기 있었을까 (Was the Mountain Really There?)
(62, 19), (62, 11),
-- 그 많던 싱아는 누가 다 먹었을까
(63, 10),
-- Three Generations
(64, 16),
-- Peace Under Heaven
(65, 27) ON CONFLICT (book_id, genre_id) DO NOTHING;

-- BookInstance 데이터 삽입
INSERT INTO library_bookinstance (id, book_id, imprint, due_back, status) VALUES
-- Book 1-3 (Robert C. Martin)
('a1b2c3d4-e5f6-7890-1234-567890abcdef', 1, 'Prentice Hall', NULL, 'a'),
('b2c3d4e5-f6a7-8901-2345-67890abcdef1', 1, 'Prentice Hall', '2025-12-20', 'o'),
('c3d4e5f6-a7b8-9012-3456-7890abcdef23', 2, 'Prentice Hall', NULL, 'a'),
('d4e5f6a7-b8c9-0123-4567-890abcdef34a', 3, 'Prentice Hall', NULL, 'm'),
-- Book 4-6 (Jane Austen)
('e5f6a7b8-c9d0-1234-5678-90abcdef4567', 4, 'Penguin Classics', NULL, 'a'),
('f6a7b8c9-d0e1-2345-6789-0abcdef5678b', 4, 'Penguin Classics', '2026-01-10', 'o'),
('a7b8c9d0-e1f2-3456-7890-1bcdef67890a', 5, 'Signet Classics', NULL, 'a'),
('b8c9d0e1-f2a3-4567-8901-cdef67890ab1', 6, 'Penguin Classics', NULL, 'r'),
-- Book 7-9 (George Orwell)
('c9d0e1f2-a3b4-5678-9012-def67890ab1c', 7, 'Signet Classics', NULL, 'a'),
('d0e1f2a3-b4c5-6789-0123-ef67890ab1cd', 7, 'Signet Classics', '2025-11-30', 'o'),
('e1f2a3b4-c5d6-7890-1234-f67890ab1cde', 8, 'Penguin Books', NULL, 'a'),
('f2a3b4c5-d6e7-8901-2345-67890ab1cdef', 9, 'Penguin Books', NULL, 'a'),
-- Book 10-12 (Agatha Christie)
('a3b4c5d6-e7f8-9012-3456-7890ab1cdef0', 10, 'William Morrow', NULL, 'a'),
('b4c5d6e7-f8a9-0123-4567-890ab1cdef01', 11, 'William Morrow', '2026-02-15', 'o'),
('c5d6e7f8-a9b0-1234-5678-90ab1cdef012', 12, 'HarperCollins', NULL, 'a'),
-- Book 13-15 (Haruki Murakami)
('d6e7f8a9-b0c1-2345-6789-0ab1cdef0123', 13, 'Vintage', NULL, 'a'),
('e7f8a9b0-c1d2-3456-7890-ab1cdef01234', 14, 'Vintage', NULL, 'a'),
('f8a9b0c1-d2e3-4567-8901-b1cdef012345', 15, 'Vintage', '2025-12-01', 'o'),
-- Book 16-18 (Virginia Woolf)
('a9b0c1d2-e3f4-5678-9012-1cdef0123456', 16, 'Mariner Books', NULL, 'a'),
('b0c1d2e3-f4a5-6789-0123-cdef01234567', 17, 'Mariner Books', NULL, 'a'),
('c1d2e3f4-a5b6-7890-1234-def012345678', 18, 'Mariner Books', NULL, 'm'),
-- Book 19-21 (Ernest Hemingway)
('d2e3f4a5-b6c7-8901-2345-ef0123456789', 19, 'Scribner', NULL, 'a'),
('e3f4a5b6-c7d8-9012-3456-f01234567890', 20, 'Scribner', NULL, 'a'),
('f4a5b6c7-d8e9-0123-4567-01234567890a', 21, 'Scribner', '2026-03-01', 'o'),
-- Book 22-24 (Mark Twain)
('a5b6c7d8-e9f0-1234-5678-1234567890ab', 22, 'Dover Publications', NULL, 'a'),
('b6c7d8e9-f0a1-2345-6789-234567890abc', 23, 'Dover Publications', NULL, 'a'),
('c7d8e9f0-a1b2-3456-7890-34567890abcd', 24, 'Bantam Classics', NULL, 'a'),
-- Book 25-27 (Leo Tolstoy)
('d8e9f0a1-b2c3-4567-8901-4567890abcde', 25, 'Penguin Classics', NULL, 'a'),
('e9f0a1b2-c3d4-5678-9012-567890abcdef', 26, 'Penguin Classics', '2025-12-25', 'o'),
('f0a1b2c3-d4e5-6789-0123-67890abcdef0', 27, 'Dover Publications', NULL, 'a'),
-- Book 28-30 (Fyodor Dostoevsky)
('a1b2c3d4-e5f6-7890-1234-7890abcdef01', 28, 'Bantam Classics', NULL, 'a'),
('b2c3d4e5-f6a7-8901-2345-890abcdef012', 29, 'Penguin Classics', NULL, 'a'),
('c3d4e5f6-a7b8-9012-3456-90abcdef0123', 30, 'Dover Publications', NULL, 'r'),
-- Book 31-33 (Gabriel García Márquez)
('d4e5f6a7-b8c9-0123-4567-0abcdef01234', 31, 'Harper Perennial', NULL, 'a'),
('e5f6a7b8-c9d0-1234-5678-abcdef012345', 32, 'Vintage', '2026-01-20', 'o'),
('f6a7b8c9-d0e1-2345-6789-bcdef0123456', 33, 'Penguin Books', NULL, 'a'),
-- Book 34-36 (William Shakespeare)
('a7b8c9d0-e1f2-3456-7890-cdef01234567', 34, 'Simon & Schuster', NULL, 'a'),
('b8c9d0e1-f2a3-4567-8901-def012345678', 35, 'Simon & Schuster', NULL, 'a'),
('c9d0e1f2-a3b4-5678-9012-ef0123456789', 36, 'Simon & Schuster', NULL, 'm'),
-- Book 37-40 (Kafka, Brontë)
('d0e1f2a3-b4c5-6789-0123-f01234567890', 37, 'Schocken', NULL, 'a'),
('e1f2a3b4-c5d6-7890-1234-01234567890a', 38, 'Schocken', NULL, 'a'),
('f2a3b4c5-d6e7-8901-2345-1234567890ab', 39, 'Schocken', NULL, 'a'),
('a3b4c5d6-e7f8-9012-3456-234567890abc', 40, 'Penguin Classics', NULL, 'a'),
-- Book 41-65 (Korean Authors)
('b4c5d6e7-f8a9-0123-4567-34567890abcd', 41, 'Marun', NULL, 'a'),
('c5d6e7f8-a9b0-1234-5678-4567890abcde', 42, 'Changbi', NULL, 'a'),
('d6e7f8a9-b0c1-2345-6789-567890abcdef', 43, 'Changbi', '2026-04-01', 'o'),
('e7f8a9b0-c1d2-3456-7890-67890abcdef0', 44, 'Changbi', NULL, 'a'),
('f8a9b0c1-d2e3-4567-8901-7890abcdef01', 45, 'Knopf', NULL, 'a'),
('a9b0c1d2-e3f4-5678-9012-890abcdef012', 46, 'Munhakdongne', NULL, 'a'),
('b0c1d2e3-f4a5-6789-0123-90abcdef0123', 47, 'Munhakdongne', NULL, 'a'),
('c1d2e3f4-a5b6-7890-1234-0abcdef01234', 48, 'Minumsa', NULL, 'a'),
('d2e3f4a5-b6c7-8901-2345-abcdef012345', 49, 'Jieum', NULL, 'a'),
('e3f4a5b6-c7d8-9012-3456-bcdef0123456', 50, 'Munji', NULL, 'a'),
('f4a5b6c7-d8e9-0123-4567-cdef01234567', 51, 'Hogarth', NULL, 'a'),
('a5b6c7d8-e9f0-1234-5678-def012345678', 52, 'Changbi', '2025-11-11', 'o'),
('b6c7d8e9-f0a1-2345-6789-ef0123456789', 53, 'Munhakdongne', NULL, 'a'),
('c7d8e9f0-a1b2-3456-7890-f01234567890', 54, 'Mariner Books', NULL, 'a'),
('d8e9f0a1-b2c3-4567-8901-01234567890a', 55, 'Munhakdongne', NULL, 'a'),
('e9f0a1b2-c3d4-5678-9012-1234567890ab', 56, 'Munhakdongne', NULL, 'a'),
('f0a1b2c3-d4e5-6789-0123-234567890abc', 57, 'Hainaim', NULL, 'a'),
('a1b2c3d4-e5f6-7890-1234-34567890abcd', 58, 'Changbi', NULL, 'a'),
('b2c3d4e5-f6a7-8901-2345-4567890abcde', 59, 'Hainaim', NULL, 'a'),
('c3d4e5f6-a7b8-9012-3456-567890abcdef', 60, 'Dalkey Archive', NULL, 'a'),
('d4e5f6a7-b8c9-0123-4567-67890abcdef0', 61, 'Nanam', NULL, 'a'),
('e5f6a7b8-c9d0-1234-5678-7890abcdef01', 62, 'Nanam', NULL, 'a'),
('f6a7b8c9-d0e1-2345-6789-890abcdef012', 63, 'Segyesa', NULL, 'a'),
('a7b8c9d0-e1f2-3456-7890-90abcdef0123', 64, 'Jipmundang', NULL, 'a'),
('b8c9d0e1-f2a3-4567-8901-0abcdef01234', 65, 'Jipmundang', NULL, 'a');

INSERT INTO library_genre (name) VALUES
('Fiction'),
('Crime Fiction'),
('Science Fiction'),
('Historical Fiction'),
('Literary Fiction'),
('Non-Fiction'),
('Mystery'),
('Action & Adventure'),
('Business'), 
('Drama'), 
('Fantasy'), 
('Horror'),
('Romance'),
('Mystery'),
('Thriller'),
('Classics'),
('Non-fiction'),
('Young Adult'),
('Self-Help'),
('Memoir'),
('Autobiography'),
('Computer Programming'),
('language'),
('travel'),
('cooking'),
('universe'),
('econology');

INSERT INTO library_language (name) VALUES
('Korean'),
('English'),
('Chinese'),
('Mandarin Chinese'),
('French'),
('German'),
('Hindi'),
('Italian'),
('Russian'),
('Arabic'),
('Portuguese'),
('Bengali'),
('Dutch'),
('Swedish'),
('Japanese'),
('TurKish'),
('Argentinean'),
('Indonesian'),
('Urdu '),
('Egyptian Arabic'),
('Tamil'),
('Vietnamese');
