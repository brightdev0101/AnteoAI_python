CREATE TABLE "users" (
	"id"	integer,
	"username"	text NOT NULL UNIQUE,
	"password"	text NOT NULL,
	"email"	text NOT NULL,
	"name"	text NOT NULL,
	"surname"	text NOT NULL,
	"birthdate"	date NOT NULL,
	"plan"	integer NOT NULL,
	"planExpire"	integer,
	"newsletter"	integer,
	PRIMARY KEY("id")
);

	create table customTrends (
		id integer primary key,
		userId integer not null,
		title text not null,
      	FOREIGN KEY(userId) REFERENCES users(id)
);



