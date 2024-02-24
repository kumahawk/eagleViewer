BEGIN TRANSACTION;
DROP TABLE IF EXISTS "folders";
CREATE TABLE IF NOT EXISTS "folders" (
	"id"	TEXT,
	"name"	TEXT,
	"parent"	TEXT,
	"modificationTime"	TIMESTAMP,
	PRIMARY KEY("id")
);
DROP TABLE IF EXISTS "tags";
CREATE TABLE IF NOT EXISTS "tags" (
	"id"	INTEGER,
	"libid"	INTEGER,
	"name"	TEXT,
	"prefered"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("libid") REFERENCES "libraries"("id")
);
DROP TABLE IF EXISTS "imageinfolder";
CREATE TABLE IF NOT EXISTS "imageinfolder" (
	"folderid"	TEXT,
	"imageid"	TEXT,
	PRIMARY KEY("folderid","imageid"),
	FOREIGN KEY("imageid") REFERENCES "images",
	FOREIGN KEY("folderid") REFERENCES "folders"
);
DROP TABLE IF EXISTS "imageintag";
CREATE TABLE IF NOT EXISTS "imageintag" (
	"tagid"	INTEGER,
	"imageid"	TEXT,
	PRIMARY KEY("tagid","imageid"),
	FOREIGN KEY("imageid") REFERENCES "images",
	FOREIGN KEY("tagid") REFERENCES "tags"
);
DROP TABLE IF EXISTS "folderintag";
CREATE TABLE IF NOT EXISTS "folderintag" (
	"tagid"	INTEGER,
	"folderid"	TEXT,
	PRIMARY KEY("tagid","folderid"),
	FOREIGN KEY("folderid") REFERENCES "folders",
	FOREIGN KEY("tagid") REFERENCES "tags"
);
DROP TABLE IF EXISTS "libraries";
CREATE TABLE IF NOT EXISTS "libraries" (
	"id"	INTEGER,
	"path"	TEXT,
	"lastupdate"	TIMESTAMP,
	PRIMARY KEY("id" AUTOINCREMENT)
);
DROP TABLE IF EXISTS "images";
CREATE TABLE IF NOT EXISTS "images" (
	"id"	TEXT,
	"libId"	INTEGER,
	"name"	TEXT,
	"size"	INTEGER,
	"btime"	TIMESTAMP,
	"mtime"	TIMESTAMP,
	"ext"	TEXT,
	"height"	INTEGER,
	"width"	INTEGER,
	"annotation"	TEXT,
	"modificationTime"	TIMESTAMP,
	"lastModified"	TIMESTAMP,
	"star"	INTEGER,
	"noThumbnail"	INTEGER,
	"isDeleted"	INTEGER DEFAULT 0,
	PRIMARY KEY("id"),
	FOREIGN KEY("libid") REFERENCES "libraries"("id")
);
DROP INDEX IF EXISTS "image_folder";
CREATE INDEX IF NOT EXISTS "image_folder" ON "imageinfolder" (
	"imageid",
	"folderid"
);
DROP INDEX IF EXISTS "image_tag";
CREATE INDEX IF NOT EXISTS "image_tag" ON "imageintag" (
	"imageid",
	"tagid"
);
DROP INDEX IF EXISTS "folder_tag";
CREATE INDEX IF NOT EXISTS "folder_tag" ON "folderintag" (
	"folderid",
	"tagid"
);
DROP INDEX IF EXISTS "folder_image";
CREATE INDEX IF NOT EXISTS "folder_image" ON "imageinfolder" (
	"folderid",
	"imageid"
);
DROP INDEX IF EXISTS "tag_image";
CREATE INDEX IF NOT EXISTS "tag_image" ON "imageintag" (
	"tagid",
	"imageid"
);
DROP INDEX IF EXISTS "tag_folder";
CREATE INDEX IF NOT EXISTS "tag_folder" ON "folderintag" (
	"tagid",
	"folderid"
);
COMMIT;
