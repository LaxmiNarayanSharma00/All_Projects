# Recommendation System

When you go to an e-commerce platform, one of the most important factors that induces you to make the actual purchase is how quickly are you able to locate the item you want to buy. One way in which ecommerce platforms achieve is through recommendation systems (also known as recommender systems), e.g. the ‘customers who bought this item also bought…’ section on Amazon. Almost all e-commerce platforms as well as movie & song streaming platforms like Amazon prime, Spotify, Netflix use a variation of recommendation system algorithm. The idea is to improve the user experience. There is an unwritten rule in any business - more happy is your customer, more is your profits.

## Types of Recommendation Systems

### 1. Content-based filtering

One popular technique of recommendation/recommender systems is __content-based filtering__. Content here refers to the attributes or characteristic features of the products you like. So, the idea in content-based filtering is to map the user based on his likes/dislikes to the appropriate products based on the features of the product. Also, note that some features can be important than others. For example, in case of book recommendation, the author name may be a more important feature than genre and price, because people tend to read books by the same author. This suggests that the system needs to assign weights to the features.

This technique is called content-based filtering because you need to understand the content descriptions very well to make good recommendations. As I mentioned before, basic idea of content-based filters is to map the relevant content based on certain features. For example, books may be tagged by features such as author name, price, genre, etc. Another example is movies which may be tagged by attributes such as genre, actors, run-time, year of release, etc. Another example of content-based systems is YouTube. When you watch videos of a certain band, say Pink Flyod or Maroon 5, the system finds other videos which are tagged by the band name. Note that, in this case there is one feature which is more important than all others- the band name. There may be other features like genre, video length, year, etc. but the band name is probably the most important.

So, in content-based systems, you need a way to store two things — the description of the features of the item, and the interest of the user with respect to that feature. In this case, the name of the author is one of the features. The other features can be the genre of the book, price, year of launch, recommended age-group, etc. To solve the first problem, each item is described through an item vector. Thus, if there are n attributes that can be used to describe any item set, the item vector for an item will be a vector of size n having 0 or 1 corresponding to each characteristic (or any value in case we consider weights). Similarly, the taste and preferences of a user is represented by a user vector where rating points are assigned corresponding to each characteristic of the user. The dot product (as a measure of similarity) of the two vectors depicts the compatibility of the item with the user. The higher the value of this dot product, the more is the chance of the user liking the particular product.

### 2. Collaborative filtering

The other extremely popular technique is __collaborative filtering__. The basic idea of collaborative filters is that similar users tend to like similar items and it is based on the assumption that, if some users have had similar interests in the past, they will also have similar tastes in the future too. In collaborative systems, the main advantage is that you do not need to know the content in detail. Amazon’s product ‘Customers who bought this item also bought…’ is a popular example of collaborative filtering. When you buy Inferno by Dan Brown, it recommends other books which were bought by other people who also bought Inferno. In this case, the system may not even care about the genre or the price of the books being recommended; it simply recommends them to you because other people similar to you bought them.

#### User-based Collaborative Filtering

In user-based collaborative filtering, you try to find users who have similar tastes and preferences, based on the past ratings they have given to the same items. The similarity between the users is represented in terms of correlation or cosine similarity. Finally, you can use the weighted sum of the ratings provided by like-minded users for an item to predict what rating may be provided by a user.

#### Item-based Collaborative Filtering

Another extremely successful type of collaborative filtering algorithm is item-based collaborative filtering. Item-based systems are heavily used by companies such as Amazon and various movie recommendation sites. In user-based collaborative filters, you measure the similarity between users. The basic idea is that similar users are likely have similar tastes. In contrast, item-based systems calculate the similarity between various items or products. Next the rating that a particular user will give on a given item is predicted by taking weighted sum of ratings provided by the user on different items that are similar to the given item. 

## About MovieLens dataset

This dataset (ml-latest-small) describes 5-star rating and free-text tagging activity from MovieLens, a movie recommendation service. It contains 100836 ratings and 3683 tag applications across 9742 movies. These data were created by 610 users between March 29, 1996 and September 24, 2018.

Credits: F. Maxwell Harper and Joseph A. Konstan. 2015. The MovieLens Datasets: History and Context. ACM Transactions on Interactive Intelligent Systems (TiiS) 5, 4: 19:1–19:19. https://doi.org/10.1145/2827872

#### Ratings Data File Structure (ratings.csv)

  - All ratings are contained in the file ratings.csv. Each line of this file after the header row represents one rating of one movie by one user, and has the following format: userId,movieId,rating,timestamp

  - The lines within this file are ordered first by userId, then, within user, by movieId.

  - Ratings are made on a 5-star scale, with half-star increments (0.5 stars - 5.0 stars).

  - Timestamps represent seconds since midnight Coordinated Universal Time (UTC) of January 1, 1970.

Link for MovieLens dataset: https://grouplens.org/datasets/movielens/
(The dataset used in this project is in ml-latest-small.zip)
