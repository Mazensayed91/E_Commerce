from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
	title = models.CharField(max_length = 64)
	image_url = models.CharField(max_length = 2084,default='noimage',blank = True)
	user_id = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'listings') #related_name listings will give me all the listings with this user
	describtion = models.CharField(max_length = 128)
	active = models.BooleanField(default = True)

	def __str__(self):
		return f"Listing : {self.title}"

class Category(models.Model):
	category = models.CharField(max_length = 64)
	listing_id = models.ForeignKey(Listing,on_delete = models.CASCADE,related_name = 'categories')

	def __str__(self):
		return f"Category is {self.category}"

class Bid(models.Model):
	max_bid = models.IntegerField()
	starting_bid = models.IntegerField()
	listing_id = models.ForeignKey(Listing,on_delete = models.CASCADE,related_name = 'bid')
	user_id = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'bids')


class Comment(models.Model):
	comment = models.CharField(max_length = 200)
	listing_id = models.ForeignKey(Listing,on_delete = models.CASCADE,related_name = 'comments')

class WatchListItem(models.Model):
	listing = models.ForeignKey(Listing,on_delete = models.CASCADE,related_name = 'watchlistitem')
	users = models.ManyToManyField(User,blank = True,related_name = "watchlistitems")
