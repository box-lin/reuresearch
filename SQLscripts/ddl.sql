DROP TABLE IF EXISTS apitoyear;
DROP TABLE IF EXISTS apktoapi;
DROP TABLE IF EXISTS APKminsdk;
DROP TABLE IF EXISTS apktoyear;
DROP TABLE IF EXISTS apkcompat;
DROP TABLE IF EXISTS apk;
 


create table apk (
    apkname varchar primary key
);

create table apkcompat(
    apkname varchar,
    isFail boolean,
    failMessage varchar,
    primary key (apkname, isFail, failMessage),
    foreign key (apkname) references APK(apkname)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

create table apktoyear(
    apkname varchar,
    apkyear varchar,
    primary key (apkname, apkyear),
    foreign key (apkname) references apk(apkname)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

create table apkminsdk(
    apkname varchar,
    minsdk varchar,
    primary key (apkname, minsdk),
    foreign key (apkname) references apk(apkname)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

create table apktoapi(
    apkname varchar,
    apkapi varchar,
    primary key (apkname, apkapi),
    foreign key (apkname) references apk(apkname)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

create table apitoyear(
    apkname varchar,
    apkapi varchar,
    apiyear varchar,
    primary key (apkname, apkapi, apiyear),
    foreign key (apkname, apkapi) references apktoapi(apkname, apkapi)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);