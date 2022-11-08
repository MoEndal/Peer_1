
CREATE TABLE timetable (
    Id SERIAL PRIMARY KEY,
    statring timestamp  NOT NULL,
    ending timestamp NOT NULL,
    project varchar(255) NOT NULL,
    tasks varchar(255) NOT NULL
);




