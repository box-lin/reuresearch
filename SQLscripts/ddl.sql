drop apkminsdk if exists apkminsdk
drop apkinscompat if exists apkinscompat
drop apkruncompat if exists apkruncompat
drop apk if exists apk

create table apk (
    apkname varchar,
    typ varchar,
    apkyear varchar,
    apkapi varchar,
    apiyear varchar,
    primary key (apkname, typ)
);

-- if an apk is run compat, runMsg should be None
create table apkruncompat(
    apkname varchar,
    typ varchar,
    run_fail boolean, 
    runMsg varchar,
    primary key (apkname, typ, run_fail),
    foreign key (apkname, typ) references apk(apkname, typ)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

create table apkinscompat(
    apkname varchar,
    typ varchar,
    ins_fail boolean, 
    insMsg varchar,
    primary key (apkname, typ, ins_fail),
    foreign key (apkname, typ) references apk(apkname, typ)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


create table apkminsdk(
    apkname varchar,
    typ varchar,
    minsdk varchar,
    primary key (apkname, typ, minsdk),
    foreign key (apkname, typ) references apk(apkname, typ)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
