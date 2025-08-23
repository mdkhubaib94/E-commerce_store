# CS50W Project 2: Commerce

This is my implementation of **Project 2: Commerce** from Harvard's CS50W (Web Programming with Python and JavaScript).  
The project is an **e-commerce auction site** built using Django, where users can create auction listings, place bids, add items to a watchlist, and post comments.

---

## 📌 Features

- **User Authentication**
  - Register, log in, and log out
- **Create Listings**
  - Users can create new auction listings with title, description, starting bid, and an optional image URL
- **Active Listings Page**
  - Displays all currently active auction items
- **Bidding**
  - Users can place bids, with automatic validation against the current highest bid
- **Watchlist**
  - Users can add or remove listings from their personal watchlist
- **Categories**
  - Listings can be filtered by categories
- **Comments**
  - Users can post comments on listings
- **Close Auction**
  - Listing creators can close an auction, awarding it to the highest bidder

---

## 🚀 How to Run: 

   ```bash
   git clone https://github.com/<your-username>/cs50w-project2-commerce.git
   cd cs50w-project2-commerce
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   type into your browser: http://127.0.0.1:8000/




