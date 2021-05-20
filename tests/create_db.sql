CREATE TABLE gsheet ('influence','Naam','Bijgewerkt','Cred.cap.','Taakstelling voor WS-ontwikkeling
(geen spaties in dit veld!)','WhiteStar 1 :15
WhiteStar 2 :15
        X :169','Transport','Total Cargo Slots','Miner','Hydrogen Capacity','Battleship','Cargo bay extension','Shipment Computer','Trade boost','Rush','Trade burst','Shipment Drone','Offload','Shipment Beam','Entrust','Dispatch','Recall','Relic Drone','Mining Boost','Hydrogen bay extension','Enrich','Remote mining','Hydrogen upload','Mining Unity','Crunch','Genesis','Hydrogen Rocket','Mining Drone','Weak Battery','Battery','Laser','Mass battery','Dual laser','Barrage','Dart Launcher','Alpha Shield','Delta shield','Passive shield','Omega shield','Mirror shield','Blast Shield','Area shield','EMP','Teleport','Red star life extender','Remote Repair','Time warp','Unity','Sanctuary','Stealth','Fortify','Impulse','Alpha Rocket','Salvage','Suppress','Destiny','Barrier','Vengeance','Delta Rocket','Leap','Bond','Alpha Drone','Suspend','Omega Rocket','Remote Bomb');
CREATE TABLE Status (
        DiscordId TEXT,
        LastUpdate NUMERIC,
        StatusText TEXT
, Id INTEGER);
CREATE VIEW gsheet_v
as select g.Naam as Naam, g."WhiteStar 1 :15
WhiteStar 2 :15
        X :169" as WhiteStar
from gsheet g
/* gsheet_v(Naam,WhiteStar) */;
CREATE TABLE UserMap (
        DiscordId TEXT,
        DiscordAlias TEXT,
        GsheetAlias TEXT
, Id INTEGER);
CREATE TABLE IF NOT EXISTS "WSinschrijvingen" (
        DiscordId TEXT,
        inschrijving TEXT,
        Opmerkingen TEXT,
        Inschrijftijd TEXT,
        actueel TEXT DEFAULT ja
, Id INTEGER);
CREATE TABLE temp_ws (username, Id INTEGER);
CREATE TABLE WSReturn (
        Id INTEGER NOT NULL,
        ws TEXT,
        Shiptype TEXT,
        ReturnTime TEXT,
        NotificationTime TEXT
);


insert into usermap (DiscordId, DiscordAlias, GsheetAlias, Id) values ('discordid1','discordalias1','gsheetalias1',1); /* test_usermap */