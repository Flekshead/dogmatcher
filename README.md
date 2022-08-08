# BARK & SOUL
#### Video Demo: https://youtu.be/agx3kPOa4PA
#### Description:
Bark & Soul is a web application which allows users to gauge what physical and behavioral traits of a dog would best match with their preferences and lifestyle. It is run with Flask.

I've worked with dogs as a trainer for several years and one of the main issues  people run into is they get a dog that doesn't mesh well with their character. The reason for this is because people tend to select a dog mostly on how cute it is and don't take into consideration all the other factors that come with having a dog in your home. So I wanted to create a way for people to ascertain what kind of characteristics they should be looking for in a dog outside of the cuteness factor.

**layout.html** - This file sets charset to utf8. It also sets the viewport to be responsive. Additionally, layout.html pulls bootstrap and a styles.css file as stylesheets. This file also uses the pictures found in the static folder. It also dontains a navbar and a Flask placeholder for the main text of each page.

**index.html** - This file is an introduction to the user about the purpose of the application. There is also a link to get to the survey.

**survey.html** - This file contains the form with questions for the user to respond to regarding their lifestyle and preferences. This file also includes logic for showing the correct initial "tab"/button of the form. There is also logic for showing the proper tab when the next or previous button is clicked . Lastly there is a validateForm function which is called when going from tab1 to tab2 as well as when submitting the survey form.

**no_dog.html** - This is a landing page which advises the user to not get a dog. Users are taken to this page if the survey is submitted succesfully and they do not have the necessary time and/or patience to care for a dog. While I don't want to upset anyone, I believe people should be told the hard truth sometimes.

**result.html** - This is the landing page when the survey is succesfully submitted and not routed to the no_dog.html. This page has a table describing the ideal dog attributes for the user. There are also two lists of potential dogs. The primary list more closely matches the users traits and the secondary list expands slightly on those traits to give more options.

**styles.css** - This is the stylesheet I created. In addition to the different formatting styles for certain tags and classes, this file also includes formatting to be responsive to different size screens - adjusting images, navbar, headings, forms. The responsive part took me a while to figure out. I was having trouble with the width of the form on different screens so I created the width-var class and apply different width percentages for varying screen sizes.

**dogs.db** - database of 264 dogs and scores of their physical and behavioral traits. This database is information that was scraped form https://dogtime.com/dog-breeds/profiles/ using the chrome scraper extension. I found this part interesting as I had never used a scraper before and got to learn something new.

**app.py** - imports SQL from cs50 library and Flask, return_template, & request from flask library. This file defines each route for the app (/index and /survey). When survey route is reached via POST method, the logic gathers all of the user's survey answers and assigns the attributes of the user's ideal dog. The logic also creates a primary and secondary list of potential breeds from dogs.db based on user's ideal dog. The primary list is set to very closely resemble the user's ideal dog. Occasionally, I found that the primary list would not have any dog breed options. To address this, I decided to make a secondary list which gives a little more wiggle room in regards to the ideal attributes. 
