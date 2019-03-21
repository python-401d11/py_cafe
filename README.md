# py_cafe

**Authors**: Dan-Huy Le, Tim Schoen, Milo Anderson

**Version**: 1.1.0

## Overview:
Py_cafe allows restauranteurs to integrate front-of-house data (customer identity, table reservations) with point-of-sale data (menu orders). Managers can view detailed reports on customer preferences & behavior; customers can accumulate reward points or participate in special offers.

## Features
* Allow users to register as customers.
* As Customers users are able to make reservations and place orders. 
* Customers are able update order by adding or removing items.
* As Orders are being generated users are able to see the grand-total of items in order.
* Managers are allowed to create, both customer and managers roles.
* As a Manager, you have the ability to add, remove, and update items from the menu.  
* Items have the attributes of (Name, Price, Cost (cost of goods sold), and Inventory Count.  
* As Orders are being placed, the inventory count reflects changes in real-time.
* As a Manager you have the ability, to run reports  which include:
** Users Sales ( how much of each item a selected used has ordered)
** Item Sales(how many times each user as ordered a selected item)
** Timely Sales( All Sales detail (User, Item, Quantity, Time) with in a selected time window.


## Getting Started — Running local

1. Clone Repo to local machine.

2. Set up a  Virtual Environment using  PIPENV SHELL
3. Create a database and in your .env file  DATABASE_URL =  << your data base >>
4. Add a secret key to you .env file.  SECRET_KEY = <<your secret key (UUID) >>
5. Install dependencies  using. PIPENV INSTALL
6. Run the app     FLASK RUN


7. In your browser go to localhost:5000

8. In order to set up first manager role go to localhost:5000/user/manager


## Tools Used:
  * Vue.js
  * flask
  * sqlalchemy
  * wtforms
  * SQL
  * postgres 

## Deployment:
* Deployed on AWS - ES2 (server)
*  AWS - RDS (database)
* guincorn -- Python Web Server Gateway Interface HTTP server
* nginx -- web server which can also be used as a reverse proxy, load balancer.

## Credits

 * CSS Skeleton V2.04  was used  Copyright 2014, Dave Gamache, Free to use under MIT license.
 * CSS Inspired by bitsofco.de/holy-grail-layout-css-grid 

 
