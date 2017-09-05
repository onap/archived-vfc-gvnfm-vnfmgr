use gvnfm;

CREATE TABLE `VNF_REG` (
    `ID` varchar(200) NOT NULL PRIMARY KEY,
    `IP` varchar(200) NOT NULL,
    `PORT` varchar(200) NOT NULL,
    `USERNAME` varchar(255) NOT NULL,
    `PASSWORD` varchar(255) NOT NULL
)
;

COMMIT;