CREATE TABLE `item` ( `i_id` integer NOT NULL , `title` varchar(20) DEFAULT NULL , PRIMARY KEY (`i_id`) )

CREATE TABLE `review` ( `a_id` integer NOT NULL PRIMARY KEY , `u_id` integer NOT NULL , `i_id` integer NOT NULL , `rating` integer DEFAULT NULL , `rank` integer DEFAULT NULL , FOREIGN KEY (`u_id`) REFERENCES `useracct`(`u_id`) , FOREIGN KEY (`i_id`) REFERENCES `item`(`i_id`) )

CREATE TABLE `useracct` ( `u_id` integer NOT NULL , `name` varchar(128) DEFAULT NULL , PRIMARY KEY (`u_id`) )

CREATE TABLE "trust" (`source_u_id` integer NOT NULL, `target_u_id` integer NOT NULL, `trust` integer NOT NULL, FOREIGN KEY (`source_u_id`) REFERENCES `useracct`(`u_id`), FOREIGN KEY (`target_u_id`) REFERENCES `useracct`(`u_id`))