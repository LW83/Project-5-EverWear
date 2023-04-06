Bugs
1. Reverse URL error - had wishlist in url on wishlist template instead of Add to Wishlist - Stakcoverflow: https://stackoverflow.com/questions/25359441/using-request-meta-gethttp-referer-in-url-reverse-in-django


Resources
https://favicon.io/ for creation of favicon
https://www.youtube.com/watch?v=OgA0TTKAtqQ&list=PLOLrQ9Pn6caxY4Q1U9RjO1bulQp5NDYS_&index=7 for Wishlist
Adding marksafe to file: https://stackoverflow.com/questions/72013969/nameerror-name-mark-safe-is-not-defined-django

https://www.youtube.com/@YukselCELIK/search?query=Django - Tried to get product variations but could not get working

Ratings from https://github.com/dev-rathankumar/greatkart-pre-deploy/blob/main/store/models.py


Bugs: 
Login redirect error - had a login url in commented out code. Meant couldnt view product detail page when not logged in. Link; https://forum.djangoproject.com/t/reverse-for-logout-not-found-logout-is-not-a-valid-view-function-or-pattern-name-i-am-unable-to-redirect-a-url-page/10364/6
Getting sizes to display dynamically - needed to have color_id in size fields in view