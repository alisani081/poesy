from django.db import models
from django.contrib.auth.models import User, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=160, blank=True)
    image = models.URLField(blank=True, null=True)
    follows = models.ManyToManyField(
        'self',
        related_name='followed_by',
        symmetrical=False,
        blank=True
    )   
    bookmarks = models.ManyToManyField(
        'poems.Poem',
        related_name='bookmarked_by',
        blank=True
    )
    likes = models.ManyToManyField(
        'poems.Poem',
        related_name='liked_by',
        blank=True
    )

    def natural_key(self):
        return (self.user.username)    

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile` if user not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if user already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if user is following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following user; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()

    def bookmark(self, poem):
        """Bookmark `poem` if user haven't already bookmarked it."""
        self.bookmarks.add(poem)

    def unbookmark(self, poem):
        """Unbookmark `poem` if user already bookmarked it."""
        self.bookmarks.remove(poem)

    def has_bookmarked(self, poem):
        """Returns True if user have Bookmarked `poem`; else False."""
        return self.bookmarks.filter(pk=poem.pk).exists()
    
    def like(self, poem):
        """Like `poem` if user have'nt already liked `poem`"""
        self.likes.add(poem)
    
    def unlike(self, poem):
        """UnLike `poem` if user already liked `poem`"""
        self.likes.remove(poem)
    
    def has_liked(self, poem):
        """Returns True if user already liked `poem`"""
        return self.likes.filter(pk=poem.pk).exists()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
