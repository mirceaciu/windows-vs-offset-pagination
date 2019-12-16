# Offset vs Window Functions for SQL pagination.

I've been in the programming business for long enough to see many trends come and go. 

New technologies tend to spun enthusiasm into the community so more and more adopters jump into this waggons. Previous practices are considered old and inefficient tho this is not always the case.


For some migrating from Sql to NoSql seems like a no-brainer. I've noticed this first hand: project migrated to NoSql just to later realize that the effort of implementing and maintaining would vastly overcome any benefits. Turns out that Sql was the better fit and with some optimization some comparable performance could be achieved.

Older doesn't mean worse. Sql for example has evolved over the years and gained new functionality. It's battle testes and has proven it's worth times and times again. We just need to make sure we use it at it's best.


I'm a dedicated pythonista and can't deny the joy of building projects with Python.
I love when someone considers Django or Flask to build their web vision and I am confident when tackling any task knowing that the versatility of Python is backing me up.
This frameworks are easy to set up and deploy and are quite feature rich. All this functionality doesn't always feat our needs tho. It's easy to start a Django project, feed it some thousands of entries for a database and complain: "pagination is slow, I'm moving to NoSql".
Have you tried optimizing for your needs?

     
So here we are, we have reached the context of this article. Sql pagination sometimes can be slow. As database get large our queries take longer to resolve. 
Most frameworks I've used provide an ORM (object relational mapper) as a way of making interating with the database easyers. Instead of writing SQL queries you use this ORM's methods to read and write data to/from the database.  
Some ORMs are more generous and provide some extra functionality you wouldn't typically have access to via simply SQL.

One of such functionality is pagination. 